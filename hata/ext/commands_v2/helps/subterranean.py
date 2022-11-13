__all__ = ('SubterraneanHelpCommand', )

from functools import partial as partial_func

from scarletio import CallableAnalyzer, DOCS_ENABLED, docs_property

from ....discord.channel import Channel
from ....discord.embed import Embed, EmbedBase
from ....discord.emoji.emoji import Emoji
from ....discord.guild import Guild
from ....discord.invite import Invite
from ....discord.message import Message
from ....discord.preconverters import preconvert_str
from ....discord.role import Role
from ....discord.user import User, UserBase
from ....discord.utils import chunkify

from ...command_utils import Closer, Pagination

from ..command_helpers import run_checks
from ..content_parser import relativedelta, timedelta
from ..utils import raw_name_to_display


MAX_SUB_COMMAND_DEEPNESS = 5

MAX_LINE_PER_PAGE = 24
DEFAULT_PREFIX = '**>>**'

PARAMETER_REQUIRED_START = '<'
PARAMETER_REQUIRED_END = '>'
PARAMETER_OPTIONAL_START = '*'
PARAMETER_OPTIONAL_END = '*'

PARAMETER_NAME_REST = 'rest'

PARAMETER_TYPE_TO_NAME = {
    UserBase: 'user',
    User: 'user',
    Channel: 'channel',
    Invite: 'invite',
    Role: 'role',
    Guild: 'guild',
    Message: 'message',
    str: 'string',
    int: 'integer',
    timedelta: 'time-delta',
    Emoji: 'emoji',
}

if (relativedelta is not None):
    PARAMETER_TYPE_TO_NAME[relativedelta] = 'relative-time-delta'

PARAMETER_UNDEFINED = 'undefined'

DEFAULT_HELP_NAME = 'help'

PARAMETER_SEPARATOR_SPACE_AFTER_ONLY = {
    ',',
    ':',
    ';',
}


def check_user(user, event):
    """
    Checks whether the ``ReactionAddEvent``, ``ReactionDeleteEvent``'s user is same as the given one.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user who should be matched.
    event : ``ReactionAddEvent``, ``ReactionDeleteEvent``
        The reaction addition or deletion event.
    """
    return (event.user is user)


async def run_command_checks(command_context, command):
    """
    Returns whether the given command checks pass and it is not hidden either.
    
    This function is a coroutine.
    
    Parameters
    ----------
    command_context : ``CommandContext``
        Respective command context.
    command : ``Command``
        The command to check.
    
    Returns
    -------
    should_show : `bool`
    """
    if command.hidden:
        return False
    
    if command.hidden_if_checks_fail:
        failed_check = await run_checks(command._iter_own_checks(), command_context)
        if (failed_check is not None):
            return False
    
    return True


async def run_command_checks_in_category(command_context, command):
    """
    Returns whether the given command should be shown. Checks the category and the command as well.
    
    This function is a coroutine.
    
    Parameters
    ----------
    command_context : ``CommandContext``
        Respective command context.
    command : ``Command``
        The command to check.
    
    Returns
    -------
    should_show : `bool`
        Whether the command should be shown.
    """
    category = command.get_category()
    if category is None:
        # runtime error
        return False
    
    if category.hidden:
        return False
    
    if category.hidden_if_checks_fail:
        failed_check = await run_checks(category._iter_own_checks(), command_context)
        if (failed_check is not None):
            return False
    
    if command.hidden:
        return False
    
    if command.hidden_if_checks_fail:
        failed_check = await run_checks(command._iter_own_checks(), command_context)
        if (failed_check is not None):
            return False
    
    return True


async def is_category_command_shown(command_context, category):
    """
    Returns whether the any command of the category should be shown.
    
    This function is a coroutine.
    
    command_context : ``CommandContext``
        Respective command context.
    command : ``Category``
        The category to check.
    
    Returns
    -------
    should_show : `bool`
        Whether any command would be shown.
    """
    for command in category.command_instances:
        if await run_command_checks(command_context, command):
            return True
    
    return False


