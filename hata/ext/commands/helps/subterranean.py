# -*- coding: utf-8 -*-
__all__ = ('SubterraneanHelpCommand', )

from functools import partial as partial_func

from ....backend.utils import DOCS_ENABLED, doc_property
from ....backend.futures import is_awaitable
from ....backend.analyzer import CallableAnalyzer
from ....discord.embed import Embed
from ....discord.utils import chunkify
from ....discord.preconverters import preconvert_color, preconvert_str
from ....discord.user import UserBase, User
from ....discord.channel import ChannelBase, ChannelGuildBase, ChannelTextBase, ChannelText, ChannelPrivate, \
    ChannelVoice, ChannelGroup, ChannelCategory, ChannelStore, ChannelThread
from ....discord.role import Role
from ....discord.emoji import Emoji
from ....discord.guild import Guild
from ....discord.message import Message
from ....discord.invite import Invite

from ...command_utils import Pagination, Closer
from ..content_parser import DEFAULT_TYPE_NONE, RestParserContext, SingleArgsParserContext, ChainedArgsParserContext, \
    SingleParserContext, ChainedParserContext, timedelta, relativedelta

MAX_LINE_PER_PAGE = 24
DEFAULT_PREFIX = '**>>**'

ARGUMENT_REQUIRED_START = '<'
ARGUMENT_REQUIRED_END = '>'
ARGUMENT_OPTIONAL_START = '*'
ARGUMENT_OPTIONAL_END = '*'

ARGUMENT_NAME_REST = 'rest'

ARGUMENT_TYPE_TO_NAME = {
    UserBase : 'user',
    User : 'user',
    ChannelBase : 'channel',
    ChannelGuildBase : 'guild-channel',
    ChannelTextBase : 'any-text-channel',
    ChannelText : 'text-channel',
    ChannelPrivate : 'private-channel',
    ChannelVoice : 'voice-channel',
    ChannelGroup : 'group-channel',
    ChannelCategory : 'category-channel',
    ChannelStore : 'store-channel',
    ChannelThread : 'thread-channel',
    Invite : 'invite',
    Role : 'role',
    Guild : 'guild',
    Message : 'message',
    str : 'string',
    int : 'integer',
    timedelta : 'time-delta',
    Emoji : 'emoji',
        }

if (relativedelta is not None):
    ARGUMENT_TYPE_TO_NAME[relativedelta] = 'relative-time-delta'

ARGUMENT_UNDEFINED = 'undefined'

DEFAULT_HELP_NAME = 'help'

ARGUMENT_SEPARATOR_SPACE_AFTER_ONLY = {
    ',',
    ':',
    ';',
        }

COLOR_GETTER_TYPE_STATIC = 0
COLOR_GETTER_TYPE_CALLABLE = 1

def check_user(user, event):
    """
    Checks whether the ``ReactionAddEvent`` or ``ReactionDeleteEvent`` instance's user is same as the given one.
    
    Parameters
    ----------
    user : ``User`` or ``Client``
        The user who should be matched.
    event : ``ReactionAddEvent`` or ``ReactionDeleteEvent``
        The reaction addition or deletion event.
    """
    return (event.user is user)

