# -*- coding: utf-8 -*-
__all__ = ('Converter', 'ConverterFlag', 'ContentParser', 'FlaggedAnnotation')

#TODO: ask python for GOTO already
import re
from datetime import timedelta

try:
    from dateutil.relativedelta import relativedelta
except ImportError:
    relativedelta = None

from ...env import CACHE_USER
from ...backend.utils import MethodLike, module_property, MethodType, FunctionType
from ...backend.analyzer import CallableAnalyzer

from ...discord.bases import FlagBase
from ...discord.utils import USER_MENTION_RP, ROLE_MENTION_RP, CHANNEL_MENTION_RP, ID_RP, INVITE_CODE_RP, parse_rdelta,\
    parse_tdelta, CHANNEL_MESSAGE_RP
from ...discord.client import Client
from ...discord.exceptions import DiscordException, ERROR_CODES
from ...discord.emoji import parse_emoji, Emoji
from ...discord.core import USERS, CHANNELS, ROLES, GUILDS, MESSAGES, CLIENTS, EMOJIS
from ...discord.message import Message
from ...discord.channel import ChannelBase, ChannelGuildBase, ChannelTextBase, ChannelText, ChannelPrivate, \
    ChannelVoice, ChannelGroup, ChannelCategory, ChannelStore, ChannelThread, ChannelDirectory
from ...discord.user import User, UserBase
from ...discord.role import Role
from ...discord.events.handling_helpers import check_parameter_count_and_convert
from ...discord.preconverters import preconvert_flag, preconvert_bool
from ...discord.guild import Guild
from ...discord.http import MESSAGE_JUMP_URL_RP, INVITE_URL_RP
from ...discord.invite import Invite
from ...discord.color import Color, parse_color

NUMERIC_CONVERSION_LIMIT = 100

CONTENT_ARGUMENT_SEPARATORS = {}

class ContentParameterSeparator:
    """
    Content parameter separator used inside of a ``ContentParserContext`` and stored by ``CommandContentParser``
    instances.
    
    Attributes
    ----------
    _caller : `function`
        The chosen function what is called when the separator s called.
        
        Can be 1 of:
        - ``._rule_single``
        - ``._rule_inter``
    _rp : `_sre.SRE_Pattern`
        The regex pattern what is passed and used by the caller.
    separator : `str` or `tuple` (`str`, `str`)
        The executed separator by the ``ContentParameterSeparator`` instance.
    """
    __slots__ = ('_caller', '_rp', 'separator', )
    
    def __new__(cls, separator):
        """
        Creates a new ``ContentParameterSeparator`` instance. If one already exists with the given parameters, returns
        that instead.
        
        Parameters
        ----------
        separator : `str`, `tuple` (`str`, `str`)
            The executed separator by the ``ContentParameterSeparator`` instance.
        
        Raises
        ------
        TypeError
            - If `separator` is not given as `None`, ``ContentParameterSeparator``, `str`, neither as `tuple` instance.
            - If `separator` was given as `tuple`, but it's element are not `str` instances.
        ValueError
            - If `separator` is given as `str`, but it's length is not 1.
            - If `separator` is given as `str`, but it is a space character.
            - If `separator` is given as `tuple`, but one of it's element's length is not 1.
            - If `separator` is given as `tuple`, but one of it's element's is a space character.
        """
        if separator is None:
            return DEFAULT_SEPARATOR
        
        separator_type = separator.__class__
        if separator_type is cls:
            return separator
        
        if separator_type is str:
            processed_separator = separator
        elif separator_type is tuple:
            processed_separator = list(separator)
        elif issubclass(separator_type, str):
            processed_separator = str(separator)
            separator_type = str
        elif issubclass(separator_type, tuple):
            processed_separator = list(separator)
            separator_type = tuple
        else:
            raise TypeError(f'`separator` should have be given as `str` or as `tuple` instance, got '
                f'{separator_type.__name__}.')
        
        if separator_type is str:
            if len(processed_separator) != 1:
                raise ValueError(f'`str` separator length can be only `1`, got {separator!r}.')
            
            if processed_separator.isspace():
                raise ValueError(f'`str` separator cannot be a space character`, meanwhile it is, got {separator!r}.')
            
            separator = processed_separator
        
        else:
            if len(processed_separator) != 2:
                raise ValueError(f'`tuple` separator length can be only `2`, got {separator!r}.')
            
            for index in range(2):
                element = processed_separator[index]
                
                element_type = element.__class__
                if element_type is str:
                    processed_element = element
                elif issubclass(element_type, str):
                    processed_element  = str(element)
                    processed_separator[index] = processed_element
                else:
                    raise TypeError(f'`tuple` separator\'s elements can be only `str` instances, meanwhile it\'s '
                        f'element under index `{index}` is type {element_type.__name__!r}.')
                
                if len(processed_element) != 1:
                    raise ValueError(f'`tuple` separator\'s elements can be only `str` with length of `1`, meanwhile '
                        f'it\'s element under index `{index}` is not, got {element!r}.')
                
                if processed_element.isspace():
                    raise ValueError(f'`tuple` separator\'s elements cannot be space character`, meanwhile it\'s '
                        f'element under index `{index}` is, got {element!r}.')
            
            separator = tuple(processed_separator)
        
        try:
            return CONTENT_ARGUMENT_SEPARATORS[separator]
        except KeyError:
            pass
        
        if separator_type is str:
            escaped = re.escape(separator)
            rp = re.compile(f'[^{escaped}\S]*(?:{escaped}[^{escaped}\S]*)+', re.M|re.S)
            caller = cls._rule_single
        
        else:
            start, end = separator
            if start == end:
                escaped = re.escape(start)
                rp = re.compile(f'(?:{escaped}(.+?){escaped}|(\S+))[^{escaped}\S]*', re.M|re.S)
            
            else:
                start_escaped = re.escape(start)
                end_escaped = re.escape(end)
                rp = re.compile(f'(?:{start_escaped}(.+?){end_escaped}|(\S+))[^{start_escaped}\S]*', re.M|re.S)
            
            caller = cls._rule_inter
        
        self = object.__new__(cls)
        self.separator = separator
        self._rp = rp
        self._caller = caller
        CONTENT_ARGUMENT_SEPARATORS[separator] = self
        return self
    
    @staticmethod
    def _rule_single(rp, content, index):
        """
        Rule used when the the content's part are separated by a given character.
        
        Parameters
        ----------
        rp : `_sre.SRE_Pattern`
            The regex pattern what looks for the next part in the given content.
        content : `str`
            The content what's next part we are going to be parsed.
        index : `int`
            The starter index of the content to parse from.
        
        Returns
        -------
        part : `str`
            The parsed out part.
        index : `int`
            The index where the next parsing should start from.
        """
        searched = rp.search(content, index)
        # never matches the end
        if searched is None:
            return content[index:], len(content)
        
        return content[index:searched.start()], searched.end()
    
    @staticmethod
    def _rule_inter(rp, content, index):
        """
        Rule used when the content's part are separated by a space or if they are between 2 (or 1) predefined
        character.
        
        Parameters
        ----------
        rp : `_sre.SRE_Pattern`
            The regex pattern what looks for the next part in the given content.
        content : `str`
            The content what's next part we are going to be parsed.
        index : `int`
            The starter index of the content to parse from.
        
        Returns
        -------
        part : `str`
            The parsed out part.
        index : `int`
            The index where the next parsing should start from.
        """
        parsed = rp.match(content, index)
        part = parsed.group(2)
        if part is None:
            part = parsed.group(1)
        
        return part, parsed.end()
    
    def __call__(self, content, index):
        """
        Calls the content parameter separator to get the next part of the given content.
        
        Parameters
        ----------
        content : `str`
            The content what's next part we are going to be parsed.
        index : `int`
            The starter index of the content to parse from.
        
        Returns
        -------
        part : `str`
            The parsed out part.
        index : `int`
            The index where the next parsing should start from.
        """
        return self._caller(self._rp, content, index)
    
    def __repr__(self):
        """Returns the content parameter separator's representation."""
        return f'{self.__class__.__name__}({self.separator!r})'
    
    def __hash__(self):
        """Returns the content parameter parser's hash."""
        return hash(self.separator)
    
    def __eq__(self, other):
        """Returns whether the two content parameter separator are the same."""
        if type(self) is not type(other):
            return NotImplemented
        
        return (self.separator == other.separator)


DEFAULT_SEPARATOR = ContentParameterSeparator(('"', '"'))

def parse_user_mention(part, message):
    """
    If the message's given part is a user mention, returns the respective user.
    
    Parameters
    ----------
    part : `str`
        A part of a message's content.
    message : ``Message``
        The respective message of the given content part.
    
    Returns
    -------
    user : `None` or ``UserBase`` instance
    """
    user_mentions = message.user_mentions
    if user_mentions is None:
        return
    
    parsed = USER_MENTION_RP.fullmatch(part)
    if parsed is None:
        return
    
    user_id = int(parsed.group(1))
    for user in user_mentions:
        if user.id == user_id:
            return user

def parse_role_mention(part, message):
    """
    If the message's given part is a role mention, returns the respective role.
    
    Parameters
    ----------
    part : `str`
        A part of a message's content.
    message : ``Message``
        The respective message of the given content part.
    
    Returns
    -------
    role : `None` or ``Role`` instance
    """
    role_mentions = message.role_mentions
    if role_mentions is None:
        return
    
    parsed = ROLE_MENTION_RP.fullmatch(part)
    if parsed is None:
        return

    role_id = int(parsed.group(1))
    for role in role_mentions:
        if role.id == role_id:
            return role

def parse_channel_mention(part, message):
    """
    If the message's given part is a channel mention, returns the respective channel.
    
    Parameters
    ----------
    part : `str`
        A part of a message's content.
    message : ``Message``
        The respective message of the given content part.
        
    Returns
    -------
    channel : `None` or ``ChannelBase`` instance
    """
    channel_mentions = message.channel_mentions
    if channel_mentions is None:
        return
    
    parsed = CHANNEL_MENTION_RP.fullmatch(part)
    if parsed is None:
        return

    channel_id = int(parsed.group(1))
    for channel in channel_mentions:
        if channel.id == channel_id:
            return channel


class ConverterFlag(FlagBase):
    """
    Flags for a converter to describe by which rules it should convert.
    
    +---------------+---------------+-----------------------------------------------------------------------+
    | Rule name     | Shift value   | Description                                                           |
    +===============+===============+=======================================================================+
    | url           | 0             | Whether the entity should be parsed from it's url.                    |
    +---------------+---------------+-----------------------------------------------------------------------+
    | mention       | 1             | Whether the entity should be parsed out from it's mention.            |
    +---------------+---------------+-----------------------------------------------------------------------+
    | name          | 2             | Whether the entity should be picked up by it's name.                  |
    +---------------+---------------+-----------------------------------------------------------------------+
    | id            | 3             | Whether the entity should be picked up by it's name.                  |
    +---------------+---------------+-----------------------------------------------------------------------+
    | everywhere    | 4             | Whether the entity should be searched out of the local scope.         |
    |               |               | Mostly pairs with the `id` flag.                                      |
    +---------------+---------------+-----------------------------------------------------------------------+
    | profile       | 5             | User parser only. Can be used when user cache is disabled to          |
    |               |               | ensure, that the user will have local guild profile if applicable.    |
    +---------------+---------------+-----------------------------------------------------------------------+
    
    There are already precreated flags, which are the following:
    +-------------------+-------------------------------------------+
    | Name              | Included flags                            |
    +===================+===========================================+
    | user_default      | mention, name, id                         |
    +-------------------+-------------------------------------------+
    | user_all          | mention, name, id, everywhere, profile    |
    +-------------------+-------------------------------------------+
    | client_default    | mention, name, id                         |
    +-------------------+-------------------------------------------+
    | client_all        | mention, name, id, everywhere             |
    +-------------------+-------------------------------------------+
    | role_default      | mention, name, id                         |
    +-------------------+-------------------------------------------+
    | role_all          | mention, name, id, everywhere             |
    +-------------------+-------------------------------------------+
    | channel_default   | mention, name, id                         |
    +-------------------+-------------------------------------------+
    | channel_all       | mention, name, id, everywhere             |
    +-------------------+-------------------------------------------+
    | emoji_default     | mention, name, id                         |
    +-------------------+-------------------------------------------+
    | emoji_all         | mention, name, id, everywhere             |
    +-------------------+-------------------------------------------+
    | guild_default     | id                                        |
    +-------------------+-------------------------------------------+
    | guild_all         | id, everywhere                            |
    +-------------------+-------------------------------------------+
    | message_default   | url, id                                   |
    +-------------------+-------------------------------------------+
    | message_all       | url, id, everywhere                       |
    +-------------------+-------------------------------------------+
    | invite_default    | url, id                                   |
    +-------------------+-------------------------------------------+
    | invite_all        | url, id                                   |
    +-------------------+-------------------------------------------+
    
    Note, if you use for example a `'user'` parser, then by default it will use the `user_default` flags, and it
    will ignore everything else, than `user_all`.
    
    Some events, like `int`, or `str` do not have any flags, what means, their behaviour cannot be altered.
    """
    __keys__ = {
        'url': 0,
        'mention': 1,
        'name': 2,
        'id': 3,
        'everywhere': 4,
        'profile': 5,
    }
    
    user_default = NotImplemented
    user_all = NotImplemented
    client_default = NotImplemented
    client_all = NotImplemented
    role_default = NotImplemented
    role_all = NotImplemented
    channel_default = NotImplemented
    channel_all = NotImplemented
    emoji_default = NotImplemented
    emoji_all = NotImplemented
    guild_default = NotImplemented
    guild_all = NotImplemented
    message_default = NotImplemented
    message_all = NotImplemented
    invite_default = NotImplemented
    invite_all = NotImplemented

