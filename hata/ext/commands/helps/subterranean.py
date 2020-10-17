# -*- coding: utf-8 -*-
__all__ = ('SubterraneanHelpCommand', )

from ....backend.dereaddons_local import DOCS_ENABLED, DocProperty
from ....backend.futures import isawaitable
from ....discord.embed import Embed
from ....discord.others import chunkify
from ....discord.preconverters import preconvert_color, preconvert_str
from ....discord.user import UserBase, User
from ....discord.channel import ChannelBase, ChannelGuildBase, ChannelTextBase, ChannelText, ChannelPrivate, \
    ChannelVoice, ChannelGroup, ChannelCategory, ChannelStore, ChannelThread
from ....discord.role import Role
from ....discord.emoji import Emoji
from ....discord.guild import Guild
from ....discord.message import Message
from ....discord.invite import Invite

from ..utils import Pagination, Closer
from ..content_parser import DEFAULT_TYPE_NONE, RestParserContext, SingleArgsParserContext, ChainedArgsParserContext, \
    SingleParserContext, ChainedParserContext, timedelta, relativedelta

MAX_LINE_PER_PAGE = 24
DEFAULT_PREFIX = '**>>**'

ARGUMENT_REQUIRD_START = '<'
ARGUMENT_REQUIRD_END = '>'
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
        }

if (relativedelta is not None):
    ARGUMENT_TYPE_TO_NAME[relativedelta] = 'relative-time-delta'

ARGUMENT_UNDEFINED = 'undefined'

ARGUMENT_SEPARATOR_SPACE_AFTER_ONLY = {
    ',',
    ':',
    ';',
        }

class SubterraneanHelpHelp(object):
    """
    Shows the usage of help of a respective help command.
    
    Attributes
    ----------
    color : ``Color``
        The color of the generated embed.
    """
    __slots__ = ('color',)
    
    def __init__(self, parent):
        """
        Creates a new Subterranean help help instance.
        
        Attributes
        ----------
        parent : ``SubterraneanHelpCommand``
            The parent of the help helper.
        """
        self.color = parent.color
    
    async def __call__(self, client, message):
        """
        Returns the respective help command's generated help embed.
        
        Returns
        -------
        embed : ``Embed``
        """
        prefix = client.command_processer.get_prefix_for(message)
        if isawaitable(prefix):
            prefix = await prefix
        
        return Embed('help',
            'Shows the help command of the client.\n'
            f'Try `{prefix}help` for displaying the categories or the commands of it.',
            color = self.color)