async def list_category_commands(command_context, category):
    """
    Returns the commands which should be shown under the given category.
    
    This function is a coroutine.
    
    command_context : ``CommandContext``
        Respective command context.
    command : ``Category``
        The category to check.
    
    Returns
    -------
    commands : `list` of ``Command``
        The commands to show.
    """
    commands = []
    for command in category.command_instances:
        if await run_command_checks(command_context, command):
            commands.append(command)
    
    return commands


async def run_category_checks(command_context, category):
    """
    Returns whether the given category's checks pass and it is not hidden either.
    
    This function is a coroutine.
    
    command_context : ``CommandContext``
        Respective command context.
    command : ``Category``
        The category to check.
    
    Returns
    -------
    should_show : `bool`
    """
    if category.hidden:
        return False
    
    if category.hidden_if_checks_fail:
        failed_check = await run_checks(category._iter_own_checks(), command_context)
        if (failed_check is not None):
            return False
    
    return True


async def should_show_category(command_context, category):
    """
    Returns whether the given category's should be shown.
    
    This function is a coroutine.
    
    command_context : ``CommandContext``
        Respective command context.
    command : ``Category``
        The category to check.
    
    Returns
    -------
    should_show : `bool`
    """
    if await run_category_checks(command_context, category):
        return await is_category_command_shown(command_context, category)
    
    return False


def iter_sub_commands(command_category, command_name_trace):
    """
    Iterates overt he cub commands of a command or a command category.
    
    This function is a generator.
    
    Parameters
    ----------
    command_category : ``Command``, ``CommandCategory``
        The command or command category to iterate trough.
    
    Yields
    ------
    command_path_and_function : `str`, ``CommandFunction``
        Path to a command function and itself.
    """
    command_name_trace.append(command_category.display_name)
    command_name_joined = ' '.join(command_name_trace)
    
    command_function = command_category._command_function
    if (command_function is not None):
        yield command_name_joined, command_function
    
    if len(command_name_trace) != MAX_SUB_COMMAND_DEEPNESS:
        command_categories = command_category._command_categories
        if (command_categories is not None):
            for sub_command_category in command_categories:
                yield from iter_sub_commands(sub_command_category, command_name_trace)
    
    del command_name_trace[-1]


def get_sub_commands(command):
    """
    Gets the sub commands and sub command functions of a command.
    
    Parameter
    ---------
    command : ``Command``
        The respective command.
    
    Returns
    -------
    command_paths_and_functions : `list` of `str`, ``CommandFunction``
    Sorted command paths and functions.
    """
    return sorted(iter_sub_commands(command, []))


def get_parameter_name(command_parameter):
    """
    Gets the command parameter's name-
    
    Parameters
    ----------
    command_parameter : ``CommandParameter``
        The parameter.
    
    Returns
    -------
    command_parameter_name : `str`
    """
    parameter_names = []
    for detail in command_parameter._iter_details():
        type_ = detail.type
        if (type_ is not None):
            try:
                parameter_name = PARAMETER_TYPE_TO_NAME[type_]
            except KeyError:
                pass
            else:
                parameter_names.append(parameter_name)
                continue
        
        parameter_name = detail.converter.alternative_type_name
        if parameter_name is None:
            parameter_name = PARAMETER_UNDEFINED
        
        parameter_names.append(parameter_name)
    
    return ' / '.join(parameter_names)