ConverterFlag.user_default = ConverterFlag().update_by_keys(mention=True, name=True, id=True)
ConverterFlag.user_all = ConverterFlag.user_default.update_by_keys(everywhere=True, profile=True)
ConverterFlag.client_default = ConverterFlag().update_by_keys(mention=True, name=True, id=True)
ConverterFlag.client_all = ConverterFlag.client_default.update_by_keys(everywhere=True)
ConverterFlag.role_default = ConverterFlag().update_by_keys(mention=True, name=True, id=True)
ConverterFlag.role_all = ConverterFlag.role_default.update_by_keys(everywhere=True)
ConverterFlag.channel_default = ConverterFlag().update_by_keys(mention=True, name=True, id=True)
ConverterFlag.channel_all = ConverterFlag.channel_default.update_by_keys(everywhere=True)
ConverterFlag.emoji_default = ConverterFlag().update_by_keys(mention=True, name=True, id=True)
ConverterFlag.emoji_all = ConverterFlag.emoji_default.update_by_keys(everywhere=True)
ConverterFlag.guild_default = ConverterFlag().update_by_keys(id=True)
ConverterFlag.guild_all = ConverterFlag.guild_default.update_by_keys(everywhere=True)
ConverterFlag.message_default = ConverterFlag().update_by_keys(url=True, id=True)
ConverterFlag.message_all = ConverterFlag.message_default.update_by_keys(everywhere=True)
ConverterFlag.invite_default = ConverterFlag().update_by_keys(url=True, id=True)
ConverterFlag.invite_all = ConverterFlag.invite_default


CONVERTER_FLAG_URL = 1 << ConverterFlag.__keys__['url']
CONVERTER_FLAG_MENTION = 1 << ConverterFlag.__keys__['mention']
CONVERTER_FLAG_NAME = 1 << ConverterFlag.__keys__['name']
CONVERTER_FLAG_ID = 1 << ConverterFlag.__keys__['id']
CONVERTER_FLAG_EVERYWHERE = 1 << ConverterFlag.__keys__['everywhere']
CONVERTER_FLAG_PROFILE = 1 << ConverterFlag.__keys__['profile']

class ContentParserContext:
    """
    Content parser instance context used when parsing a message's content.
    
    Attributes
    ----------
    client : ``Client``
        The respective client.
    content : `str`
        A message's content after it's prefix.
    index : `int`
        The index, of the last character's end.
    last_part : `None` or `str`
        The last parsed part.
    last_start : `bool`
        When the last returned string started
    length : `int`
        The length of the string to parse.
    message : ``Message``
        The respective message.
    result : `list` of `Any`
        The successfully parsed objects.
    separator : ``ContentParameterSeparator``
        The parameter separator of the parser.
    """
    __slots__ = ('client', 'content', 'index', 'last_part', 'last_start', 'length', 'message', 'result', 'separator', )
    
    def __init__(self, separator, client, message, content):
        """
        Creates a new ``ContentParserContext`` instance.
        
        Parameters
        ----------
        separator : ``ContentParameterSeparator``
            The parameter separator of the parser.
        client : ``Client``
            The respective client.
        message : ``Message``
            The respective message.
        content : `str`
            A message's content after it's prefix.
        """
        self.separator = separator
        self.client = client
        self.message = message
        self.index = 0
        self.length = len(content)
        self.content = content
        self.last_part = None
        self.last_start = 0
        self.result = []
    
    def get_next(self):
        """
        Gets the next string part from a respective message's content.
        
        Returns
        -------
        next_ : `None` or `str`
            Returns `None` if the message has no more parts left.
        """
        index = self.index
        length = self.length
        if index == length:
            if self.last_start == index:
                part = None
            else:
                part = self.last_part
        else:
            part, self.index = self.separator(self.content, index)
            self.last_part = part
            self.last_start = index
        
        return part
    
    def mark_last_as_used(self):
        """
        Marks the lastly returned string as it was used up, making the next call to try to parse a
        new one.
        """
        self.last_start = self.index
    
    def get_rest(self):
        """
        Returns the not yet used string part of ``.content``.
        
        Returns
        -------
        rest : `str`
            Might be empty string.
        """
        last_start = self.last_start
        rest = self.content
        if last_start:
            rest = rest[last_start:]
        
        return rest

DEFAULT_TYPE_NONE = 0
DEFAULT_TYPE_OBJ = 1
DEFAULT_TYPE_CALL = 2
DEFAULT_TYPE_NAMES = ('DEFAULT_TYPE_NONE', 'DEFAULT_TYPE_OBJ', 'DEFAULT_TYPE_CALL', )

class ParserContextBase:
    """
    Base class for parser contexts.
    """
    __slots__ = ()
    
    async def __call__(self, content_parser_ctx):
        """
        Calls the ``ParserContextBase`` with the given content parser context.
        
        This method is a coroutine.
        
        Parameters
        ----------
        content_parser_ctx : ``ContentParserContext``
            The content parser context in which the conversion is executed.
            
        Returns
        -------
        passed : `bool`
            Whether parsing out the variable was successful.
        """
        return True
    
    def __repr__(self):
        """Returns the parser context's representation."""
        return f'<{self.__class__.__name__}>'

class RestParserContext(ParserContextBase):
    """
    Parser context used when getting rest value.
    
    Attributes
    ----------
    default : `Any`
        The default object to return if the parser fails.
    default_type : `int`
        Describes how `default` is used up.
        
        Possible values:
        +-----------------------+-------+
        | Respective name       | Value |
        +=======================+=======+
        | DEFAULT_TYPE_NONE     | 0     |
        +-----------------------+-------+
        | DEFAULT_TYPE_OBJ      | 1     |
        +-----------------------+-------+
        | DEFAULT_TYPE_CALL     | 2     |
        +-----------------------+-------+
    """
    __slots__ = ('default', 'default_type')
    
    def __new__(cls, default_type, default):
        """
        Creates a new parser context instance with the given parameters.
        
        Parameters
        ----------
        default_type : `Any`
            Describes how `default` is used up.
            
            Possible values:
            +-----------------------+-------+
            | Respective name       | Value |
            +=======================+=======+
            | DEFAULT_TYPE_NONE     | 0     |
            +-----------------------+-------+
            | DEFAULT_TYPE_OBJ      | 1     |
            +-----------------------+-------+
            | DEFAULT_TYPE_CALL     | 2     |
            +-----------------------+-------+
        default : `Any`
            The default object to return if the parser fails
        """
        self = object.__new__(cls)
        self.default_type = default_type
        self.default = default
        return self
    
    async def __call__(self, content_parser_ctx):
        """
        Calls the ``RestParserContext`` with the given content parser context.
        
        This method is a coroutine.
        
        Parameters
        ----------
        content_parser_ctx : ``ContentParserContext``
            The content parser context in which the conversion is executed.
        
        Returns
        -------
        passed : `bool`
            Whether parsing out the variable was successful.
        """
        result = content_parser_ctx.get_rest()
        if (not result):
            default_type = self.default_type
            if default_type:
                result = self.default
                if default_type == DEFAULT_TYPE_CALL:
                    result = await result(self, content_parser_ctx)
        
        content_parser_ctx.result.append(result)
        return True
    
    def __repr__(self):
        """Returns the parser context's representation."""
        result = [
            '<',
            self.__class__.__name__,
        ]
        
        default_type = self.default_type
        if default_type:
            result.append(' default_type=')
            result.append(repr(default_type))
            result.append(' (')
            result.append(DEFAULT_TYPE_NAMES[default_type])
            result.append('), default=')
            result.append(repr(self.default))
        
        result.append('>')
        
        return ''.join(result)

class ParserContext(ParserContextBase):
    """
    Parser context used inside of chained content events.
    
    Attributes
    ----------
    converter : `async-callable`
        A function, what converts a part of the a respective message's content.
    flags : ``ConverterFlag``
        Flags which describe what details should the parser function check.
    type : `None` or `type`
        Type info about the entity to parse.
    """
    __slots__ = ('converter', 'flags', 'type')
    
    def __new__(cls, flagged_annotation):
        """
        Creates a new parser context instance with the given parameters.
        
        Parameters
        ----------
        flagged_annotation : ``FlaggedAnnotation``
            Describes what type of entity and how it should be parsed.
        
        Raises
        ------
        TypeError
            If `flagged_annotation` was given as `tuple`.
        """
        type_ = flagged_annotation.annotation
        if type(type_) is tuple:
            raise TypeError(f'`flagged_annotation` cannot be given as `tuple`, when creating a `{cls.__name__}` '
                f'instance, got {flagged_annotation!r}.')
        
        self = object.__new__(cls)
        self.flags = flagged_annotation.flags
        self.type = type_
        self.converter = CONVERTER_SETTING_TYPE_RELATION_MAP[type_].converter
        return self
    
    async def __call__(self, content_parser_ctx):
        """
        Calls the ``ParserContext`` with the given content parser context.
        
        This method is a coroutine.
        
        Parameters
        ----------
        content_parser_ctx : ``ContentParserContext``
            The content parser context in which the conversion is executed.
            
        Returns
        -------
        passed : `bool`
            Whether parsing out the variable was successful.
        """
        result = await self.converter(self, content_parser_ctx)
        if result is None:
            return False
        
        content_parser_ctx.mark_last_as_used()
        content_parser_ctx.result.append(result)
        return True
    
    def __repr__(self):
        """Returns the parser context's representation."""
        result = [
            '<',
            self.__class__.__name__,
            ' converter=',
            self.converter.__name__,
            ' type=',
        ]
        
        type_ = self.type
        if (type_ is None):
            result.append('None')
        else:
            result.append(type_.__name__)
        
        flags = self.flags
        if flags:
            result.append(', flags=')
            result.append(int.__repr__(flags))
        
        result.append('>')
        
        return ''.join(result)

class SingleArgsParserContext(ParserContext):
    """
    Parser context used to parse *args.
    
    Attributes
    ----------
    converter : `async-callable`
        A function, what converts a part of the a respective message's content.
    flags : ``ConverterFlag``
        Flags which describe what details should the parser function check.
    type : `None` or `type`
        Type info about the entity to parse.
    """
    __slots__ = ()
    
    async def __call__(self, content_parser_ctx):
        """
        Calls the ``ArgsParserContext`` with the given content parser context.
        
        This method is a coroutine.
        
        Parameters
        ----------
        content_parser_ctx : ``ContentParserContext``
            The content parser context in which the conversion is executed.
            
        Returns
        -------
        passed : `bool`
            Whether parsing out the variable was successful.
        """
        while True:
            result = await self.converter(self, content_parser_ctx)
            if result is None:
                break
            
            content_parser_ctx.mark_last_as_used()
            content_parser_ctx.result.append(result)
        
        return True