class SubterraneanHelpCommand(object):
    __class_doc__ = (
    """
    A default help command shipped with hata's commands extension.
    
    Usage
    -----
    After you did setup your client, just add the command to your client.
    
    ```
    from hata import Client
    from hata.ext.commands import setup_ext_commands
    from hata.ext.commands.helps.subterranean import SubterraneanHelpCommand
    
    Orin = Client('TOKEN')
    setup_ext_commands(Orin, 'o|')
    
    Orin.commands(SubterraneanHelpCommand(0xc90d00), 'help')
    
    Orin.start()
    ```
    
    ``SubterraneanHelpCommand`` allows you modifying it's embeds' colors, so do not forget to pass some cool colors
    when instancing it.
    
    
    Attributes
    ----------
    color : `None` or ``Color``
        A color for the generated embeds.
    prefix : `str`
        Prefix inserted before commands's display name.
    """ ) if DOCS_ENABLED else None
    
    @property
    def __instance_doc__(self):
        """
        Returns the help of the help for the help command.
        
        Returns
        -------
        helphelp : ``SubterraneanHelpHelp``
        """
        return SubterraneanHelpHelp(self)
    
    __doc__ = DocProperty()
    
    __slots__ = ('color', 'prefix')
    
    def __new__(cls, color=None, prefix=None):
        """
        Creates a new ``SubterraneanHelpCommand`` instance.
        
        Parameters
        ----------
        color : `None`, `int`, ``Color``, Optional
            A color for the generated embeds.
        prefix : `None` or `str`, Optional
            Prefix inserted before commands's display name.
        
        Raises
        ------
        TypeError
            If `color` was not given as `None` or as `int` instance.
        ValueError
            If the `color` was given as `int` instance, but it's value is less than `0` or is over than `0xffffff`.
        """
        if (color is not None):
            color = preconvert_color(color)
        
        if prefix is None:
            prefix = DEFAULT_PREFIX
        else:
            prefix = preconvert_str(prefix, 'prefix', 1, 32)
        
        self = object.__new__(cls)
        self.color = color
        self.prefix = prefix
        return self
    
    def __repr__(self):
        """Returns the help command's represnetation."""
        result = [
            self.__class__.__name__,
            '(',
                ]
        
        color = self.color
        if color is None:
            put_comma = False
        else:
            result.append('color=')
            result.append(repr(color))
            put_comma = True
        
        prefix = self.prefix
        if (prefix is not DEFAULT_PREFIX):
            if put_comma:
                result.append(', ')
            
            result.append('prefix=')
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
        name : `str`, Optoonmal
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
                await Closer(client, message.channel, embed)
                return
            
            if embed_type is list:
                await Pagination(client, message.channel, embed)
                return
            
            # Is other embed type?
            if hasattr(embed_type, 'to_data'):
                await Closer(client, message.channel, embed)
                return
            
            # Is other indexable sequence?
            if hasattr(embed_type, '__getitem__') and hasattr(embed_type, '__len__'):
                await Pagination(client, message.channel, embed)
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
        if isawaitable(prefix):
            prefix = await prefix
        
        embed = Embed('Command not found.',
            f'There is no category or command named as: `{name}`.\n'
            f'Try using `{prefix}help`',
            color = self.color)
        
        await Closer(client, message.channel, embed)
    
    async def list_categories(self, client, message):
        """
        Lists the categories of the respective client's command preocesser..
        
        Parameters
        ----------
        client : ``Client``
            The client who received the respective message.
        message : ``Message``
            The received message.
        """
        categories = client.command_processer.categories
        if len(categories) == 1:
            category = categories[0]
            if await category.run_checks(client, message):
                await self.list_category(client, message, category, display_categoiry_name=False)
                return
            
            pages = [Embed('Categories', '*[No available category]*', color=self.color)]
            
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
        if isawaitable(prefix):
            prefix = await prefix
        
        field_name = f'Use `{prefix}help <category/command>` for more information.'
        
        embeds = [
            Embed('Categories', page, color=self.color).add_field(field_name, f'page {index}/{page_count}')
                for index, page in enumerate(pages, 1)]
        
        await Pagination(client, message.channel, embeds)
    
    async def list_category(self, client, message, category, display_categoiry_name=True):
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
        display_categoiry_name : `bool`, Optional
            Whether the dispplay name of the given category should be displayed. Defaults to `True`.
        """
        command_names = []
        for command in category.commands:
            if await command.run_checks(client, message):
                command_names.append(command.display_name)
        
        if display_categoiry_name:
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
            The commnd's names to display.
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
        if isawaitable(prefix):
            prefix = await prefix
        
        field_name = f'Use `{prefix}help <command>` for more information.'
        
        if category_name is None:
            title = 'Commands'
        else:
            title = f'Commands of {category_name}'
        
        embeds = [
            Embed(title, page, color=self.color).add_field(field_name, f'page {index}/{page_count}')
                for index, page in enumerate(pages, 1)]
        
        await Pagination(client, message.channel, embeds)
    
    
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
        if len(description) < 2048:
            embed = Embed(command_name, description, color=self.color)
            await Closer(client, message.channel, embed)
            return
        
        description_parts = chunkify(description.splitlines())
        embeds = [Embed(command_name, description_part, color=self.color) for description_part in description_parts]
        await Pagination(client, message.channel, embeds)
    
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
        description_parts = ['Usage : `', command.display_name]
        
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
                    arg_parser_index +=1
                    
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
                            arg_name_index +=1
                            
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
                            arg_name_index +=1
                            
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
                        
                        description_parts.append(ARGUMENT_REQUIRD_START if required else ARGUMENT_OPTIONAL_START)
                        description_parts.append(arg_name)
                        description_parts.append(ARGUMENT_REQUIRD_END if required else ARGUMENT_OPTIONAL_END)
                    
                    elif arg_parser_type is ChainedParserContext:
                        required = (arg_parser.default_type == DEFAULT_TYPE_NONE)
                        arg_names = [
                            ARGUMENT_TYPE_TO_NAME.get(parser_context.type, ARGUMENT_UNDEFINED)
                                for parser_context in arg_parser.parser_contexts]
                        
                        description_parts.append(ARGUMENT_REQUIRD_START if required else ARGUMENT_OPTIONAL_START)
                        
                        arg_name_limit = len(arg_names)
                        arg_name_index = 0
                        while True:
                            arg_name = arg_names[arg_name_index]
                            arg_name_index +=1
                            
                            description_parts.append(arg_name)
                            
                            if arg_name_index == arg_name_limit:
                                break
                            
                            description_parts.append('/')
                            continue
                        
                        description_parts.append(ARGUMENT_REQUIRD_END if required else ARGUMENT_OPTIONAL_END)
                    
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
                alias_index +=1
                
                description_parts.append('`')
                description_parts.append(alias)
                description_parts.append('`')
                
                if alias_index == alias_limit:
                    break
                
                description_parts.append(', ')
                continue
        
        embed = Embed(command.display_name, ''.join(description_parts), color=self.color)
        await Closer(client, message.channel, embed)


del timedelta
del relativedelta
del UserBase
del User
del ChannelBase
del ChannelTextBase
del ChannelText
del ChannelPrivate
del ChannelVoice
del ChannelGroup
del ChannelCategory
del ChannelStore
del ChannelThread
del Role
del Emoji
del Guild
del Message
del Invite
del DOCS_ENABLED
del DocProperty