def generate_command_parameter_representation(command_parameter, separator, assigner):
    """
    Generates a command parameter's representation.
    
    Parameters
    ----------
    command_parameter : ``CommandParameter``
        The command parameter to represent.
    separator : `str`
        Separator separating command parameters if needed.
    assigner : `str`
        Assigner to assign command parameters.
    
    Returns
    -------
    representation : `str`
    """
    if command_parameter.is_rest:
        return f'{PARAMETER_OPTIONAL_START}{command_parameter.display_name}{PARAMETER_OPTIONAL_END}'
    
    detail = command_parameter.detail
    if (detail is not None) and (not detail.converter_setting.requires_part):
        return None
    
    if command_parameter.is_kwargs:
        return f'{PARAMETER_OPTIONAL_START}...{assigner}...~1{PARAMETER_OPTIONAL_END}{separator}' \
               f'{PARAMETER_OPTIONAL_START}...{assigner}...~2{PARAMETER_OPTIONAL_END}{separator}' \
               f'...'
    
    parameter_name = get_parameter_name(command_parameter)
    if command_parameter.is_args:
        return f'{PARAMETER_OPTIONAL_START}{parameter_name}~1{PARAMETER_OPTIONAL_END}{separator}' \
               f'{PARAMETER_OPTIONAL_START}{parameter_name}~2{PARAMETER_OPTIONAL_END}{separator}' \
               f'...'
    
    if command_parameter.is_positional:
        return f'{PARAMETER_REQUIRED_START}{parameter_name}{PARAMETER_REQUIRED_END}'
    
    if command_parameter.is_keyword:
        return f'{PARAMETER_OPTIONAL_START}' \
               f'{command_parameter.display_name}{assigner}{parameter_name}' \
               f'{PARAMETER_OPTIONAL_END}'
    
    return None


def generate_command_parameters(command_function):
    """
    Generates command parameter annotations for the given command function.
    
    Parameters
    ----------
    command_function : ``CommandFunction``
        Command function ot generate representation of.
    
    Returns
    -------
    command_parameters : `None`, `str`
        The command function's parameters representation if has any.
    """
    content_parser = command_function._content_parser
    content_parameter_parser = content_parser._content_parameter_parser
    assigner = content_parameter_parser.assigner
    separator = content_parameter_parser.separator
    
    if type(separator) is str:
        if separator in PARAMETER_SEPARATOR_SPACE_AFTER_ONLY:
            parameter_separator = f'{separator} '
        else:
            parameter_separator = f' {separator} '
    else:
        parameter_separator = ' '
    
    if assigner.endswith(' '):
        parameter_assigner = assigner
    else:
        parameter_assigner = f'{assigner} '
    
    parameter_representations = []
    for command_parameter in content_parser._parameters:
        parameter_representation = generate_command_parameter_representation(command_parameter, \
            parameter_separator, parameter_assigner)
        
        if (parameter_representation is not None):
            parameter_representations.append(parameter_representation)
    
    if parameter_representations:
        command_parameters = parameter_separator.join(parameter_representations)
    else:
        command_parameters = None
    
    return command_parameters


def category_sort_key(category):
    """
    Sort key for sorting categories.
    
    Parameters
    ----------
    category : ``Category``
        A command processor's category.
    
    Returns
    -------
    sort_key : `str`
        The categories are sorted based on their display name.
    """
    return category.display_name


class SubterraneanHelpHelp:
    """
    Shows the usage of help of a respective help command.
    
    Attributes
    ----------
    embed_postprocessor : `None`, `callable`
        An embed post-processor, what is called with the autogenerated embeds.
    """
    __slots__ = ('embed_postprocessor', )
    
    def __init__(self, parent):
        """
        Creates a new Subterranean help help instance.
        
        Attributes
        ----------
        parent : ``SubterraneanHelpCommand``
            The parent of the help helper.
        """
        self.embed_postprocessor = parent.embed_postprocessor
    
    async def __call__(self, command_context):
        """
        Returns the respective help command's generated help embed.
        
        Parameters
        ----------
        command_context : ``CommandContext``
            The help command's context.
        command : ``Command``
            The command to display it's help.
        
        Returns
        -------
        embed : ``Embed``
        """
        prefix = command_context.prefix
        
        embed = Embed(
            command_context.command.display_name,
            f'Shows the help command of the client.\n'
            f'Try `{prefix}{command_context.command.display_name}` for displaying the categories or the commands\' of them.',
        )
        
        embed_postprocessor = self.embed_postprocessor
        if (embed_postprocessor is not None):
            embed_postprocessor(command_context, embed)
        
        return embed