class ChainedArgsParserContext(ParserContextBase):
    """
    A chained converter *args used, when parts can represent more types.
    
    Attributes
    ----------
    parser_contexts : `tuple` of `ParserContext`
        The chained converters.
    """
    __slots__ = ('parser_contexts', )
    
    def __new__(cls, flagged_annotations):
        """
        Creates a new parser context instance with the given parameters.
        
        Parameters
        ----------
        flagged_annotations : `tuple` of ``FlaggedAnnotation``
            Describes what type of entity and how it should be parsed.
        
        Raises
        ------
        TypeError
            If `flagged_annotation` was given not given as `tuple` or it contains only 1 (or less) element.
        """
        if (type(flagged_annotations) is not tuple) or (len(flagged_annotations) < 2):
            raise TypeError(f'`flagged_annotations` cannot be given as not `tuple`, or as `tuple` with 1 (or less) '
                f'elements, when creating a `{cls.__name__}` instance, got {flagged_annotations!r}.')
        
        parser_contexts = []
        for flagged_annotation in flagged_annotations:
            parser_context = ParserContext(flagged_annotation)
            parser_contexts.append(parser_context)
        
        self = object.__new__(cls)
        self.parser_contexts = parser_contexts
        return self
    
    async def __call__(self, content_parser_ctx):
        """
        Calls the ``ChainedArgsParserContext`` with the given content parser context.
        
        This method is a coroutine.
        
        Parameters
        ----------
        content_parser_ctx : ``ContentParserContext``
            The content parser context in which the conversion is executed.
        
        Returns
        -------
        passed : `bool`
            Whether parsing out the variable was successful.
        """
        parser_contexts = self.parser_contexts
        while True:
            for parser_context in parser_contexts:
                result = await parser_context.converter(parser_context, content_parser_ctx)
                if (result is not None):
                    content_parser_ctx.mark_last_as_used()
                    content_parser_ctx.result.append(result)
                    break
            else:
                break
        
        return True
    
    def __repr__(self):
        """Returns the parser context's representation."""
        result = [
            '<',
            self.__class__.__name__,
            ' parser_contexts=[',
        ]
        
        parser_contexts = self.parser_contexts
        index = 0
        limit = len(parser_contexts)
        while True:
            parser_context = parser_contexts[index]
            index +=1
            
            result.append(repr(parser_context))
            
            if index == limit:
                break
            
            result.append(', ')
            continue
        
        result.append(']>')
        
        return ''.join(result)


class SingleParserContext(ParserContext):
    """
    Parser context used inside of a content parser.
    
    Attributes
    ----------
    converter : `async-callable`
        A function, what converts a part of the a respective message's content.
    flags : ``ConverterFlag``
        Flags which describe what details should the parser function check.
    type : `None` or `type_`
        Type info about the entity to parse.
    default : `Any`
        The default object to return if the parser fails
    default_type : `int`
        Describes how `default` is used up.
        
        Possible values:
        +-----------------------+-------+
        | Respective name       | Value |
        +=======================+=======+
        | DEFAULT_TYPE_NONE     | 0     |
        +-----------------------+-------+
        | DEFAULT_TYPE_OBJ      | 1     |
        +-----------------------+-------+
        | DEFAULT_TYPE_CALL     | 2     |
        +-----------------------+-------+
    """
    __slots__ = ('default', 'default_type')
    
    def __new__(cls, flagged_annotation, default_type, default):
        """
        Creates a new parser context instance with the given parameters.
        
        Parameters
        ----------
        flagged_annotation : ``FlaggedAnnotation``
            Describes what type on entity and how it should be parsed.
        default_type : `Any`
            Describes how `default` is used up.
            
            Possible values:
            +-----------------------+-------+
            | Respective name       | Value |
            +=======================+=======+
            | DEFAULT_TYPE_NONE     | 0     |
            +-----------------------+-------+
            | DEFAULT_TYPE_OBJ      | 1     |
            +-----------------------+-------+
            | DEFAULT_TYPE_CALL     | 2     |
            +-----------------------+-------+
        default : `Any`
            The default object to return if the parser fails
        
        Raises
        ------
        TypeError
            If `flagged_annotation` was given as `tuple`.
        """
        type_ = flagged_annotation.annotation
        if type(type_) is tuple:
            raise TypeError(f'`flagged_annotation` cannot be given as `tuple`, when creating a `{cls.__name__}` '
                f'instance, got {flagged_annotation!r}.')
        
        self = object.__new__(cls)
        self.flags = flagged_annotation.flags
        self.type = type_
        self.default_type = default_type
        self.default = default
        self.converter = CONVERTER_SETTING_TYPE_RELATION_MAP[type_].converter
        return self
    
    async def __call__(self, content_parser_ctx):
        """
        Calls the ``SingleParserContext`` with the given content parser context.
        
        This method is a coroutine.
        
        Parameters
        ----------
        content_parser_ctx : ``ContentParserContext``
            The content parser context in which the conversion is executed.
        
        Returns
        -------
        passed : `bool`
            Whether parsing out the variable was successful.
        """
        result = await self.converter(self, content_parser_ctx)
        if (result is not None):
            content_parser_ctx.mark_last_as_used()
            content_parser_ctx.result.append(result)
            return True
        
        default_type = self.default_type
        if default_type == DEFAULT_TYPE_NONE:
            return False
        
        default = self.default
        if default_type == DEFAULT_TYPE_CALL:
            default = await default(content_parser_ctx)
        
        content_parser_ctx.result.append(default)
        return True

    def __repr__(self):
        """Returns the parser context's representation."""
        result = [
            '<',
            self.__class__.__name__,
            ' type=',
        ]
        
        type_ = self.type
        if (type_ is None):
            result.append('None')
        else:
            result.append(type_.__name__)
        
        flags = self.flags
        if flags:
            result.append(', flags=')
            result.append(int.__repr__(flags))
            
            add_comma = True
        else:
            add_comma = False
        
        default_type = self.default_type
        if default_type:
            if add_comma:
                result.append(',')
            
            result.append(' default_type=')
            result.append(repr(default_type))
            result.append(' (')
            result.append(DEFAULT_TYPE_NAMES[default_type])
            result.append('), default=')
            result.append(repr(self.default))
        
        result.append('>')
        
        return ''.join(result)


class ChainedParserContext(ChainedArgsParserContext):
    """
    A chained converter used, when a single part can represent more types.
    
    Attributes
    ----------
    parser_contexts : `tuple` of `ParserContext`
        The chained converters.
    default : `Any`
        The default object to return if the parser fails
    default_type : `int`
        Describes how `default` is used up.
        
        Possible values:
        +-----------------------+-------+
        | Respective name       | Value |
        +=======================+=======+
        | DEFAULT_TYPE_NONE     | 0     |
        +-----------------------+-------+
        | DEFAULT_TYPE_OBJ      | 1     |
        +-----------------------+-------+
        | DEFAULT_TYPE_CALL     | 2     |
        +-----------------------+-------+
    """
    __slots__ = ('default', 'default_type')
    
    def __new__(cls, flagged_annotations, default_type, default):
        """
        Creates a new chained converter.
        
        Parameters
        ----------
        flagged_annotations : `tuple` of ``FlaggedAnnotation``
            Describes what type of entity and how it should be parsed.
        default : `Any`
            The default object to return if the parser fails
        default_type : `int`
            Describes how `default` is used up.
            
            Possible values:
            +-----------------------+-------+
            | Respective name       | Value |
            +=======================+=======+
            | DEFAULT_TYPE_NONE     | 0     |
            +-----------------------+-------+
            | DEFAULT_TYPE_OBJ      | 1     |
            +-----------------------+-------+
            | DEFAULT_TYPE_CALL     | 2     |
            +-----------------------+-------+
        
        Raises
        ------
        TypeError
            If `flagged_annotation` was given not given as `tuple` or it contains only 1 (or less) element.
        """
        if (type(flagged_annotations) is not tuple) or (len(flagged_annotations) < 2):
            raise TypeError(f'`flagged_annotations` cannot be given as not `tuple`, or as `tuple` with 1 (or less) '
                f'elements, when creating a `{cls.__name__}` instance, got {flagged_annotations!r}.')
        
        parser_contexts = []
        for flagged_annotation in flagged_annotations:
            parser_context = ParserContext(flagged_annotation)
            parser_contexts.append(parser_context)
        
        self = object.__new__(cls)
        self.parser_contexts = parser_contexts
        self.default = default
        self.default_type = default_type
        return self
    
    async def __call__(self, content_parser_ctx):
        """
        Calls the ``ChainedParserContext`` with the given content parser context.
        
        This method is a coroutine.
        
        Parameters
        ----------
        content_parser_ctx : ``ContentParserContext``
            The content parser context in which the conversion is executed.
        
        Returns
        -------
        passed : `bool`
            Whether parsing out the variable was successful.
        """
        for parser_context in self.parser_contexts:
            result = await parser_context.converter(parser_context, content_parser_ctx)
            if (result is not None):
                content_parser_ctx.mark_last_as_used()
                content_parser_ctx.result.append(result)
                return True
        
        default_type = self.default_type
        if default_type == DEFAULT_TYPE_NONE:
            return False
        
        default = self.default
        if default_type == DEFAULT_TYPE_CALL:
            default = await default(content_parser_ctx)
        
        content_parser_ctx.result.append(default)
        return True

    def __repr__(self):
        """Returns the parser context's representation."""
        result = [
            '<',
            self.__class__.__name__,
            ' parser_contexts=[',
        ]
        
        parser_contexts = self.parser_contexts
        index = 0
        limit = len(parser_contexts)
        while True:
            parser_context = parser_contexts[index]
            index +=1
            
            result.append(repr(parser_context))
            
            if index == limit:
                break
            
            result.append(', ')
            continue
        
        result.append(']')
        
        default_type = self.default_type
        if default_type:
            result.append(', default_type=')
            result.append(repr(default_type))
            result.append(' (')
            result.append(DEFAULT_TYPE_NAMES[default_type])
            result.append('), default=')
            result.append(repr(self.default))
        
        result.append('>')
        
        return ''.join(result)


CONVERTER_SETTING_TYPE_RELATION_MAP = {}
CONVERTER_SETTING_NAME_TO_TYPE = {}