class ColorGetter:
    """
    Color getter of the ``SubterraneanHelpCommand``
    
    Attributes
    ----------
    getter : `None`, `color ` or `callable`
        The color itself or a callable, what supposed to return it. If given as a `callable`
    type : `int`
        A type-hint telling, whether ``.color`` is a color, or a callable returning it.
        
        Can be set as one of the following:
        
        +-------------------------------+-------+
        | Respective name               | Value |
        +===============================+=======+
        | COLOR_GETTER_TYPE_STATIC      | 0     |
        +-------------------------------+-------+
        | COLOR_GETTER_TYPE_CALLABLE    | 1     |
        +-------------------------------+-------+
    """
    __slots__ = ('getter', 'type',)
    def __new__(cls, color):
        """
        Creates a new ``ColorGetter`` instance with the given parameter.
        
        Attributes
        ----------
        color : `None`, `color ` or `callable`
            A color for the generated embeds by the respective help command.
        
        Raises
        ------
        TypeError
            If `color` was not given as `None`, `int`, neither as a `callable` accepting `3` parameters.
        ValueError
            If the `color` was given as `int` instance, but it's value is less than `0` or is over than `0xffffff`.
        """
        if color is None:
            getter = None
            type_ = COLOR_GETTER_TYPE_STATIC
        elif callable(color):
            analyzer = CallableAnalyzer(color)
            min_, max_ = analyzer.get_non_reserved_positional_argument_range()
            if min_ > 3:
                raise TypeError(f'A callable `color` should accept `3` arguments, `client, message, name`, meanwhile '
                    f'the given one expects at least `{min_!r}`, got `{color!r}`.')
            
            if (min_ != 3) and (max_ < 3) and (not analyzer.accepts_args()):
                raise TypeError(f'A callable `color` should accept `3` arguments, `client, message, name`, meanwhile '
                    f'the given one expects up to `{max_!r}`, got `{color!r}`.')
            
            getter = color
            type_ = COLOR_GETTER_TYPE_CALLABLE
        else:
            getter = preconvert_color(color)
            type_ = COLOR_GETTER_TYPE_STATIC
        
        self = object.__new__(cls)
        self.getter = getter
        self.type = type_
        return self
    
    async def __call__(self, client, message, name):
        """
        Calls the color getter returning a desired color for the respective message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who received the respective message.
        message : ``Message``
            The received message.
        name : `str`
            The respective command's or category's name.
        
        Returns
        -------
        color : `None`, ``Color`` or `int`
        """
        type_ = self.type
        getter = self.getter
        if type_ == COLOR_GETTER_TYPE_STATIC:
            color = getter
        elif type_ == COLOR_GETTER_TYPE_CALLABLE:
            color = getter(client, message, name)
            if is_awaitable(color):
                color = await color
        else:
            # should not happen
            color = None
        
        return color
    
    def __repr__(self):
        """Returns the color getter's representation."""
        return f'{self.__class__.__name__}({self.getter!r})'


class SubterraneanHelpHelp:
    """
    Shows the usage of help of a respective help command.
    
    Attributes
    ----------
    color_getter : ``ColorGetter``
        Color getter for the embed to generate.
    embed_postprocessor : `None` or `callable`
        An embed post-processor, what is called with the autogenerated embeds.
    """
    __slots__ = ('color_getter', 'embed_postprocessor')
    
    def __init__(self, parent):
        """
        Creates a new Subterranean help help instance.
        
        Attributes
        ----------
        parent : ``SubterraneanHelpCommand``
            The parent of the help helper.
        """
        self.color_getter = parent.color_getter
        self.embed_postprocessor = parent.embed_postprocessor
    
    async def __call__(self, client, message):
        """
        Returns the respective help command's generated help embed.
        
        Returns
        -------
        embed : ``Embed``
        """
        prefix = client.command_processer.get_prefix_for(message)
        if is_awaitable(prefix):
            prefix = await prefix
        
        color = await self.color_getter(client, message, DEFAULT_HELP_NAME)
        
        embed = Embed('help',
            'Shows the help command of the client.\n'
            f'Try `{prefix}help` for displaying the categories or the commands\' of them.',
            color = color)
        
        embed_postprocessor = self.embed_postprocessor
        if (embed_postprocessor is not None):
            embed_postprocessor(client, message, embed)
        
        return embed