class SubterraneanHelpCommand:
    __class_doc__ = (
    """
    A default help command shipped with hata's commands v2 extension.
    
    Usage
    -----
    After you did setup your client, just add the command to your client.
    
    ```py
    from hata import Client
    from hata.ext.commands.helps.subterranean import SubterraneanHelpCommand
    
    Orin = Client(
        'TOKEN',
        extensions = ('commands_v2', 'command_utils'),
        prefix = 'o|',
    )
    
    Orin.commands(SubterraneanHelpCommand(), 'help')
    
    Orin.start()
    ```
    
    You can also add prefix in front of commands, when listing them. Just pass a `prefix` keyword parameter as a string.
    
    If you want to modify each autogenerated embed, then we got you as well! There is an `embed_postprocessor`
    parameter just for this.
    
    The following 2 values are passed to it:
    
    +-----------------------+-------------------------------+
    | Respective name       | Type                          |
    +=======================+===============================+
    | command_context       | ``CommandContext``            |
    +-----------------------+-------------------------------+
    | command_or_category   | ``Command``, ``Category``     |
    +-----------------------+-------------------------------+
    
    Here is an example using `embed_postprocessor`:
    ```py
    from hata import Client
    from hata.ext.commands.helps.subterranean import SubterraneanHelpCommand
    
    Orin = Client(
        'TOKEN',
        extensions = ('commands_v2', 'command_utils'),
        prefix = 'o|',
    )
    
    def embed_postprocessor(command_context, command_or_category, embed):
        embed.add_thumbnail(command_context.client.avatar_url)
        
        if (embed.color is None):
            if command is help_command:
                color = 0xffffff
            else:
                color = command_context.author.color_at(command_context.guild)
            
            embed.color = color
    
    help_command = Orin.commands(
        SubterraneanHelpCommand(
            embed_postprocessor=embed_postprocessor,
        ),
        'help',
    )
    
    
    # Add a command as well to showcase
    @Orin.commands
    async def ping(client, message):
        return 'pong'
    
    
    Orin.start()
    ```
    
    Note, that `embed_postprocessor` feature is only experimental for now.
    
    Attributes
    ----------
    embed_postprocessor : `None`, `callable`
        An embed post-processor, what is called with the autogenerated embeds.
    prefix : `str`
        Prefix inserted before commands' display name.
    """ ) if DOCS_ENABLED else None
    
    @property
    def __instance_doc__(self):
        """
        Returns the help of the help for the help command.
        
        Returns
        -------
        help_help : ``SubterraneanHelpHelp``
        """
        return SubterraneanHelpHelp(self)
    
    __doc__ = docs_property()
    
    __slots__ = ('embed_postprocessor', 'prefix')
    
    def __new__(cls, prefix = None, embed_postprocessor=None):
        """
        Creates a new ``SubterraneanHelpCommand``.
        
        Parameters
        ----------
        prefix : `None`, `str` = `None`, Optional
            Prefix inserted before commands' display name.
        
        embed_postprocessor : `None`, `callable` = `None`, Optional
            An embed post-processor, what is called with the autogenerated embeds.
            
            The following `2` parameters are passed to it:
            
            +-----------------------+-------------------------------+
            | Respective name       | Type                          |
            +=======================+===============================+
            | command_context       | ``CommandContext``            |
            +-----------------------+-------------------------------+
            | command_context       | ``Command``, ``Category``     |
            +-----------------------+-------------------------------+
        
        Raises
        ------
        TypeError
            If `embed_postprocessor` is given, but not as a `non-async` `callable` accepting `2` parameters.
        """
        if (embed_postprocessor is not None):
            analyzer = CallableAnalyzer(embed_postprocessor)
            min_, max_ = analyzer.get_non_reserved_positional_parameter_range()
            if min_ > 3:
                raise TypeError(
                    f'`embed_postprocessor` should accept `3` parameters: `command_context, '
                    f'command_context`, meanwhile the given one expects at least `{min_!r}`, got '
                    f'{embed_postprocessor!r}.'
                )
            
            if (min_ != 2) and (max_ < 2) and (not analyzer.accepts_args()):
                raise TypeError(
                    f'`embed_postprocessor` should accept `2` parameters: `command_context, '
                    f'command_context`, meanwhile the given one expects up to `{max_!r}`, got '
                    f'{embed_postprocessor!r}.'
                )
            
            if analyzer.is_async():
                raise TypeError(
                    f'`embed_postprocessor` cannot be async, got {embed_postprocessor!r}.'
                )
        
        if prefix is None:
            prefix = DEFAULT_PREFIX
        else:
            prefix = preconvert_str(prefix, 'prefix', 1, 32)
        
        self = object.__new__(cls)
        self.embed_postprocessor = embed_postprocessor
        self.prefix = prefix
        return self
    
    
    def __repr__(self):
        """Returns the help command's representation."""
        repr_parts = [
            '<', self.__class__.__name__,
        ]
        
        prefix = self.prefix
        if (prefix == DEFAULT_PREFIX):
            field_added = False
        else:
            field_added = True
            repr_parts.append(' prefix=')
            repr_parts.append(repr(prefix))
        
        embed_postprocessor = self.embed_postprocessor
        if (embed_postprocessor is not None):
            if not field_added:
                repr_parts.append(',')
            
            repr_parts.append(' embed_postprocessor=')
            repr_parts.append(repr(embed_postprocessor))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    async def __call__(self, command_context, name=None):
        """
        Calls the subterranean help command.
        
        Parameters
        ----------
        command_context : ``CommandContext``
            The command's context.
        name : `None`, `str` = `None`, Optional
            Search term to lookup a category or a command.
        """
        if name is None:
            await self.list_categories(command_context)
            return
        
        if name.isdecimal() and len(name)<21: # do not convert longer names than 64 bit.
            await self.list_category_indexed(command_context, name)
        else:
            await self.lookup_by_name(command_context, name)
    
    
    async def lookup_by_name(self, command_context, name):
        """
        Tries to lookup a command, then a category with the given `name`.
        
        Parameters
        ----------
        command_context : ``CommandContext``
            The command's context.
        name : `str`
            Search term to lookup a category or a command.
        """
        name = raw_name_to_display(name)
        
        command_processor = command_context.client.command_processor
        try:
            command = command_processor.command_name_to_command[name]
        except KeyError:
            category = command_processor.category_name_to_category.get(name, None)
            if (category is None) or (not await run_category_checks(command_context, category)):
                await self.command_not_found(command_context, name)
                return
        else:
            if await run_command_checks_in_category(command_context, command):
                await self.show_command(command_context, command)
            else:
                await self.command_not_found(command_context, name)
            return
        
        commands = await list_category_commands(command_context, category)
        if commands:
            command_names = sorted(command.display_name for command in commands)
            await self.list_commands(command_context, command_names, category.display_name)
        else:
            await self.command_not_found(command_context, name)
    
    
    async def show_command(self, command_context, command):
        """
        SHows the given command's description.
        
        Parameters
        ----------
        command_context : ``CommandContext``
            Respective command's context.
        command : ``Command``
            The respective command.
        """
        description = command.description
        if isinstance(description, str):
            await self.show_string_description(command_context, command.display_name, description)
            return
        
        if callable(description):
            embed = await description(command_context)
            embed_type = type(embed)
            if issubclass(embed_type, EmbedBase):
                await Closer(command_context.client, command_context.message.channel, embed,
                    check = partial_func(check_user, command_context.message.author))
                return
            
            if issubclass(embed_type, (tuple, set)) or hasattr(embed_type, '__getitem__') and hasattr(embed_type, '__len__'):
                await Pagination(command_context.client, command_context.message.channel, embed,
                    check = partial_func(check_user, command_context.message.author))
                return
            
            # No more case, go back to default
        
        await self.show_autogenerated_description(command_context, command)
    
    
    async def command_not_found(self, command_context, name):
        """
        Called, when no command or category was found with the given name,
        
        Parameters
        ----------
        command_context : ``CommandContext``
            Command context of the respective
        name : `str`
            The search word.
        """
        embed = Embed('Command not found.',
            f'There is no category or command named as: `{name}`.\n'
            f'Try using `{command_context.prefix}help`',
        )
        
        embed_postprocessor = self.embed_postprocessor
        if (embed_postprocessor is not None):
            embed_postprocessor(command_context, embed)
        
        await Closer(command_context.client, command_context.message.channel, embed,
            check = partial_func(check_user, command_context.message.author))
    
    
    async def list_categories(self, command_context):
        """
        Lists the categories of the respective client's command preprocessor.
        
        Parameters
        ----------
        command_context : ``CommandContext``
            The called command's context.
        """
        categories = command_context.client.command_processor.categories
        
        displayable_categories = []
        
        for category in categories:
            if await should_show_category(command_context, category):
                displayable_categories.append(category)
        
        
        
        displayable_categories_length = len(displayable_categories)
        if displayable_categories_length == 1:
            await self.list_category(command_context, displayable_categories[0], display_category_name=False)
            return
        
        category_names = sorted(category.display_name for category in displayable_categories)
        pages = []
        
        if displayable_categories_length == 0:
            pages.append('*[No available category or command]*')
        else:
            page = []
            page_line_count = 0
            for index, category_name in enumerate(category_names, 1):
                page.append(str(index))
                page.append('.: ')
                page.append(category_name)
                
                page_line_count += 1
                
                if page_line_count == MAX_LINE_PER_PAGE:
                    pages.append(''.join(page))
                    page.clear()
                    page_line_count = 0
                else:
                    page.append('\n')
            
            if page_line_count:
                del page[-1]
                pages.append(''.join(page))
        
        page_count = len(pages)
        
        field_name = f'Use `{command_context.prefix}help <category/command>` for more information.'
        
        embeds = [
            Embed('Categories', page).add_field(field_name, f'page {index}/{page_count}')
                for index, page in enumerate(pages, 1)
        ]
        
        embed_postprocessor = self.embed_postprocessor
        if (embed_postprocessor is not None):
            for embed in embeds:
                embed_postprocessor(command_context, embed)
        
        await Pagination(command_context.client, command_context.message.channel, embeds,
            check = partial_func(check_user, command_context.message.author))
    
    
    async def list_category(self, command_context, category, display_category_name=True):
        """
        Lists the given category's commands.
        
        This command only collects the displayable commands' names, then calls ``.list_commands``.
        
        Parameters
        ----------
        command_context : ``CommandContext``
            The called command's context.
        category : ``Category``
            The category, which' commands will be listed.
        display_category_name : `bool` = `True`, Optional
            Whether the display name of the given category should be displayed. Defaults to `True`.
        """
        commands = await list_category_commands(command_context, category)
        command_names = sorted(command.display_name for command in commands)
        
        if display_category_name:
            category_name = category.display_name
        else:
            category_name = None
        
        await self.list_commands(command_context, command_names, category_name)
    
    
    async def list_commands(self, command_context, command_names, category_name):
        """
        Lists the given commands.
        
        Parameters
        ----------
        command_context : ``CommandContext``
            The called command's context.
        command_names : `list` of `str`
            The command's names to display.
        category_name : `None or `str`
            The respective category's name.
        """
        pages = []
        page = []
        page_line_count = 0
        prefix = self.prefix
        for command_name in command_names:
            page.append(prefix)
            page.append(' ')
            page.append(command_name)
            
            page_line_count +=1
            
            if page_line_count == MAX_LINE_PER_PAGE:
                pages.append(''.join(page))
                page.clear()
                page_line_count = 0
            else:
                page.append('\n')
        
        if page_line_count:
            del page[-1]
            pages.append(''.join(page))
        
        page_count = len(pages)
        
        field_name = f'Use `{command_context.prefix}help <command>` for more information.'
        
        if category_name is None:
            title = 'Commands'
        else:
            title = f'Commands of {category_name}'
        
        embeds = [
            Embed(title, page).add_field(field_name, f'page {index}/{page_count}')
                for index, page in enumerate(pages, 1)]
        
        embed_postprocessor = self.embed_postprocessor
        if (embed_postprocessor is not None):
            for embed in embeds:
                embed_postprocessor(command_context, embed)
        
        await Pagination(command_context.client, command_context.message.channel, embeds,
            check = partial_func(check_user, command_context.message.author))
    
    
    async def list_category_indexed(self, command_context, name):
        """
        Tries to find the category with the given `name` (decimal only string) index value.
        
        If the represented index ends up out of bounds, calls ``.lookup_by_name``, if not, then ``.list_commands``.
        
        Parameters
        ----------
        command_context : ``CommandContext``
            The called command's context.
        name : `str`
            Decimal only string, which might represent a category's index.
        """
        category_index = int(name)
        if category_index == 0:
            await self.lookup_by_name(command_context, name)
            return
        
        categories = iter(sorted(command_context.client.command_processor.categories, key = category_sort_key))
        
        while category_index > 1:
            try:
                category = next(categories)
            except StopIteration:
                await self.lookup_by_name(command_context, name)
                return
            
            if not await should_show_category(command_context, category):
                continue
            
            category_index -= 1
            continue
        
        
        while True:
            try:
                category = next(categories)
            except StopIteration:
                await self.lookup_by_name(command_context, name)
                return
            
            if not await run_category_checks(command_context, category):
                continue
            
            commands = await list_category_commands(command_context, category)
            if not commands:
                continue
            
            break
        
        command_names = sorted(command.display_name for command in commands)
        
        await self.list_commands(command_context, command_names, category.display_name)
    
    
    async def show_string_description(self, command_context, command_name, description):
        """
        Shows the given string description.
        
        Parameters
        ----------
        command_context : ``CommandContext``
            The called command's context.
        command_name : `str`
            The respective command's display name.
        description : `str`
            The respective command's description.
        """
        if len(description) < 2048:
            embed = Embed(command_name, description)
            
            embed_postprocessor = self.embed_postprocessor
            if (embed_postprocessor is not None):
                embed_postprocessor(command_context, embed)
            
            await Closer(command_context.client, command_context.message.channel, embed,
                check = partial_func(check_user, command_context.message.author))
        
        else:
            description_parts = chunkify(description.splitlines())
            embeds = [Embed(command_name, description_part) for description_part in description_parts]
            
            embed_postprocessor = self.embed_postprocessor
            if (embed_postprocessor is not None):
                for embed in embeds:
                    embed_postprocessor(command_context, embed)
            
            await Pagination(command_context.client, command_context.message.channel, embeds,
                check = partial_func(check_user, command_context.message.author))
    
    
    async def show_autogenerated_description(self, command_context, command):
        """
        Generates, then sends the description of the given description-less command.
        
        Parameters
        ----------
        command_context : ``CommandContext``
            The called command's context.
        command : ``Command``
            The respective command.
        """
        prefix = command_context.prefix
        
        description_lines = []
        
        sun_commands = get_sub_commands(command)
        if len(sun_commands) == 0:
            description_lines.append('*no usages*')
        else:
            if len(sun_commands) == 1:
                description_lines.append('Usage:')
            else:
                description_lines.append('Usages:')
            
            for command_path, command_function in sun_commands:
                description_line = ['`', prefix, command_path]
                command_parameters = generate_command_parameters(command_function)
                if command_parameters is not None:
                    description_line.append(' ')
                    description_line.append(command_parameters)
                
                description_line.append('`')
                
                description_lines.append(''.join(description_line))
        
        
        embed = Embed(command.display_name, '\n'.join(description_lines))
        
        embed_postprocessor = self.embed_postprocessor
        if (embed_postprocessor is not None):
            embed_postprocessor(command_context, embed)
        
        await Closer(command_context.client, command_context.message.channel, embed,
            check = partial_func(check_user, command_context.message.author))