class ConverterSetting:
    """
    Store settings about a converter.
    
    Attributes
    ----------
    all_flags : ``ConverterFlag``
        All the flags which the converter picks up.
    alternative_type_name : `None` or `str`
        Alternative string name for the parser, what allows picking up a respective converter.
    alternative_types : `None` or `list` of `type` instances
        Alternative type specifications, which are supported by the parser.
    converter : `async-function`
        The converter function.
    default_flags : ``ConverterFlag``
        The default flags with what the converter will be used if not defining any specific.
    default_type : `None` or `type`
        The default annotation type of the converter.
    uses_flags : `bool`
        Whether the converter processes any flags.
    """
    __slots__ = ('all_flags', 'alternative_type_name', 'alternative_types', 'converter', 'default_flags',
        'default_type', 'uses_flags')
    
    def __new__(cls, converter, uses_flags, default_flags, all_flags, alternative_type_name, default_type,
            alternative_types):
        """
        Creates a new ``ConverterSetting`` instance to store settings related to a converter function.
        
        Parameters
        ----------
        converter : `function` (async)
            The converter function.
        uses_flags : `bool`
            Whether the converter processes any flags.
        default_flags : ``ConverterFlag``
            The default flags with what the converter will be used if not defining any specific.
        all_flags : ``ConverterFlag``
             All the flags which the converter picks up.
        alternative_type_name : `None` or `str`
            Alternative string name for the parser, what allows picking up a respective converter.
        default_type : `None` or `type`
            The default annotation type of the converter.
        alternative_types : `None` `iterable` of `type`
            A list of the alternatively accepted types.
        
        Raises
        -------
        TypeError
            - If `converter` is not `function` type.
            - If `converter` is not `async`.
            - If `converter` accepts bad amount of parameters.
            - If `uses_flags` was not given as `bool`, nether as `int` as `0` or `1`.
            - If `default_flags` or `all_flags` was not given as `ConverterFlag` instance.
            - If `alternative_type_name` was not given as `None`, neither as `str` instance.
            - If `default_type` was not given as `None`, neither as `type` instance.
            - If `alternative_types` was not given as `None`, neither as `iterable` of `type`.
        ValueError
            If `uses_flags` is given as `true`, but at the same time `all_flags` was not given as
            `ConverterFlag(0)`
        """
        converter_type = converter.__class__
        if (converter_type is not FunctionType):
            raise TypeError(f'`converter` should have been given as `{FunctionType.__name__}` instance, got '
                f'{converter_type.__name__}.')
        
        analyzed = CallableAnalyzer(converter)
        if (not analyzed.is_async()):
            raise TypeError(f'`converter` should have been given as an async function instance, got '
                f'{converter!r}.')
        
        non_reserved_positional_parameter_count = analyzed.get_non_reserved_positional_parameter_count()
        if non_reserved_positional_parameter_count != 2:
            raise TypeError(f'`converter` should accept `2` non reserved positional parameters, meanwhile it expects '
                f'{non_reserved_positional_parameter_count}.')
        
        if analyzed.accepts_args():
            raise TypeError(f'`converter` should accept not expect args, meanwhile it does.')
        
        if analyzed.accepts_kwargs():
            raise TypeError(f'`converter` should accept not expect kwargs, meanwhile it does.')
        
        non_default_keyword_only_parameter_count = analyzed.get_non_default_keyword_only_parameter_count()
        if non_default_keyword_only_parameter_count:
            raise TypeError(f'`converter` should accept `0` keyword only parameters, meanwhile it expects '
                f'{non_default_keyword_only_parameter_count}.')
        
        uses_flags_type = uses_flags.__class__
        if uses_flags_type is bool:
            pass
        elif issubclass(uses_flags_type, int):
            if uses_flags in (0, 1):
                uses_flags = bool(uses_flags)
            else:
                raise TypeError(f'`uses_flags` was given as `int` instance, but not as `0`, or `1`, got '
                    f'{uses_flags_type.__name__}. Next time please pass a `bool` instance.')
        else:
            raise TypeError(f'`uses_flags` should have been given as `bool` instance, got {uses_flags_type.__name__}.')
        
        default_flags_type = default_flags.__class__
        if default_flags_type is not ConverterFlag:
            raise TypeError(f'`default_flags` should have be given as `{ConverterFlag.__name__}` instance, got '
                f'{default_flags_type.__name__}.')
        
        all_flags_type = all_flags.__class__
        if all_flags_type is not ConverterFlag:
            raise TypeError(f'`all_flags` should have be given as `{ConverterFlag.__name__}` instance, got '
                f'{all_flags_type.__name__}.')
        
        if (alternative_type_name is not None):
            alternative_type_name_type = alternative_type_name.__class__
            if alternative_type_name_type is str:
                pass
            elif issubclass(alternative_type_name_type, str):
                alternative_type_name = str(alternative_type_name)
            else:
                raise TypeError(f'`alternative_type_name` should have be given as `None` or as `str` instance, got '
                    f'{alternative_type_name_type.__class__}.')
        
        if (default_type is not None) and (not isinstance(default_type, type)):
            raise TypeError(f'`default_type` was not given as `None`, neither as `type` instance, got '
                f'{default_type.__class__.__name__}.')
        
        if (alternative_types is None):
            alternative_types_processed = None
        
        else:
            alternative_types_type = alternative_types.__class__
            if not hasattr(alternative_types_type, '__iter__'):
                raise TypeError(f'`alternative_types` can be given as `None` or as `iterable` of `type`, got '
                    f'{alternative_types_type.__name__}.')
            
            alternative_types_processed = []
            
            index = 1
            for alternative_type in alternative_types:
                if not isinstance(alternative_type, type):
                    raise TypeError(f'`alternative_types` can be given as `None`, or as `iterable` of `type`, got '
                        f'`iterable`, but it\'s {index} element is {alternative_type.__class__.__name__}.')
                
                alternative_types_processed.append(alternative_type)
                index +=1
            
            if not alternative_types_processed:
                 alternative_types_processed = None
        
        if (not uses_flags) and all_flags:
            raise ValueError(f'If `uses_flags` is given as `true`, then `all_flags` should be given as '
                f'`{ConverterFlag.__name__}(0)`, got {all_flags!r}.')
        
        self = object.__new__(cls)
        self.converter = converter
        self.uses_flags = uses_flags
        self.default_flags = default_flags
        self.all_flags = all_flags
        self.alternative_type_name = alternative_type_name
        self.default_type = default_type
        self.alternative_types = alternative_types_processed
        
        if (default_type is not None):
            CONVERTER_SETTING_TYPE_RELATION_MAP[default_type] = self
            CONVERTER_SETTING_NAME_TO_TYPE[default_type.__name__] = default_type
        
        if (alternative_type_name is not None):
            CONVERTER_SETTING_NAME_TO_TYPE[alternative_type_name] = default_type
        
        if (alternative_types_processed is not None):
            for alternative_type in alternative_types_processed:
                CONVERTER_SETTING_TYPE_RELATION_MAP[alternative_type] = self
                CONVERTER_SETTING_NAME_TO_TYPE[alternative_type.__name__] = alternative_type
    
    def __repr__(self):
        """Returns the converter setting's representation."""
        result = [
            '<',
            self.__class__.__name__,
            ' converter=',
            self.converter.__name__,
        ]
        
        default_type = self.default_type
        if default_type is None:
            alternative_type_name = self.alternative_type_name
            if (alternative_type_name is not None):
                result.append(', alternative_type_name=')
                result.append(repr(alternative_type_name))
        else:
            default_type_name = default_type.__name__
            result.append(', default_type=')
            result.append(default_type_name)
            
            alternative_type_name = self.alternative_type_name
            if alternative_type_name != default_type_name:
                result.append(', alternative_type_name=')
                result.append(repr(alternative_type_name))
            
            alternative_types = self.alternative_types
            if (alternative_types is not None):
                result.append(', alternative_types=[')
                
                index = 0
                limit = len(alternative_types)
                while True:
                    alternative_type_= alternative_types[index]
                    index +=1
                    
                    result.append(alternative_type_.__name__)
                    
                    if index == limit:
                        break
                    
                    result.append(', ')
                    continue
                
                result.append(']')
        
        if self.uses_flags:
            default_flags = self.default_flags
            result.append(', default_flags=')
            result.append(int.__repr__(default_flags))
            
            all_flags = self.all_flags
            if default_flags != all_flags:
                result.append(', all_flags=')
                result.append(int.__repr__(all_flags))
        
        result.append('>')
        return ''.join(result)


if CACHE_USER:
    async def user_converter(parser_ctx, content_parser_ctx):
        part = content_parser_ctx.get_next()
        if (part is None):
            return None
        
        flags = parser_ctx.flags
        message = content_parser_ctx.message
        
        if flags&CONVERTER_FLAG_ID:
            parsed = ID_RP.fullmatch(part)
            if (parsed is not None):
                id_ = int(parsed.group(1))
                
                if flags&CONVERTER_FLAG_EVERYWHERE:
                    try:
                        user = USERS[id_]
                    except KeyError:
                        try:
                            user = await content_parser_ctx.client.user_get(id_)
                        except BaseException as err:
                            if not (isinstance(err, ConnectionError) or
                                isinstance(err, DiscordException) and err.code in (
                                    ERROR_CODES.unknown_user,
                                    ERROR_CODES.unknown_member,
                                        )):
                                    raise
                        else:
                            return user
                    else:
                        return user
                
                else:
                    channel = message.channel
                    guild = message.guild
                    if guild is None:
                        if (not isinstance(channel, ChannelGuildBase)):
                            for user in channel.users:
                                if user.id == id_:
                                    return user
                    
                    else:
                        try:
                            user = guild.users[id_]
                        except KeyError:
                            pass
                        else:
                            return user
        
        if flags&CONVERTER_FLAG_MENTION:
            user = parse_user_mention(part, message)
            if (user is not None):
                return user
        
        if flags&CONVERTER_FLAG_NAME:
            channel = message.channel
            guild = channel.guild
            if (guild is None):
                if isinstance(channel, ChannelGuildBase):
                    user = None
                else:
                    user = channel.get_user_like(part)
            else:
                user = guild.get_user_like(part)
            
            if (user is not None):
                return user
        
        return None
else:
    async def user_converter(parser_ctx, content_parser_ctx):
        part = content_parser_ctx.get_next()
        if (part is None):
            return None
        
        flags = parser_ctx.flags
        message = content_parser_ctx.message
        
        if flags&CONVERTER_FLAG_ID:
            parsed = ID_RP.fullmatch(part)
            if (parsed is not None):
                id_ = int(parsed.group(1))
                
                if flags&CONVERTER_FLAG_EVERYWHERE:
                    if flags&CONVERTER_FLAG_PROFILE:
                        guild = message.guild
                        if (guild is not None):
                            try:
                                user = await content_parser_ctx.client.guild_user_get(guild, id_)
                            except BaseException as err:
                                if not (isinstance(err, ConnectionError) or
                                    isinstance(err, DiscordException) and err.code in (
                                        ERROR_CODES.unknown_user,
                                        ERROR_CODES.unknown_member,
                                            )):
                                        raise
                            else:
                                return user
                    
                    try:
                        user = await content_parser_ctx.client.user_get(id_)
                    except BaseException as err:
                        if not (isinstance(err, ConnectionError) or
                            isinstance(err, DiscordException) and err.code in (
                                ERROR_CODES.unknown_user,
                                ERROR_CODES.unknown_member,
                                    )):
                                raise
                    else:
                        return user
                
                else:
                    channel = message.channel
                    guild = message.guild
                    if guild is None:
                        if (not isinstance(channel, ChannelGuildBase)):
                            for user in channel.users:
                                if user.id == id_:
                                    return user
                    
                    else:
                        try:
                            user = await content_parser_ctx.client.guild_user_get(guild, id_)
                        except BaseException as err:
                            if not (isinstance(err, ConnectionError) or
                                isinstance(err, DiscordException) and err.code in (
                                    ERROR_CODES.unknown_user,
                                    ERROR_CODES.unknown_member,
                                        )):
                                    raise
                        else:
                            return user
        
        if flags&CONVERTER_FLAG_MENTION:
            user = parse_user_mention(part, message)
            if (user is not None):
                return user
        
        if flags&CONVERTER_FLAG_NAME:
            channel = message.channel
            guild = channel.guild
            if (guild is None):
                if (not isinstance(channel, ChannelGuildBase)):
                    user = channel.get_user_like(part)
                    if (user is not None):
                        return user
            
            else:
                try:
                    user = await content_parser_ctx.client.guild_user_search(guild, part)
                except BaseException as err:
                    if not (isinstance(err, ConnectionError) or
                        isinstance(err, DiscordException) and err.code in (
                            ERROR_CODES.unknown_user,
                            ERROR_CODES.unknown_member,
                                )):
                            raise
                else:
                    return user
        
        return None

ConverterSetting(
    converter = user_converter,
    uses_flags = True,
    default_flags = ConverterFlag.user_default,
    all_flags = ConverterFlag.user_all,
    alternative_type_name = 'user',
    default_type = User,
    alternative_types = [
        UserBase,
    ],
)

async def client_converter(parser_ctx, content_parser_ctx):
    part = content_parser_ctx.get_next()
    if (part is None):
        return None
    
    flags = parser_ctx.flags
    message = content_parser_ctx.message
    
    if flags&CONVERTER_FLAG_ID:
        parsed = ID_RP.fullmatch(part)
        if (parsed is not None):
            id_ = int(parsed.group(1))
            
            try:
                client = CLIENTS[id_]
            except KeyError:
                pass
            else:
                if flags&CONVERTER_FLAG_EVERYWHERE:
                    return client
                
                else:
                    if client in message.channel.clients:
                        return client
    
    if flags&CONVERTER_FLAG_MENTION:
        client = parse_user_mention(part, message)
        if (client is not None) and isinstance(client, Client):
            return client
    
    if flags&CONVERTER_FLAG_NAME:
        if flags&CONVERTER_FLAG_EVERYWHERE:
            clients = list(CLIENTS.values())
        else:
            clients = message.channel.clients
        
        if 1 < len(part) < 38:
            if len(part) > 6 and part[-5] == '#':
                try:
                    discriminator = int(part[-4:])
                except ValueError:
                    pass
                else:
                    name_ = part[:-5]
                    for client in clients:
                        if (client.discriminator == discriminator) and (client.name == name_):
                            return client
            
            if len(part) < 32:
                pattern = re.compile(re.escape(part), re.I)
                for client in clients:
                    if (pattern.match(client.name) is not None):
                        return client
                
                guild = message.guild
                if (guild is not None):
                    for client in clients:
                        try:
                            guild_profile = client.guild_profiles[guild.id]
                        except KeyError:
                            continue
                        
                        nick = guild_profile.nick
                        
                        if nick is None:
                            continue
                        
                        if pattern.match(nick) is None:
                            continue
                        
                        return client
    
    return None
    
ConverterSetting(
    converter = client_converter,
    uses_flags = True,
    default_flags = ConverterFlag.client_default,
    all_flags = ConverterFlag.client_all,
    alternative_type_name = 'client',
    default_type = Client,
    alternative_types = None,
)

async def channel_converter(parser_ctx, content_parser_ctx):
    part = content_parser_ctx.get_next()
    if (part is None):
        return None
    
    flags = parser_ctx.flags
    channel_type = parser_ctx.type
    message = content_parser_ctx.message
    
    if flags&CONVERTER_FLAG_ID:
        parsed = ID_RP.fullmatch(part)
        if (parsed is not None):
            id_ = int(parsed.group(1))
            
            if flags&CONVERTER_FLAG_EVERYWHERE:
                try:
                    channel = CHANNELS[id_]
                except KeyError:
                    pass
                else:
                    if ((channel_type is None) or isinstance(channel, channel_type)):
                        return channel
            
            else:
                channel = message.channel
                guild = message.guild
                if guild is None:
                    if ((channel_type is None) or isinstance(channel, channel_type)) and channel.id == id_:
                        return channel
                
                else:
                    try:
                        channel = guild.channels[id_]
                    except KeyError:
                        pass
                    else:
                        if ((channel_type is None) or isinstance(channel, channel_type)):
                            return channel
    
    if flags&CONVERTER_FLAG_MENTION:
        channel = parse_channel_mention(part, message)
        if (channel is not None):
            if ((channel_type is None) or isinstance(channel, channel_type)):
                return channel
    
    if flags&CONVERTER_FLAG_NAME:
        channel = message.channel
        guild = channel.guild
        if guild is None:
            if ((channel_type is None) or isinstance(channel, channel_type)) and channel.has_name_like(part):
                return channel
        else:
            channel = guild.get_channel_like(part, type_=channel_type)
            if (channel is not None):
                return channel
    
    return None