class SubterraneanHelpCommand:
    __class_doc__ = (
    """
    A default help command shipped with hata's commands extension.
    
    Usage
    -----
    After you did setup your client, just add the command to your client.
    
    ```py
    from hata import Client
    from hata.ext.commands import setup_ext_commands
    from hata.ext.commands.helps.subterranean import SubterraneanHelpCommand
    
    Orin = Client('TOKEN')
    setup_ext_commands(Orin, 'o|')
    
    Orin.commands(SubterraneanHelpCommand(color=0xc90d00), 'help')
    
    Orin.start()
    ```
    
    ``SubterraneanHelpCommand`` allows you modifying it's embeds' colors, so do not forget to pass some cool colors
    when instancing it.
    
    If you wanna generate colors based on the respective messages, do not worry, we got you! You can also give color
    as an async or non-async function accepting 3 parameters:
    
    +-------------------+-------------------+
    | Respective name   | Parameter type    |
    +===================+===================+
    | client            | ``Client``        |
    +-------------------+-------------------+
    | message           | ``Message``       |
    +-------------------+-------------------+
    | name              | `str`             |
    +-------------------+-------------------+
    
    You can also add prefix in front of commands, when listing them. Just pass a `prefix` keyword argument as a string.
    
    If you want to modify each autogenerated embed, then we got you as well! There is an `embed_postprocessor`
    parameter just for this.
    
    The following 3 arguments are passed to it:
    
    +-------------------+-------------------+
    | Respective name   | Parameter type    |
    +===================+===================+
    | client            | ``Client``        |
    +-------------------+-------------------+
    | message           | ``Message``       |
    +-------------------+-------------------+
    | embed             | ``Embed``         |
    +-------------------+-------------------+
    
    Here is an other example using `callable` color and `embed_postprocessor`:
    ```py
    from hata import Client
    from hata.ext.commands import setup_ext_commands
    from hata.ext.commands.helps.subterranean import SubterraneanHelpCommand
    
    Orin = Client('TOKEN')
    setup_ext_commands(Orin, 'o|')
    
    
    def color_getter(client, message, name):
        if name == 'help':
            color = 0xffffff
        else:
            color = message.author.color_at(message.guild)
        
        return color
    
    def embed_postprocessor(client, message, embed):
        embed.add_thumbnail(client.avatar_url)
    
    Orin.commands(SubterraneanHelpCommand(color=color_getter, embed_postprocessor=embed_postprocessor), 'help')
    
    
    # Add a command as well to showcase
    @Orin.commands
    async def ping(client, message):
        await client.message_create(message.channel, 'pong')
    
    
    Orin.start()
    ```
    
    Note, that `embed_postprocessor` feature is only experimental for now.
    
    Attributes
    ----------
    color_getter : ``ColorGetter``
        A color getter for the generated embeds.
    embed_postprocessor : `None` or `callable`, Optional
        An embed post-processor, what is called with the autogenerated embeds.
    prefix : `str`
        Prefix inserted before commands's display name.
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
    
    __doc__ = doc_property()
    
    __slots__ = ('color_getter', 'embed_postprocessor', 'prefix')
    
    def __new__(cls, color=None, prefix=None, embed_postprocessor=None):
        """
        Creates a new ``SubterraneanHelpCommand`` instance.
        
        Parameters
        ----------
        color : `None`, ``Color``, `int`, `callable`, Optional
            A color for the generated embeds. If given as a `callable`, then `3` parameters will be passed to it:
            
            +-------------------+-------------------+
            | Respective name   | Parameter type    |
            +===================+===================+
            | client            | ``Client``        |
            +-------------------+-------------------+
            | message           | ``Message``       |
            +-------------------+-------------------+
            | name              | `str`             |
            +-------------------+-------------------+
            
            Async and not async callables are supported as well.
        
        prefix : `None`, `str`, Optional
            Prefix inserted before commands's display name.
        
        embed_postprocessor : `None` or `callable`, Optional
            An embed post-processor, what is called with the autogenerated embeds.
            
            `3` arguments are passed to it, which are the following:
            
            +-------------------+-------------------+
            | Respective name   | Parameter type    |
            +===================+===================+
            | client            | ``Client``        |
            +-------------------+-------------------+
            | message           | ``Message``       |
            +-------------------+-------------------+
            | embed             | ``Embed``         |
            +-------------------+-------------------+
        
        Raises
        ------
        TypeError
            If `color` was not given as `None`, `int`, neither as a `callable` accepting `3` parameters.
            If `embed_postprocessor` is given, but not as a `non-async` `callable` accepting `3` parameters.
        ValueError
            If the `color` was given as `int` instance, but it's value is less than `0` or is over than `0xffffff`.
        """
        color_getter = ColorGetter(color)
        
        if (embed_postprocessor is not None):
            analyzer = CallableAnalyzer(embed_postprocessor)
            min_, max_ = analyzer.get_non_reserved_positional_argument_range()
            if min_ > 3:
                raise TypeError(f'`embed_postprocessor` should accept `3` arguments: `client, message, embed`, '
                    f'meanwhile the given one expects at least `{min_!r}`, got `{embed_postprocessor!r}`.')
            
            if (min_ != 3) and (max_ < 3) and (not analyzer.accepts_args()):
                raise TypeError(f'`embed_postprocessor` should accept `3` arguments: `client, message, embed`, '
                    f'meanwhile the given one expects up to `{max_!r}`, got `{embed_postprocessor!r}`.')
            
            if analyzer.is_async():
                raise TypeError(f'`embed_postprocessor` cannot be async, got `{embed_postprocessor}`.')
        
        if prefix is None:
            prefix = DEFAULT_PREFIX
        else:
            prefix = preconvert_str(prefix, 'prefix', 1, 32)
        
        self = object.__new__(cls)
        self.color_getter = color_getter
        self.embed_postprocessor = embed_postprocessor
        self.prefix = prefix
        return self
    
    def __repr__(self):
        """Returns the help command's representation."""
        result = [
            self.__class__.__name__,
            '(',
                ]
        
        result.append('color_getter=')
        result.append(repr(self.color_getter))
        
        prefix = self.prefix
        if (prefix is not DEFAULT_PREFIX):
            result.append(', prefix=')
            result.append(repr(prefix))
        
        result.append(')')
        
        return ''.join(result)
    
    async def __call__(self, client, message, name=None):
        """
        Calls the subterranean help command.
        
        Parameters
        ----------
        client : ``Client``
            The client who received the respective message.
        message : ``Message``
            The received message.
        name : `str`, Optional
            Search term to lookup a category or a command.
        """
        if name is None:
            await self.list_categories(client, message)
            return
        
        if name.isdecimal() and len(name)<21: # do not convert longer names than 64 bit.
            await self.list_category_indexed(client, message, name)
        else:
            await self.lookup_by_name(client, message, name)
    
    async def lookup_by_name(self, client, message, name):
        """
        Tries to lookup a command, then a category with the given `name`.
        
        Parameters
        ----------
        client : ``Client``
            The client who received the respective message.
        message : ``Message``
            The received message.
        name : `str`
            Search term to lookup a category or a command.
        """
        name = name.lower()
        
        command_processer = client.command_processer
        try:
            command = command_processer.commands[name]
        except KeyError:
            category = command_processer.get_category(name)
            if (category is None) or (not await category.run_checks(client, message)):
                await self.command_not_found(client, message, name)
                return
            
            command_names = []
            for command in category.commands:
                if await command.run_checks(client, message):
                    command_names.append(command.display_name)
            
            if command_names:
                await self.list_commands(client, message, command_names, category.name)
            else:
                await self.command_not_found(client, message, name)
            return
        
        category = command.category
        if (await category.run_checks(client, message)) and (await command.run_checks(client, message)):
            await self.show_command(client, message, command)
        else:
            await self.command_not_found(client, message, name)
        
    async def show_command(self, client, message, command):
        """
        SHows the given command's description.
        
        Parameters
        ----------
        client : ``Client``
            The client who received the respective message.
        message : ``Message``
            The received message.
        command : ``Command``
            The respective command.
        """
        description = command.description
        if isinstance(description, str):
            await self.show_string_description(client, message, command.display_name, description)
            return
        
        if callable(description):
            embed = await description(client, message)
            embed_type = embed.__class__
            if embed_type is Embed:
                await Closer(client, message.channel, embed, check=partial_func(check_user, message.author))
                return
            
            if embed_type is list:
                await Pagination(client, message.channel, embed, check=partial_func(check_user, message.author))
                return
            
            # Is other embed type?
            if hasattr(embed_type, 'to_data'):
                await Closer(client, message.channel, embed, check=partial_func(check_user, message.author))
                return
            
            # Is other indexable sequence?
            if hasattr(embed_type, '__getitem__') and hasattr(embed_type, '__len__'):
                await Pagination(client, message.channel, embed, check=partial_func(check_user, message.author))
                return
            
            # No more case, go back to default
        
        await self.show_autogenerated_description(client, message, command)
    
    async def command_not_found(self, client, message, name):
        """
        Called, when no command or category was found with the given name,
        
        Parameters
        ----------
        client : ``Client``
            The client who received the respective message.
        message : ``Message``
            The received message.
        name : `str`
            The search word.
        """
        prefix = client.command_processer.get_prefix_for(message)
        if is_awaitable(prefix):
            prefix = await prefix
        
        color = await self.color_getter(client, message, DEFAULT_HELP_NAME)
        
        embed = Embed('Command not found.',
            f'There is no category or command named as: `{name}`.\n'
            f'Try using `{prefix}help`',
            color = color)
        
        embed_postprocessor = self.embed_postprocessor
        if (embed_postprocessor is not None):
            embed_postprocessor(client, message, embed)
        
        await Closer(client, message.channel, embed, check=partial_func(check_user, message.author))
    
    async def list_categories(self, client, message):
        """
        Lists the categories of the respective client's command preprocessor.
        
        Parameters
        ----------
        client : ``Client``
            The client who received the respective message.
        message : ``Message``
            The received message.
        """
        color = await self.color_getter(client, message, DEFAULT_HELP_NAME)
        categories = client.command_processer.categories
        if len(categories) == 1:
            category = categories[0]
            if await category.run_checks(client, message):
                await self.list_category(client, message, category, display_category_name=False)
                return
            
            pages = [Embed('Categories', '*[No available category]*', color=color)]
            
        else:
            # Collect all the categories to display.
            category_names = []
            for category in categories:
                if await category.run_checks(client, message):
                    for command in category.commands:
                        if await command.run_checks(client, message):
                            category_names.append(category.display_name)
                            break
            
            pages = []
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
        
        prefix = client.command_processer.get_prefix_for(message)
        if is_awaitable(prefix):
            prefix = await prefix
        
        field_name = f'Use `{prefix}help <category/command>` for more information.'
        
        embeds = [
            Embed('Categories', page, color=color).add_field(field_name, f'page {index}/{page_count}')
                for index, page in enumerate(pages, 1)]
        
        embed_postprocessor = self.embed_postprocessor
        if (embed_postprocessor is not None):
            for embed in embeds:
                embed_postprocessor(client, message, embed)
        
        await Pagination(client, message.channel, embeds, check=partial_func(check_user, message.author))
    
    async def list_category(self, client, message, category, display_category_name=True):
        """
        Lists the given commands.
        
        This command only collects the displayable commands' names, then calls ``.list_commands``.
        
        Parameters
        ----------
        client : ``Client``
            The client who received the respective message.
        message : ``Message``
            The received message.
        category : ``Category``
            The category, which' commands will be listed.
        display_category_name : `bool`, Optional
            Whether the display name of the given category should be displayed. Defaults to `True`.
        """
        command_names = []
        for command in category.commands:
            if await command.run_checks(client, message):
                command_names.append(command.display_name)
        
        if display_category_name:
            category_name = category.display_name
        else:
            category_name = None
        
        await self.list_commands(client, message, command_names, category_name)
    
    async def list_commands(self, client, message, command_names, category_name):
        """
        Lists the given commands.
        
        Parameters
        ----------
        client : ``Client``
            The client who received the respective message.
        message : ``Message``
            The received message.
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
        
        prefix = client.command_processer.get_prefix_for(message)
        if is_awaitable(prefix):
            prefix = await prefix
        
        field_name = f'Use `{prefix}help <command>` for more information.'
        
        if category_name is None:
            title = 'Commands'
            name = DEFAULT_HELP_NAME
        else:
            title = f'Commands of {category_name}'
            name = category_name
        
        color = await self.color_getter(client, message, name)
        
        embeds = [
            Embed(title, page, color=color).add_field(field_name, f'page {index}/{page_count}')
                for index, page in enumerate(pages, 1)]
        
        embed_postprocessor = self.embed_postprocessor
        if (embed_postprocessor is not None):
            for embed in embeds:
                embed_postprocessor(client, message, embed)
        
        await Pagination(client, message.channel, embeds, check=partial_func(check_user, message.author))
    
    
    async def list_category_indexed(self, client, message, name):
        """
        Tries to find the category with the given `name` (decimal only string) index value.
        
        If the represented index ends up out of bounds, calls ``.lookup_by_name``, if not, then ``.list_commands``.
        
        Parameters
        ----------
        client : ``Client``
            The client who received the respective message.
        message : ``Message``
            The received message.
        name : `str`
            Decimal only string, which might represent a category's index.
        """
        category_index = int(name)
        if category_index == 0:
            await self.lookup_by_name(client, message, name)
            return
        
        categories = iter(client.command_processer.categories)
        
        while category_index > 1:
            try:
                category = next(categories)
            except StopIteration:
                await self.lookup_by_name(client, message, name)
                return
            
            if not await category.run_checks(client, message):
                continue
            
            for command in category.commands:
                if await command.run_checks(client, message):
                    break
            else:
                continue
            
            category_index -=1
            continue
        
        
        while True:
            try:
                category = next(categories)
            except StopIteration:
                await self.lookup_by_name(client, message, name)
                return
            
            if not await category.run_checks(client, message):
                continue
            
            command_names = []
            for command in category.commands:
                if await command.run_checks(client, message):
                    command_names.append(command.display_name)
            
            if command_names:
                break
        
        
        await self.list_commands(client, message, command_names, category.display_name)
    
    
    async def show_string_description(self, client, message, command_name, description):
        """
        Shows the given string description.
        
        Parameters
        ----------
        client : ``Client``
            The client who received the respective message.
        message : ``Message``
            The received message.
        command_name : `str`
            The respective command's display name.
        description : `str`
            The respective command's description.
        """
        color = await self.color_getter(client, message, command_name)
        if len(description) < 2048:
            embed = Embed(command_name, description, color=color)
            
            embed_postprocessor = self.embed_postprocessor
            if (embed_postprocessor is not None):
                embed_postprocessor(client, message, embed)
            
            await Closer(client, message.channel, embed, check=partial_func(check_user, message.author))
        
        else:
            description_parts = chunkify(description.splitlines())
            embeds = [Embed(command_name, description_part, color=color) for description_part in description_parts]
            
            embed_postprocessor = self.embed_postprocessor
            if (embed_postprocessor is not None):
                for embed in embeds:
                    embed_postprocessor(client, message, embed)
            
            await Pagination(client, message.channel, embeds, check=partial_func(check_user, message.author))
    
    async def show_autogenerated_description(self, client, message, command):
        """
        Generates, then sends the description of the given description-less command.
        
        Parameters
        ----------
        client : ``Client``
            The client who received the respective message.
        message : ``Message``
            The received message.
        command : ``Command``
            The respective command.
        """
        prefix = client.command_processer.get_prefix_for(message)
        if is_awaitable(prefix):
            prefix = await prefix
        
        description_parts = ['Usage : `', str(prefix), command.display_name]
        
        command_arg_parser = command.parser
        if command_arg_parser is None:
            arg_parsers = None
        else:
            arg_parsers = command_arg_parser._parsers
            if (arg_parsers is not None):
                
                arg_separator = command_arg_parser._separator.separator
                if type(arg_separator) is str:
                    if arg_separator in ARGUMENT_SEPARATOR_SPACE_AFTER_ONLY:
                        separator = f'{arg_separator} '
                    else:
                        separator = f' {arg_separator} '
                else:
                    separator = ' '
                
                description_parts.append(' ')
                arg_parser_index = 0
                arg_parser_limit = len(arg_parsers)
                
                while True:
                    arg_parser = arg_parsers[arg_parser_index]
                    arg_parser_index += 1
                    
                    arg_parser_type = arg_parser.__class__
                    
                    if arg_parser_type is RestParserContext:
                        description_parts.append(ARGUMENT_OPTIONAL_START)
                        description_parts.append(ARGUMENT_NAME_REST)
                        description_parts.append(ARGUMENT_OPTIONAL_START)
                    
                    elif arg_parser_type is SingleArgsParserContext:
                        arg_name = ARGUMENT_TYPE_TO_NAME.get(arg_parser.type, ARGUMENT_UNDEFINED)
                        description_parts.append(ARGUMENT_OPTIONAL_START)
                        description_parts.append(arg_name)
                        description_parts.append('-1')
                        description_parts.append(ARGUMENT_OPTIONAL_END)
                        description_parts.append(' ')
                        description_parts.append(ARGUMENT_OPTIONAL_START)
                        description_parts.append(arg_name)
                        description_parts.append('-2')
                        description_parts.append(ARGUMENT_OPTIONAL_END)
                        description_parts.append(' ...')
                    
                    elif arg_parser_type is ChainedArgsParserContext:
                        arg_names = [
                            ARGUMENT_TYPE_TO_NAME.get(parser_context.type, ARGUMENT_UNDEFINED)
                                for parser_context in arg_parser.parser_contexts]
                        
                        arg_name_limit = len(arg_names)
                        
                        description_parts.append(ARGUMENT_OPTIONAL_START)
                        
                        arg_name_index = 0
                        while True:
                            arg_name = arg_names[arg_name_index]
                            arg_name_index += 1
                            
                            description_parts.append(arg_name)
                            description_parts.append('-1')
                            
                            if arg_name_index == arg_name_limit:
                                break
                            
                            description_parts.append('/')
                            continue
                        
                        description_parts.append(ARGUMENT_OPTIONAL_END)
                        description_parts.append(' ')
                        description_parts.append(ARGUMENT_OPTIONAL_START)
    
                        arg_name_index = 0
                        while True:
                            arg_name = arg_names[arg_name_index]
                            arg_name_index += 1
                            
                            description_parts.append(arg_name)
                            description_parts.append('-2')
                            
                            if arg_name_index == arg_name_limit:
                                break
                            
                            description_parts.append('/')
                            continue
                        
                        description_parts.append(ARGUMENT_OPTIONAL_END)
                        description_parts.append(' ...')
                    
                    elif arg_parser_type is SingleParserContext:
                        required = (arg_parser.default_type == DEFAULT_TYPE_NONE)
                        arg_name = ARGUMENT_TYPE_TO_NAME.get(arg_parser.type, ARGUMENT_UNDEFINED)
                        
                        description_parts.append(ARGUMENT_REQUIRED_START if required else ARGUMENT_OPTIONAL_START)
                        description_parts.append(arg_name)
                        description_parts.append(ARGUMENT_REQUIRED_END if required else ARGUMENT_OPTIONAL_END)
                    
                    elif arg_parser_type is ChainedParserContext:
                        required = (arg_parser.default_type == DEFAULT_TYPE_NONE)
                        arg_names = [
                            ARGUMENT_TYPE_TO_NAME.get(parser_context.type, ARGUMENT_UNDEFINED)
                                for parser_context in arg_parser.parser_contexts]
                        
                        description_parts.append(ARGUMENT_REQUIRED_START if required else ARGUMENT_OPTIONAL_START)
                        
                        arg_name_limit = len(arg_names)
                        arg_name_index = 0
                        while True:
                            arg_name = arg_names[arg_name_index]
                            arg_name_index += 1
                            
                            description_parts.append(arg_name)
                            
                            if arg_name_index == arg_name_limit:
                                break
                            
                            description_parts.append('/')
                            continue
                        
                        description_parts.append(ARGUMENT_REQUIRED_END if required else ARGUMENT_OPTIONAL_END)
                    
                    # No more case
                    
                    if arg_parser_index == arg_parser_limit:
                        break
                    
                    description_parts.append(separator)
                    continue
                    
        description_parts.append('`')
        
        
        if (arg_parsers is not None) and (type(arg_parsers[0]) is not RestParserContext) \
                and (type(arg_separator) is tuple):
            
            description_parts.append('\nNote, that you can encapsulate more words inside of `')
            separator_starter, separator_ender = arg_separator
            description_parts.append(separator_starter)
            if separator_starter != separator_ender:
                description_parts.append('`, `')
                description_parts.append(separator_ender)
            description_parts.append('` characters.')
        
        
        aliases = command.aliases
        if (aliases is not None):
            description_parts.append('\nAliases: ')
            
            alias_limit = len(aliases)
            alias_index = 0
            while True:
                alias = aliases[alias_index]
                alias_index += 1
                
                description_parts.append('`')
                description_parts.append(alias)
                description_parts.append('`')
                
                if alias_index == alias_limit:
                    break
                
                description_parts.append(', ')
                continue
        
        color = await self.color_getter(client, message, command.name)
        
        embed = Embed(command.display_name, ''.join(description_parts), color=color)
        
        embed_postprocessor = self.embed_postprocessor
        if (embed_postprocessor is not None):
            embed_postprocessor(client, message, embed)
        
        await Closer(client, message.channel, embed, check=partial_func(check_user, message.author))