ConverterSetting(
    converter = channel_converter,
    uses_flags = True,
    default_flags = ConverterFlag.channel_default,
    all_flags = ConverterFlag.channel_all,
    alternative_type_name = 'channel',
    default_type = ChannelBase,
    alternative_types = [
        ChannelGuildBase,
        ChannelTextBase,
        ChannelText,
        ChannelPrivate,
        ChannelVoice,
        ChannelGroup,
        ChannelCategory,
        ChannelStore,
        ChannelThread,
        ChannelDirectory,
    ],
)

async def role_converter(parser_ctx, content_parser_ctx):
    part = content_parser_ctx.get_next()
    if (part is None):
        return None
    
    flags = parser_ctx.flags
    message = content_parser_ctx.message
    
    if flags&CONVERTER_FLAG_ID:
        parsed = ID_RP.fullmatch(part)
        if (parsed is not None):
            id_ = int(parsed.group(1))
            
            if flags&CONVERTER_FLAG_EVERYWHERE:
                try:
                    role = ROLES[id_]
                except KeyError:
                    pass
                else:
                    return role
            
            else:
                guild = message.guild
                if (guild is not None):
                    try:
                        role = guild.roles[id_]
                    except KeyError:
                        pass
                    else:
                        return role
    
    if flags&CONVERTER_FLAG_MENTION:
        role = parse_role_mention(part, message)
        if (role is not None):
            return role
    
    if flags&CONVERTER_FLAG_NAME:
        guild = message.guild
        if (guild is not None):
            role = guild.get_role_like(part)
            if (role is not None):
                return role
    
    return None

ConverterSetting(
    converter = role_converter,
    uses_flags = True,
    default_flags = ConverterFlag.role_default,
    all_flags = ConverterFlag.role_all,
    alternative_type_name = 'role',
    default_type = Role,
    alternative_types = None,
)

async def emoji_converter(parser_ctx, content_parser_ctx):
    part = content_parser_ctx.get_next()
    if (part is None):
        return None
    
    flags = parser_ctx.flags
    if flags&CONVERTER_FLAG_MENTION:
        emoji = parse_emoji(part)
        if (emoji is not None):
            return emoji
    
    message = content_parser_ctx.message
    if flags&CONVERTER_FLAG_ID:
        parsed = ID_RP.fullmatch(part)
        if (parsed is not None):
            id_ = int(parsed.group(1))
            
            if flags&CONVERTER_FLAG_EVERYWHERE:
                try:
                    emoji = EMOJIS[id_]
                except KeyError:
                    pass
                else:
                    return emoji
            
            else:
                guild = message.guild
                if (guild is not None):
                    try:
                        emoji = guild.emojis[id_]
                    except KeyError:
                        pass
                    else:
                        return emoji
    
    if flags&CONVERTER_FLAG_NAME:
        guild = message.guild
        if (guild is not None):
            emoji = guild.get_emoji_like(part)
            if (emoji is not None):
                return emoji
    
    return None

ConverterSetting(
    converter = emoji_converter,
    uses_flags = True,
    default_flags = ConverterFlag.emoji_default,
    all_flags = ConverterFlag.emoji_all,
    alternative_type_name = 'emoji',
    default_type = Emoji,
    alternative_types = None,
)

async def guild_converter(parser_ctx, content_parser_ctx):
    part = content_parser_ctx.get_next()
    if (part is None):
        return None
    
    parsed = ID_RP.fullmatch(part)
    if (parsed is None):
        return None
    
    id_ = int(parsed.group(1))
    
    try:
        guild = GUILDS[id_]
    except KeyError:
        return None
    
    if parser_ctx.flags&CONVERTER_FLAG_EVERYWHERE:
        return guild
    
    if guild in content_parser_ctx.client.guild_profiles:
        return guild
    
    return None

ConverterSetting(
    converter = guild_converter,
    uses_flags = True,
    default_flags = ConverterFlag.guild_default,
    all_flags = ConverterFlag.guild_all,
    alternative_type_name = 'guild',
    default_type = Guild,
    alternative_types = None,
)

# Gets a message by it's id
async def _message_converter_m_id(parser_ctx, content_parser_ctx, message_id):
    message = MESSAGES.get(message_id, None)
    channel = content_parser_ctx.message.channel
    if (message is not None):
        # Message found
        if parser_ctx.flags&CONVERTER_FLAG_EVERYWHERE:
            return message
        else:
            # Only local message can be yielded, so check if it is local
            guild = channel.guild
            if guild is None:
                if message.channel is channel:
                    return message
                else:
                    # Message found, but other channel, yield None
                    return None
            else:
                if message.guild is guild:
                    return message
                else:
                    # Message found, but other guild, yield None
                    return None
    
    # Try to get message by id
    client = content_parser_ctx.client
    if channel.cached_permissions_for(client).can_read_message_history:
        try:
            message = await client.message_get(channel, message_id)
        except BaseException as err:
            if not (isinstance(err, ConnectionError) or
                isinstance(err, DiscordException) and err.code in (
                    ERROR_CODES.unknown_channel, # message deleted
                    ERROR_CODES.unknown_message, # channel deleted
                    ERROR_CODES.missing_access, # client removed
                    ERROR_CODES.missing_permissions, # permissions changed meanwhile
                        )):
                    raise
            
            # Message do not exists at the respective channel, or any other acceptable error
            return None
        else:
            return message
    else:
        # The message is given by id, but the client request it.
        return None

# Gets a message by it's and it's channel's id
async def _message_converter_cm_id(parser_ctx, content_parser_ctx, channel_id, message_id):
    channel = content_parser_ctx.message.channel
    message = MESSAGES.get(message_id, None)
    if (message is not None):
        # Message found
        if parser_ctx.flags&CONVERTER_FLAG_EVERYWHERE:
            return message
        else:
            # Only local message can be yielded, so check if it is local
            guild = channel.guild
            if (message.channel is channel) if (guild is None) else (message.guild is guild):
                return message
        
        # Message found, but other guild or channel yield None
        return None
    
    message_channel = CHANNELS.get(channel_id, None)
    if (message_channel is None):
        return None

    if parser_ctx.flags&CONVERTER_FLAG_EVERYWHERE:
        # Lets use that multi client core
        for client in message_channel.clients:
            if message_channel.cached_permissions_for(client).can_read_message_history:
                try:
                    message = await client.message_get(message_channel,  message_id)
                except BaseException as err:
                    if isinstance(err, ConnectionError):
                        return None
                    
                    if isinstance(err, DiscordException):
                        err_code = err.code
                        # If the message or channel is deleted, return None
                        if err_code in (
                            ERROR_CODES.unknown_channel, # message deleted
                            ERROR_CODES.unknown_message, # channel deleted
                                ):
                            return None
                        
                        # If client is removed or has it's permissions changed, lets move on the next if applicable
                        if err_code in (
                            ERROR_CODES.missing_access, # client removed
                            ERROR_CODES.missing_permissions, # permissions changed meanwhile
                                ):
                            continue
                    
                    raise
                else:
                    return message
        
        # No message could be requested successfully.
        return None
    
    guild = channel.guild
    if (message_channel is channel) if (guild is None) else (message_channel.guild is guild):
        client = content_parser_ctx.client
        if channel.cached_permissions_for(client).can_read_message_history:
            try:
                message = await client.message_get(message_channel, message_id)
            except BaseException as err:
                if not (isinstance(err, ConnectionError) or
                    isinstance(err, DiscordException) and err.code in (
                        ERROR_CODES.unknown_channel, # message deleted
                        ERROR_CODES.unknown_message, # channel deleted
                        ERROR_CODES.missing_access, # client removed
                        ERROR_CODES.missing_permissions, # permissions changed meanwhile
                            )):
                        raise
            else:
                return message
        
        return None

async def message_converter(parser_ctx, content_parser_ctx):
    part = content_parser_ctx.get_next()
    if (part is None):
        return None
    
    if parser_ctx.flags&CONVERTER_FLAG_ID:
        parsed = ID_RP.fullmatch(part)
        if (parsed is not None):
            message_id = int(parsed.group(1))
            return await _message_converter_m_id(parser_ctx, content_parser_ctx, message_id)
        
        parsed = CHANNEL_MESSAGE_RP.fullmatch(part)
        if (parsed is not None):
            channel_id, message_id = parsed.groups()
            channel_id = int(channel_id)
            message_id = int(message_id)
            return await _message_converter_cm_id(parser_ctx, content_parser_ctx, channel_id, message_id)
    
    if parser_ctx.flags&CONVERTER_FLAG_URL:
        parsed = MESSAGE_JUMP_URL_RP.fullmatch(part)
        if (parsed is not None):
            _, channel_id, message_id = parsed.groups()
            channel_id = int(channel_id)
            message_id = int(message_id)
            return await _message_converter_cm_id(parser_ctx, content_parser_ctx, channel_id, message_id)
    
    return None

ConverterSetting(
    converter = message_converter,
    uses_flags = True,
    default_flags = ConverterFlag.message_default,
    all_flags = ConverterFlag.message_all,
    alternative_type_name = 'message',
    default_type = Message,
    alternative_types = None,
        )

async def invite_converter(parser_ctx, content_parser_ctx):
    part = content_parser_ctx.get_next()
    if (part is None):
        return None
    
    flags = parser_ctx.flags
    
    # It would not be a Huyane code without some GOTO
    while True:
        if flags&CONVERTER_FLAG_URL:
            parsed = INVITE_URL_RP.fullmatch(part)
            if parsed is not None:
                break
        
        if flags&CONVERTER_FLAG_ID:
            parsed = INVITE_CODE_RP.fullmatch(part)
            if (parsed is not None):
                break
        
        return None
    
    code = parsed.group(1)
    
    try:
        invite = await content_parser_ctx.client.invite_get(code)
    except BaseException as err:
        if not (isinstance(err, ConnectionError) or
            isinstance(err, DiscordException) and err.code == ERROR_CODES.unknown_invite # Invite not exists
                    ):
                raise
        
        return None
    
    return invite

ConverterSetting(
    converter = invite_converter,
    uses_flags = True,
    default_flags = ConverterFlag.invite_default,
    all_flags = ConverterFlag.invite_all,
    alternative_type_name = 'invite',
    default_type = Invite,
    alternative_types = None,
)


async def color_converter(parser_ctx, content_parser_ctx):
    part = content_parser_ctx.get_next()
    if (part is None):
        return None
    
    return parse_color(part)

ConverterSetting(
    converter = color_converter,
    uses_flags = False,
    default_flags = ConverterFlag(),
    all_flags = ConverterFlag(),
    alternative_type_name = 'color',
    default_type = Color,
    alternative_types = None,
)


async def str_converter(parser_ctx, content_parser_ctx):
    return content_parser_ctx.get_next()

ConverterSetting(
    converter = str_converter,
    uses_flags = False,
    default_flags = ConverterFlag(),
    all_flags = ConverterFlag(),
    alternative_type_name = None,
    default_type = str,
    alternative_types = None,
)


async def int_converter(parser_ctx, content_parser_ctx):
    part = content_parser_ctx.get_next()
    if part is None:
        return None
    
    if len(part)>NUMERIC_CONVERSION_LIMIT:
        return None
    
    try:
        int_ = int(part)
    except ValueError:
        int_ = None
    
    return int_

ConverterSetting(
    converter = int_converter,
    uses_flags = False,
    default_flags = ConverterFlag(),
    all_flags = ConverterFlag(),
    alternative_type_name = None,
    default_type = int,
    alternative_types = None,
)

async def tdelta_converter(parser_ctx, content_parser_ctx):
    part = content_parser_ctx.get_next()
    if part is None:
        return None
    
    return parse_tdelta(part)

ConverterSetting(
    converter = tdelta_converter,
    uses_flags = False,
    default_flags = ConverterFlag(),
    all_flags = ConverterFlag(),
    alternative_type_name = 'tdelta',
    default_type = timedelta,
    alternative_types = None,
)

if (relativedelta is not None):
    async def rdelta_converter(parser_ctx, content_parser_ctx):
        part = content_parser_ctx.get_next()
        if part is None:
            return None
        
        return parse_rdelta(part)

    ConverterSetting(
        converter = rdelta_converter,
        uses_flags = False,
        default_flags = ConverterFlag(),
        all_flags = ConverterFlag(),
        alternative_type_name = 'rdelta',
        default_type = relativedelta,
        alternative_types = None,
    )

else:
    rdelta_converter = None

# preregistered default code codes for shortcutting

PREREGISTERED_DEFAULT_CODES = {}

async def prdc_ma(content_parser_ctx):
    return content_parser_ctx.message.author

PREREGISTERED_DEFAULT_CODES['message.author'] = prdc_ma
del prdc_ma

async def prdc_mc(content_parser_ctx):
    return content_parser_ctx.message.channel

PREREGISTERED_DEFAULT_CODES['message.channel'] = prdc_mc
del prdc_mc

async def prdc_mg(content_parser_ctx):
    return content_parser_ctx.message.guild

PREREGISTERED_DEFAULT_CODES['message.guild'] = prdc_mg
PREREGISTERED_DEFAULT_CODES['message.channel.guild'] = prdc_mg
del prdc_mg

async def prdc_c(content_parser_ctx):
    return content_parser_ctx.client

PREREGISTERED_DEFAULT_CODES['client'] = prdc_c
del prdc_c

async def prdc_rest(content_parser_ctx):
    return content_parser_ctx.get_rest()

PREREGISTERED_DEFAULT_CODES['rest'] = prdc_rest
del prdc_rest

async def prdc_mgr(content_parser_ctx):
    guild = content_parser_ctx.message.guild
    if guild is None:
        return None
    
    return guild.default_role

PREREGISTERED_DEFAULT_CODES['message.guild.default_role'] = prdc_mgr
PREREGISTERED_DEFAULT_CODES['message.guild.default_role'] = prdc_mgr
del prdc_mgr

def validate_default_code(default_code):
    """
    Validates the given `default-code`.
    
    Parameters
    ----------
    default_code : `str` or `async-callable` `function`
        A default code function, or a `str` representing a predefined one.
    
    Returns
    -------
    default_code : `async-callable` `function`
    
    Raises
    ------
    LookupError
        If `default_code` is given as `str` instance, but not as an identifier of any of the predefined ones.
    TypeError
        - If `default_code` is neither `str` or `function`.
        - If `default_code` is given as `function`, but not as `async`
        - If `default_code` is given as `function`, but accepts bad amount of parameters.
    """
    default_code_type = type(default_code)
    if default_code_type is str:
        pass
    elif issubclass(default_code_type, str):
        default_code = str(default_code)
    elif callable(default_code):
        analyzed = CallableAnalyzer(default_code)
        if (not analyzed.is_async()):
            raise TypeError(f'`default_code` should have been given as `str`, or as an `async-callable` `function`, '
                f'got a function, but not an `async` one: an async function instance, got {default_code!r}.')
        
        non_reserved_positional_parameter_count = analyzed.get_non_reserved_positional_parameter_count()
        if non_reserved_positional_parameter_count!=1:
            raise TypeError(f'`default_code` should accept `1` non reserved positional parameters, meanwhile it expects '
                f'{non_reserved_positional_parameter_count}.')
        
        if analyzed.accepts_args():
            raise TypeError(f'`default_code` should accept not expect args, meanwhile it does.')
        
        if analyzed.accepts_kwargs():
            raise TypeError(f'`default_code` should accept not expect kwargs, meanwhile it does.')
        
        non_default_keyword_only_parameter_count = analyzed.get_non_default_keyword_only_parameter_count()
        if non_default_keyword_only_parameter_count:
            raise TypeError(f'`default_code` should accept `0` keyword only parameters, meanwhile it expects '
                f'{non_default_keyword_only_parameter_count}.')
        
        return default_code
    
    else:
        raise TypeError(f'`default_code` can be given as `str` instance, identifying a predefined default code '
            f'function, or as an `async-callable` `function` type, got {default_code_type.__name__}.')
    
    try:
        default_code = PREREGISTERED_DEFAULT_CODES[default_code]
    except KeyError:
        raise LookupError(f'`default_code` was given as `str` instance, but not as 1 of the predefined default codes, '
              f'got {default_code!r}') from None
    
    return default_code

def validate_annotation_type(annotation):
    """
    Validates a single annotation and returns it.
    
    Parameters
    ----------
    annotation : `type` or `str`
        The annotation to validate.
    
    Returns
    -------
    annotation : `type`
    
    Raises
    ------
    LookupError
        - If `annotation` was given as `type` instance, but that specified type has no parser settings added to it.
        - If `annotation` was given as `str` instance, but there is no added type representation to it.
    TypeError
        - If `annotation` was not given as `str`, neither as `type` instance.
    """
    annotation_type = annotation.__class__
    if annotation_type is str:
        pass
    elif issubclass(annotation_type, str):
        annotation = str(annotation)
    
    else:
        if (annotation_type is type) or issubclass(annotation_type, type):
            if (annotation not in CONVERTER_SETTING_TYPE_RELATION_MAP):
                raise LookupError(f'`annotation` was given as `type` instance, but there is no parser for it, got '
                    f'{annotation.__name__}.')
            
            return annotation
        
        raise TypeError(f'Expected `str` or `type` instance as `annotation`, got {annotation_type.__name__}.')
    
    try:
        annotation = CONVERTER_SETTING_NAME_TO_TYPE[annotation]
    except KeyError:
        raise LookupError(f'`annotation` was given as `str` instance, but there is no parser for it, got '
            f'{annotation!r}.') from None
    
    return annotation

def validate_annotation_type_flags(annotation, flags):
    """
    Raises
    ------
    LookupError
        If the given `annotation` has no linked parser setting for it.
    TypeError
        - If `annotation` is not given as `type` instance.
        - If `flags` is not given as ``ConverterFlag`` instance.
        - If `annotation`'s setting allows flags, and given, but the given flags have no interception with the allowed
            ones.
        - If `annotation`'s setting do not allows any flags, meanwhile given.
    """
    if not isinstance(annotation, type):
        raise TypeError(f'`annotation` should have be given as `type` instance, got {annotation.__class__.__name__}.')
    
    if not isinstance(flags, ConverterFlag):
        raise TypeError(f'`flags` should have be given as `{ConverterFlag.__name__}` instance, got '
            f'{flags.__class__.__name__}.')
    
    try:
        setting = CONVERTER_SETTING_TYPE_RELATION_MAP[annotation]
    except KeyError:
        raise LookupError(f'The given `annotation` has no settings linked to it, got: {annotation.__name__}.') \
            from None
    
    if setting.uses_flags:
        if flags:
            new_flags = ConverterFlag(setting.all_flags&flags)
            if not new_flags:
                raise TypeError(f'Flags was given as `{flags!r}`, meanwhile the {annotation!r} annotation\'s setting '
                    f'allows: {setting.all_flags!r}. The two has no interception.')
        else:
            new_flags = setting.default_flags
    
    else:
        if flags:
            raise TypeError(f'The annotation {annotation!r}\'s setting do not allows flags, meanwhile given: '
                f'{flags!r}.')
        
        new_flags = flags
    
    return new_flags

class FlaggedAnnotation:
    """
    Flagged annotation to store an annotation type with it's flags.
    
    This type of annotation can be used to define a multi-type events, not, like ``Converter``, which should not be
    used for that.
    
    Attributes
    ----------
    annotation : `type`
        The type to convert to.
    flags : ``ConverterFlag``
        Extra flags for conversion.
    """
    __slots__ = ('annotation', 'flags', )
    
    def __new__(cls, annotation, flags=None):
        """
        Creates a ``FlaggedAnnotation`` with the given parameters.
        
        Parameters
        ----------
        annotation : `type`, `str`, ``FlaggedAnnotation``, ``Converter``
            The annotation to convert.
        flags : ``ConverterFlag``, Optional
            Extra flags for conversion.
        
        Raises
        ------
        LookupError
            - If `annotation` was given as `type` instance, but that specified type has no parser settings added to it.
            - If `annotation` was given as `str` instance, but there is no added type representation to it.
        TypeError
            - If `annotation` was not given as `str`, neither as `type` instance.
            - If `flags` is not given as ``ConverterFlag`` instance, neither as `int`.
            - If `annotation`'s setting allows flags, and given, but the given flags have no interception with the
                allowed ones.
            - If `annotation`'s setting do not allows any flags, meanwhile given.
            - If `annotation` is given as ``Converter`` instance with default set.
        """
        # First check if the type is the same
        if type(annotation) is cls:
            return annotation
        
        # Second check type ``Converter``
        if type(annotation) is Converter:
            if annotation.default_type:
                raise TypeError(f'`annotation` is given as `{Converter.__name__}` instance with default set, got '
                    f'{annotation!r}.')
        
        # Real annotation
        annotation = validate_annotation_type(annotation)
        if flags is None:
            flags = ConverterFlag()
        else:
            flags = preconvert_flag(flags, 'flags', ConverterFlag)
        flags = validate_annotation_type_flags(annotation, flags)
        
        self = object.__new__(cls)
        self.annotation = annotation
        self.flags = flags
        return self
    
    def __repr__(self):
        """Returns the flagged annotation's representation."""
        return f'{self.__class__.__name__}(annotation={self.annotation!r}, flags={self.flags!r})'

def unnest_tuple(tuple_):
    """
    Yields the elements of the given `tuple`. If any of them is a `tuple` as well, then yields that's elements
    and repeat this cycle.
    
    This function is a generator.
    
    Parameters
    ----------
    tuple_ : `tuple` of `Any`
    
    Yields
    ------
    element : `Any`
    """
    for element in tuple_:
        if isinstance(element, tuple):
            yield from unnest_tuple(element)
        else:
            yield element

def validate_annotation(annotation, flags=None):
    """
    Validates a given annotation.
    
    Parameters
    ----------
    annotation : `str`, `type`, ``FlaggedAnnotation``, ``Converter``, `tuple` (repeat)
        The annotation to validate.
    flags : ``ConverterFlag``, Optional
        Converter flag to create the annotation with if given.
    
    Returns
    -------
    annotation : ``FlaggedAnnotation``, `tuple` of ``FlaggedAnnotation``
        The validated annotation.
    
    Raises
    ------
    LookupError
        If `annotation` was given as `type` or `str` instance, but there is no parser for it.
    TypeError
        - If `annotation` was given as `tuple`, but contains no real annotation.
        - If `annotation` is given as a ``Converter`` instance with default set.
    
    Notes
    -----
    If the same annotation type is given with different flags, then their flags will be merged.
    """
    if isinstance(annotation, tuple):
        annotations_by_type = {}
        for sub_annotation in unnest_tuple(annotation):
            flagged_annotation = FlaggedAnnotation(sub_annotation, flags=flags)
            annotation_type = flagged_annotation.annotation
            try:
                actual_flagged_annotation = annotations_by_type[annotation_type]
            except KeyError:
                annotations_by_type[annotation_type] = flagged_annotation
            else:
                flagged_annotation.flags = ConverterFlag(actual_flagged_annotation.flags|flagged_annotation.flags)
        
        result = tuple(annotations_by_type.values())
        
        result_length = len(result)
        if result_length < 2:
            if result_length == 0:
                raise TypeError(f'`annotation` is given as a `tuple`, but it contains no real annotation, got '
                    f'{annotation!r}.')
            if result_length == 1:
                result = result[0]
    else:
        result = FlaggedAnnotation(annotation, flags=flags)
    
    return result


class Converter:
    """
    Represents a converter type-hint for setting additional information for the parser.
    
    Parameters
    ----------
    annotation : ``FlaggedAnnotation`` or `tuple` of ``FlaggedAnnotation``
        Type and flag infos about the entity to parse.
    default : `Any`
        The default object to return if the parser fails
    default_type : `int`
        Describes how `default` is used up.
        
        Possible values:
        +-----------------------+-------+
        | Respective name       | Value |
        +=======================+=======+
        | DEFAULT_TYPE_NONE     | 0     |
        +-----------------------+-------+
        | DEFAULT_TYPE_OBJ      | 1     |
        +-----------------------+-------+
        | DEFAULT_TYPE_CALL     | 2     |
        +-----------------------+-------+
    """
    __slots__ = ('annotation', 'default_type', 'default', )
    def __new__(cls, annotation, flags=None, default=..., default_code=...):
        """
        Creates a ``Converter`` instance with the given parameters.
        
        Parameters
        ----------
        annotation : `str`, `type`, ``Converter``, ``FlaggedAnnotation`` or `tuple` (repeat)
            The type or a type-hint to what type the respective value should be converted.
        flags : ``ConverterFlag``, Optional
            Flags to use with the specified type's converter.
        default : `Any`, Optional
            Default object returned if conversion fails.
        default_code : `str` or `async-function`, Optional
            Default code, what will be called, when the conversion fails. Mutually exclusive with `default`.
            
            Can be given as an `async-function`, or as a `str` representing an already precreated one.
            
            The precreated ones are the following:
            
            +----------------------------------------+--------------------------------------------------------------+
            | Name                                   | Description                                                  |
            +========================================+==============================================================+
            | `'message.author'`                     | Returns the message's author.                                |
            +----------------------------------------+--------------------------------------------------------------+
            | `'message.channel'`                    | Returns the message's channel.                               |
            +----------------------------------------+--------------------------------------------------------------+
            | `'message.guild'`                      | Returns the message's guild. (Can be `None`)                 |
            +----------------------------------------+--------------------------------------------------------------+
            | `'message.guild'`              | Same as the `'message.guild'` one.                           |
            +----------------------------------------+--------------------------------------------------------------+
            | `'client'`                             | Returns the client, who received the message.                |
            +----------------------------------------+--------------------------------------------------------------+
            | `'rest'`                               | Returns the not yet used content of the message.             |
            |                                        | (Can be empty string)                                        |
            +----------------------------------------+--------------------------------------------------------------+
            | `'message.guild.default_role'`         | Returns the message's guild's default role. (Can be `None`)  |
            +----------------------------------------+--------------------------------------------------------------+
            | `'message.guild.default_role'` | Same as the `''message.guild.default_role''` one.            |
            +----------------------------------------+--------------------------------------------------------------+
            
            Defining these might can be difficult, because first you need to get along with hata internals, but to
            mention an example, the `'message.author'` precreated one equals to:
            
            ```py
            async def precreated_default_code__message_author(content_parser_ctx: ContentParserContext):
                return content_parser_ctx.message.author
            ```
        
        Raises
        ------
        LookupError
            - If `annotation` was given as `type` or `str` instance, but there is no parser for it.
            - If `default_code` is given as `str` instance, but not as an identifier of any of the predefined ones.
        TypeError
            - If `annotation` is given as a ``Converter`` instance with default set.
            - If `flags` was not given as ``ConverterFlag`` instance.
            - If `default` and `default_code` parameters were given at the same time.
            - If `default_code` is given, but neither as `str` or `function`.
            - If `default_code` is given as `function`, but not as `async`.
            - If `default_code` is given as `function`, but accepts bad amount of parameters.
        """
        if (flags is not None):
           flags = preconvert_flag(flags, 'flags', ConverterFlag)
        
        annotation = validate_annotation(annotation, flags=flags)
        
        if (default is ...):
            default_type = DEFAULT_TYPE_NONE
            default_value = None
        else:
            default_type = DEFAULT_TYPE_OBJ
            default_value = default
        
        if (default_code is not ...):
            if default_type:
                raise TypeError(f'`default` and `default_code` are mutually exclusive, meanwhile both was given,'
                    f'default = {default!r}, default_code = {default_code!r}.')
            
            default_type = DEFAULT_TYPE_CALL
            default_value = validate_default_code(default_code)
        
        self = object.__new__(cls)
        self.annotation = annotation
        self.default_type = default_type
        self.default = default_value
        return self
    
    def __repr__(self):
        """Returns the converter's representation."""
        result = [
            self.__class__.__name__,
            '(annotation=',
        ]
        
        is_default_only = True
        
        annotation = self.annotation
        if type(annotation) is tuple:
            for flagged_annotation in annotation:
                try:
                    setting = CONVERTER_SETTING_TYPE_RELATION_MAP[flagged_annotation.annotation]
                except KeyError:
                    # ????
                    continue
                
                if flagged_annotation.flags == setting.default_flags:
                    continue
                
                is_default_only = False
                break
        
        else:
            try:
                setting = CONVERTER_SETTING_TYPE_RELATION_MAP[annotation.annotation]
            except KeyError:
                # ????
                pass
            else:
                if annotation.flags != setting.default_flags:
                    is_default_only = False
        
        if is_default_only:
            if type(annotation) is tuple:
                result.append('(')
                index = 0
                limit = len(annotation)
                while True:
                    flagged_annotation = annotation[index]
                    index +=1
                    
                    result.append(repr(flagged_annotation.annotation))
                    
                    if index == limit:
                        break
                    
                    result.append(', ')
                    continue
            else:
                result.append(repr(annotation.annotation))
        
        else:
            if type(annotation) is tuple:
                result.append(repr(annotation))
            else:
                result.append(repr(annotation.annotation))
                result.append(', flags=')
                result.append(repr(annotation.flags))
        
        default_type = self.default_type
        if default_type != DEFAULT_TYPE_NONE:
            if default_type == DEFAULT_TYPE_OBJ:
                default_name = 'default'
            else:
                default_name = 'default_code'
            
            result.append(', ')
            result.append(default_name)
            result.append('=')
            result.append(repr(self.default))
        
        result.append(')')
        
        return ''.join(result)

class ContentParserParameterHinter:
    """
    Hinter for content parser about it's parameters.
    
    Parameters
    ---------
    default : `Any`
        The default object to return if the parser fails
    default_type : `int`
        Describes how `default` is used up.
        
        Possible values:
        +-----------------------+-------+
        | Respective name       | Value |
        +=======================+=======+
        | DEFAULT_TYPE_NONE     | 0     |
        +-----------------------+-------+
        | DEFAULT_TYPE_OBJ      | 1     |
        +-----------------------+-------+
        | DEFAULT_TYPE_CALL     | 2     |
        +-----------------------+-------+
    is_args : `bool`
        Whether *args parser should be chosen.
    annotation : `None`, ``FlaggedAnnotation``, `tuple` of ``FlaggedAnnotation``
        The type of the parser to be chosen or a type-hint about it.
    """
    __slots__ = ('default',  'default_type', 'annotation', 'is_args', )
    
    def __repr__(self):
        """Returns the inter's representation."""
        return f'{self.__class__.__name__}(default={self.default!r}, default_type={self.default_type!r}, annotation=' \
            f'{self.annotation!r}, is_args={self.is_args!r})'


class CommandContentParser:
    """
    Content parser for commands.
    
    Parameters
    ----------
    _parsers : `None` or `list` of ``ParserContextBase`` instances
        The events of the command content parser. Set as `None` if it would be an empty `list`.
    _separator : ``ContentParameterSeparator``
        The parameter separator of the parser.
    """
    __slots__ = ('_parsers', '_separator')
    
    def __new__(cls, func, separator):
        """
        Parameters
        ----------
        func : `async-callable`
            The callable function.
        separator : `None`, ``ContentParameterSeparator``, `str` or `tuple` (`str`, `str`)
            The parameter separator of the parser.
        
        Raises
        ------
        LookupError
            If `annotation` was given as `type` or `str` instance, but there is no parser for it.
        TypeError
            - If `func` is not given as `callable`
            - If `func` is not given as `async-callable`, and cannot be instanced to one neither.
            - If `func` (or it's converted form) accepts keyword only parameters.
            - If `func` (or it's converted form) accepts keyword **kwargs.
            - If `func` (or it's converted form) accepts less then 2 non reversed parameter without *args.
            - If `func`'s (or it's converted form's) first parameter has default value set.
            - If `func`'s (or it's converted form's) first parameter has annotation set, but not as type ``Client``.
            - If `func`'s (or it's converted form's) second parameter has default value set.
            - If `func`'s (or it's converted form's) second parameter has annotation set, but not as type ``Message``.
            - If an parameter has annotation as a ``Converter`` instance with default value, meanwhile the parameter
                itself also has it's own default value.
            - If an annotation was given as `None` or as empty `tuple` meanwhile.
            - If an annotation was given as `tuple`, but any of it's element is not `None`, or `str`, `type` or `tuple`
                instance.
            - If `*args` parameter's annotation was given as ``Converter`` instance with default value set.
            - If `separator` is not given as `None`, ``ContentParameterSeparator``, `str`, neither as `tuple` instance.
            - If `separator was given as `tuple`, but it's element are not `str` instances.
        ValueError
            - If `separator` is given as `str`, but it's length is not 1.
            - If `separator` is given as `str`, but it is a space character.
            - If `separator` is given as `tuple`, but one of it's element's length is not 1.
            - If `separator` is given as `tuple`, but one of it's element's is a space character.
        """
        separator = ContentParameterSeparator(separator)
        
        analyzer = CallableAnalyzer(func)
        if analyzer.is_async() or analyzer.is_async_generator():
            real_analyzer = analyzer
            should_instance = False
        
        elif analyzer.can_instance_to_async_callable() or analyzer.can_instance_to_async_generator():
            real_analyzer = CallableAnalyzer(func.__call__, as_method=True)
            if (not real_analyzer.is_async()) and (not real_analyzer.is_async_generator()):
                raise TypeError(f'`func` is not `async-callable` and cannot be instanced to `async` either, got '
                    f'{func!r}.')
            
            should_instance = True
        
        else:
            raise TypeError(f'`func` is not `async-callable` and cannot be instanced to `async` either, got {func!r}.')
        
        keyword_only_parameter_count = real_analyzer.get_non_default_keyword_only_parameter_count()
        if keyword_only_parameter_count:
            raise TypeError(f'`{real_analyzer.real_function!r}` accepts keyword only parameters.')
        
        if real_analyzer.accepts_kwargs():
            raise TypeError(f'`{real_analyzer.real_function!r}` accepts **kwargs.')
        
        parameters = real_analyzer.get_non_reserved_positional_parameters()
        
        parameter_count = len(parameters)
        if parameter_count<2:
            raise TypeError(f'`{real_analyzer.real_function!r}` should accept at least 2 parameters (without *args): '
                f'`client` and `message`, meanwhile it accepts only {parameter_count}.')
        
        client_parameter = parameters[0]
        if client_parameter.has_default:
            raise TypeError(f'`{real_analyzer.real_function!r}` has default parameter set as it\'s first not '
                'reserved, meanwhile it should not have.')
        
        if client_parameter.has_annotation and (client_parameter.annotation is not Client):
            raise TypeError(f'`{real_analyzer.real_function!r}` has annotation at the client\'s parameter slot, '
                f'what is not `{Client.__name__}`.')
        
        message_parameter = parameters[1]
        if message_parameter.has_default:
            raise TypeError(f'`{real_analyzer.real_function!r}` has default parameter set as it\'s first not '
                f'reserved, meanwhile it should not have.')
        
        if message_parameter.has_annotation and (message_parameter.annotation is not Message):
            raise TypeError(f'`{real_analyzer.real_function!r}` has annotation at the message\'s parameter slot '
                f'what is not `{Message.__name__}`.')
        
        hinters = []
        to_check = parameters[2:]
        args_parameter = real_analyzer.args_parameter
        
        index = 0
        limit = len(to_check)
        while True:
            if index == limit:
                break
            
            parameter = to_check[index]
            index += 1
            
            if parameter.has_annotation:
                annotation = parameter.annotation
                if type(annotation) is Converter:
                    hinter_default = annotation.default
                    hinter_default_type = annotation.default_type
                    hinter_annotation = annotation.annotation
                
                    if parameter.has_default:
                        if hinter_default_type:
                            raise TypeError(f'`annotation` of `{parameter.name}` is given as '
                                f'`{Converter.__class__.__name__}` instance, as {Converter!r} (with default value '
                                f'set), meanwhile the parameter has default value set as well: {parameter.default!r}.')
                        
                        hinter_default = parameter.default
                        hinter_default_type = DEFAULT_TYPE_OBJ
                
                else:
                    annotation = validate_annotation(annotation)
                    
                    if parameter.has_default:
                        hinter_default = parameter.default
                        hinter_default_type = DEFAULT_TYPE_OBJ
                    else:
                        hinter_default = None
                        hinter_default_type = DEFAULT_TYPE_NONE
                    
                    hinter_annotation = annotation
                
            else:
                if parameter.has_default:
                    default = parameter.default
                    if (index == limit) and (args_parameter is None):
                        hinter_annotation = None
                    else:
                        hinter_annotation = FlaggedAnnotation(str)
                    
                    hinter_default = default
                    hinter_default_type = DEFAULT_TYPE_OBJ
                    
                else:
                    if (index == limit) and (args_parameter is None):
                        hinter_annotation = None
                    else:
                        hinter_annotation = FlaggedAnnotation(str)
                    
                    hinter_default = None
                    hinter_default_type = DEFAULT_TYPE_NONE
            
            hinter = ContentParserParameterHinter()
            hinter.default = hinter_default
            hinter.default_type = hinter_default_type
            hinter.annotation = hinter_annotation
            hinter.is_args = False
            hinters.append(hinter)
        
        if (args_parameter is not None):
            if args_parameter.has_annotation:
                annotation = args_parameter.annotation
                if type(annotation) is Converter:
                    if annotation.default_type:
                        raise TypeError(f'`*args` annotation is given as `{Converter.__class__.__name__} as '
                            f'{Converter!r}, so with default value set, do not do that!')
                    
                    hinter_annotation = annotation.annotation
                else:
                    hinter_annotation = validate_annotation(annotation)
            else:
                hinter_annotation = FlaggedAnnotation(str)
            
            hinter = ContentParserParameterHinter()
            hinter.default = None
            hinter.default_type = DEFAULT_TYPE_NONE
            hinter.annotation = hinter_annotation
            hinter.is_args = True
            hinters.append(hinter)
        
        parsers = []
        for hinter in hinters:
            annotation = hinter.annotation
            if annotation is None:
                parser = RestParserContext(hinter.default_type, hinter.default)
            
            else:
                if hinter.is_args:
                    if type(annotation) is tuple:
                        parser_cls = ChainedArgsParserContext
                    else:
                        parser_cls = SingleArgsParserContext
                    
                    parser = parser_cls(annotation)
                
                else:
                    if type(annotation) is tuple:
                        parser_cls = ChainedParserContext
                    else:
                        parser_cls = SingleParserContext
                    
                    parser = parser_cls(annotation, hinter.default_type, hinter.default)
            
            parsers.append(parser)
        
        if not parsers:
            parsers = None
        
        if should_instance:
            func = analyzer.insatnce()
        
        self = object.__new__(cls)
        self._parsers = parsers
        self._separator = separator
        return self, func
    
    async def get_args(self, client, message, content):
        """
        Parses the given content and returns whether it passed and what was parser.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who received the respective message.
        message : ``Message``
            The received message.
        content : `str`
            The message's content to parse. Can be empty.
        
        Returns
        -------
        passed : `bool`
            Whether the parsing all the parameters of the message succeeded.
        args : `None` or `list` of `Any`
            The parsed out entities. Can be empty list.
        """
        parsers = self._parsers
        if parsers is None:
            return True, None
        
        content_parser_context = ContentParserContext(self._separator, client, message, content)
        for parser in parsers:
            result = await parser(content_parser_context)
            if result:
                continue
            
            return False, content_parser_context.result
        
        return True, content_parser_context.result
    
    def __bool__(self):
        """Returns whether the content parser parses anything."""
        parsers = self._parsers
        if parsers is None:
            return False
        
        if parsers:
            return True
        
        return False
    
    def __repr__(self):
        """Returns the command content parser's representation."""
        result = [
            '<',
            self.__class__.__name__,
        ]
        
        parsers = self._parsers
        if (parsers is not None):
            result.append(' events=')
            result.append(repr(parsers))
            
            separator = self._separator
            if (separator is not DEFAULT_SEPARATOR):
                result.append(', separator=')
                result.append(repr(separator))
        
        result.append('>')
        
        return ''.join(result)

class ContentParser(CommandContentParser):
    """
    Represents a content parser, what can be used as a standalone wrapper of a function.
    
    Parameters
    ----------
    _parsers : `None` or `list` of ``ParserContextBase`` instances
        The events of the command content parser. Set as`None` if it would be an empty `list`.
    _separator : ``ContentParameterSeparator``
        The parameter separator of the parser.
    _func : `async-callable`
        The wrapped function.
    _handler : `None` or `async-callable`
        A coroutine function what is ensured, when parsing the parameters fail.
    _is_method : `bool`
        Whether the ``ContentParser`` should act like a method descriptor.
    """
    __slots__ = ('_func', '_handler', '_is_method',)
    def __new__(cls, func=None, handler=None, is_method=False, separator=None):
        """
        Parameters
        ----------
        func : `None`, `async-callable` or instantiable to `async-callable`, Optional
        
        handler : `None`, `async-callable` or instantiable to `async-callable`, Optional
            An async callable, what is ensured when the parser's cannot parse all the required parameters out.
            
            If given, should accept the following parameters:
            +-----------------------+-------------------+
            | Respective name       | Type              |
            +=======================+===================+
            | client                | ``Client``        |
            +-----------------------+-------------------+
            | message               | ``Message``       |
            +-----------------------+-------------------+
            | content_parser        | ``ContentParser`` |
            +-----------------------+-------------------+
            | content               | `str`             |
            +-----------------------+-------------------+
            | args                  | `list` of `Any`   |
            +-----------------------+-------------------+
            | parent                | `Any`             |
            +-----------------------+-------------------+
        
        is_method : `bool`, Optional
            Whether the content parser should act like a method. Default to `False`.
        separator : `None`, ``ContentParameterSeparator``, `str` or `tuple` (`str`, `str`), Optional
            The parameter separator of the parser.
        
        Returns
        -------
        wrapper / self : ``ContentParser._wrapper`` / ``ContentParser``
            If `func` is not given, then returns a wrapper, what allows using the content parser as a decorator with
            still giving parameters.
        
        Raises
        ------
        TypeError
            - If `is_method` is not given as `bool` instance.
            - If `handler` is not async, neither cannot be instanced to async.
            - If `handler` (or it's converted form) would accept bad amount of parameters.
            - If `separator` is not given as `None`, ``ContentParameterSeparator``, `str`, neither as `tuple` instance.
            - If `separator was given as `tuple`, but it's element are not `str` instances.
        ValueError
            - If `separator` is given as `str`, but it's length is not 1.
            - If `separator` is given as `str`, but it is a space character.
            - If `separator` is given as `tuple`, but one of it's element's length is not 1.
            - If `separator` is given as `tuple`, but one of it's element's is a space character.
        """
        is_method = preconvert_bool(is_method, 'is_method')
        
        if (handler is not None):
            handler = check_parameter_count_and_convert(handler, 6, name='handler', error_message= \
                '`ContentParser` expects to pass `6` parameters to it\'s `handler`: client, message, content_parser, '
                'content, args, obj (can be `None`).')
        
        separator = ContentParameterSeparator(separator)
        
        if func is None:
            return cls._wrapper(handler, is_method, separator)
        
        if is_method:
            func = MethodType(func, object())
        self, func = CommandContentParser.__new__(cls, func, separator)
        if is_method:
            func = func.__func__
        
        self._func = func
        self._handler = handler
        self._is_method = is_method
        return self
    
    class _wrapper:
        """
        A wrapper of ``ContentParser`` to allow using it as a decorator.
        
        Parameters
        ----------
        _handler : `None`, `async-callable`
            An async callable, what is ensured when the parser's cannot parse all the required parameters out.
            
            If given as not `None` should accept the following parameters:
            +-----------------------+-------------------+
            | Respective name       | Type              |
            +=======================+===================+
            | client                | ``Client``        |
            +-----------------------+-------------------+
            | message               | ``Message``       |
            +-----------------------+-------------------+
            | content_parser        | ``ContentParser`` |
            +-----------------------+-------------------+
            | content               | `str`             |
            +-----------------------+-------------------+
            | args                  | `list` of `Any`   |
            +-----------------------+-------------------+
            | parent                | `Any`             |
            +-----------------------+-------------------+
        _is_method : `bool`
            Whether the content parser should act like a method.
        _separator : ``ContentParameterSeparator``
            The parameter separator of the parser.
        """
        __slots__ = ('_handler', '_is_method', '_separator', )
        
        def __init__(self, handler, is_method, separator):
            """
            Creates a new content parser wrapper.
            
            Parameters
            ----------
            handler : `None`, `async-callable`
                An async callable, what is ensured when the parser's cannot parse all the required parameters out.
                
                If given as not `None` should accept the following parameters:
            +-----------------------+-------------------+
            | Respective name       | Type              |
            +=======================+===================+
            | client                | ``Client``        |
            +-----------------------+-------------------+
            | message               | ``Message``       |
            +-----------------------+-------------------+
            | content_parser        | ``ContentParser`` |
            +-----------------------+-------------------+
            | content               | `str`             |
            +-----------------------+-------------------+
            | args                  | `list` of `Any`   |
            +-----------------------+-------------------+
            | parent                | `Any`             |
            +-----------------------+-------------------+
            is_method : `bool`
                Whether the content parser should act like a method.
            separator : ``ContentParameterSeparator``
                The parameter separator of the parser.
            """
            self._handler = handler
            self._is_method = is_method
            self._separator = separator
        
        def __call__(self, func):
            """
            Calls the content parser wrapper to create a ``ContentParser`` instance.
            
            Parameters
            ----------
            func : `async-callable` or instantiable to `async-callable`
                The function to wrap.
            
            Returns
            -------
            content_parser : ``ContentParser``
            
            Raises
            ------
            TypeError
                If `func` was given as `None`.
            """
            if func is None:
                raise TypeError(f'`func` cannot be given as `None`, got {func!r}.')
            
            return ContentParser(func=func, handler=self._handler, is_method=self._is_method, separator=self._separator)
    
    async def __call__(self, *args):
        """
        This method is a coroutine.
        
        Parameters
        ----------
        If the content parser is a method:
            parent : `Any`
                The owner entity
            client : ``Client``
                The respective client.
            message : ``Message``
                The respective message.
            content : `str`, Optional
                The content to parse. Defaults to empty string.
        
        If the content parser is not a method:
            client : ``Client``
                The respective client.
            message : ``Message``
                The respective message.
            content : `str`, Optional
                The content to parse. Defaults to empty string.
        
        Returns
        -------
        passed : `bool`
            If parsing the content was successful.
        
        Raises
        ------
        TypeError
            Unexpected amount of parameters were passed.
        """
        # Parse out parameters.
        args_count = len(args)
        if self._is_method:
            if args_count < 3 or args_count > 4:
                raise TypeError(f'{self!r} expects 3-4 positional parameters to be given, got {args_count}.')
            
            if args_count == 3:
                parent, client, message = args
                content = ''
            else:
                parent, client, message, content = args
        else:
            if args_count < 2 or args_count > 3:
                raise TypeError(f'{self!r} expects 2-3 positional parameters to be given, got {args_count}.')
            
            if args_count == 2:
                client, message = args
                content = ''
            else:
                client, message, content = args
        
        # parse content
        passed, args = await self.get_args(client, message, content)
        if not passed:
            handler = self._handler
            if (handler is not None):
                # Handle parsing failure
                if not self._is_method:
                    parent = None
                
                await handler(client, message, self, content, args, parent)
            
            return False
        
        # call function
        func = self._func
        if args is None:
            if self._is_method:
                coro = func(parent, client, message)
            else:
                coro = func(client, message)
        else:
            if self._is_method:
                coro = func(parent, client, message, *args)
            else:
                coro = func(client, message, *args)
        
        await coro
        return True
    
    def __get__(self, obj, type_):
        if self._is_method:
            if obj is None:
                obj = type_
            
            return ContentParserMethod(self, obj)
        
        return self

    def __set__(self, obj, value):
        raise AttributeError('can\'t set attribute')

    def __delete__(self, obj):
        raise AttributeError('can\'t delete attribute')
    
    def __repr__(self):
        """Returns the content parser's representation."""
        result = [
            '<',
            self.__class__.__name__,
        ]
        
        func = self._func
        result.append(' func=')
        result.append(repr(func))
        
        parsers = self._parsers
        if (parsers is not None):
            result.append(', events=')
            result.append(repr(parsers))
            
            separator = self._separator
            if (separator is not DEFAULT_SEPARATOR):
                result.append(', separator=')
                result.append(repr(separator))
        
        handler = self._handler
        if (handler is not None):
            result.append(', handler=')
            result.append(repr(handler))
        
        if self._is_method:
            result.append(', is_method=True')
        
        result.append('>')
        
        return ''.join(result)

class ContentParserMethod(MethodLike):
    """
    ``ContentParser``'s method wrapper.
    
    Attributes
    ----------
    __self__ : `Any`
        The object with what the method was called.
    _content_parser : ``ContentParser``
        The parent content parser, what was called as a method.
    """
    __slots__ = ('__self__', '_content_parser', )
    __reserved_argcount__ = 2
    
    def __new__(cls, content_parser, obj):
        """
        Creates a new ``ContentParserMethod`` instance with the given content parser and the parent object.
        
        Parameters
        ----------
        content_parser : ``ContentParser``
            The source content parser.
        obj : `Any`
            The parent object.
        """
        self = object.__new__(cls)
        self._content_parser = content_parser
        self.__self__   = obj
        return self
    
    @property
    def __func__(self):
        """Returns the wrapped function."""
        return self._content_parser._func
    
    async def __call__(self, *args):
        """
        Calls the content parser method.
        
        This method is a coroutine.
        
        Parameters
        ----------
        parent : `Any`
            The owner entity
        client : ``Client``
            The respective client.
        message : ``Message``
            The respective message.
        content : `str`, Optional
            The content to parse. Defaults to empty string.
        
        Returns
        -------
        passed : `bool`
            If parsing the content was successful.
        
        Raises
        ------
        TypeError
            Unexpected amount of parameters were passed.
        """
        return await self._content_parser(self.__self__, *args)
    
    @module_property
    def __module__(self):
        """Return the module of the wrapped function."""
        return self._content_parser._func.__module__
    
    def __getattr__(self, name):
        """Returns the wrapped function's attribute."""
        return getattr(self._content_parser._func, name)
    
    def __repr__(self):
        """Returns the method's representation."""
        return f'{self.__class__.__name__}(content_parser={self._content_parser!r}, obj={self.__self__!r})'
