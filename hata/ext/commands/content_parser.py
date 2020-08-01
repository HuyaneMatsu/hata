# -*- coding: utf-8 -*-
__all__ = ('Converter', 'ConverterFlag', 'ContentParser', 'FlaggedAnnotation')

#TODO: ask python for GOTO already
import re
from datetime import timedelta

try:
    from dateutil.relativedelta import relativedelta
except ImportError:
    relativedelta = None

from ...backend.dereaddons_local import function, _spaceholder, MethodLike
from ...backend.analyzer import CallableAnalyzer

from ...discord.bases import FlagBase
from ...discord.others import USER_MENTION_RP, ROLE_MENTION_RP, CHANNEL_MENTION_RP, ID_RP, INVITE_CODE_RP
from ...discord.client import Client
from ...discord.exceptions import DiscordException, ERROR_CODES
from ...discord.emoji import parse_emoji, Emoji, EMOJIS
from ...discord.client_core import CACHE_USER, USERS, CHANNELS, ROLES, GUILDS, MESSAGES
from ...discord.message import Message
from ...discord.channel import ChannelBase, ChannelGuildBase, ChannelTextBase, ChannelText, ChannelPrivate, \
    ChannelVoice, ChannelGroup, ChannelCategory, ChannelStore
from ...discord.user import User, UserBase
from ...discord.role import Role
from ...discord.parsers import check_argcount_and_convert
from ...discord.preconverters import preconvert_flag, preconvert_bool
from ...discord.guild import Guild
from ...discord.http.URLS import MESSAGE_JUMP_URL_RP, INVITE_URL_PATTERN
from ...discord.invite import Invite

NUMERIC_CONVERSION_LIMIT = 100

DELTA_RP = re.compile('([\+\-]?\d+) *([a-zA-Z]+)')
PARSER_RP = re.compile('(?:"(.+?)"|(\S+))[^"\S]*')

CHANNEL_MESSAGE_RP = re.compile('(\d{7,21})-(\d{7,21})')

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
    user : `None` or``UserBase`` instance
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
    role : `None` or``Role`` instance
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

    channel_id=int(parsed.group(1))
    for channel in channel_mentions:
        if channel.id==channel_id:
            return channel

class ConverterFlag(FlagBase):
    """
    Flags for a converter to describe by which rules it should convert.
    
    +---------------+---------------+
    | Rule name     | Shift value   |
    +===============+===============+
    | url           | 0             |
    +---------------+---------------+
    | mention       | 1             |
    +---------------+---------------+
    | name          | 2             |
    +---------------+---------------+
    | id            | 3             |
    +---------------+---------------+
    | everywhere    | 4             |
    +---------------+---------------+
    | profile       | 5             |
    +---------------+---------------+
    """
    __keys__ = {
        'url'       : 0,
        'mention'   : 1,
        'name'      : 2,
        'id'        : 3,
        'everywhere': 4,
        'profile'   : 5,
            }
    
    user_default = NotImplemented
    role_default = NotImplemented
    channel_default = NotImplemented
    emoji_default = NotImplemented
    guild_default = NotImplemented
    message_default = NotImplemented
    invite_default = NotImplemented

ConverterFlag.user_default = ConverterFlag().update_by_keys(mention=True, name=True, id=True)
ConverterFlag.role_default = ConverterFlag().update_by_keys(mention=True, name=True, id=True)
ConverterFlag.channel_default = ConverterFlag().update_by_keys(mention=True, name=True, id=True)
ConverterFlag.emoji_default = ConverterFlag().update_by_keys(mention=True, name=True, id=True)
ConverterFlag.guild_default = ConverterFlag().update_by_keys(id=True)
ConverterFlag.message_default = ConverterFlag().update_by_keys(url=True, id=True)
ConverterFlag.invite_default = ConverterFlag().update_by_keys(url=True, id=True)

CONVERTER_FLAG_URL = 1 << ConverterFlag.__keys__['url']
CONVERTER_FLAG_MENTION = 1 << ConverterFlag.__keys__['mention']
CONVERTER_FLAG_NAME = 1 << ConverterFlag.__keys__['name']
CONVERTER_FLAG_ID = 1 << ConverterFlag.__keys__['id']
CONVERTER_FLAG_EVERYWHERE = 1 << ConverterFlag.__keys__['everywhere']
CONVERTER_FLAG_PROFILE = 1 << ConverterFlag.__keys__['profile']

class ContentParserContext(object):
    """
    Content parser instance context used when parsing a message's content.
    
    Attributes
    ----------
    client : ``Client``
        The respective client.
    content : `str`
        A message's content after it's prefix, but only till first linebreak if applicable.
    index : `int`
        The index, of the last character's end.
    last_part : `str` or `None`
        The last parsed part.
    last_start : `bool`
        When the last returned string started
    length : `int`
        The length of the string to parse.
    message : ``Message``
        The respective message.
    result : `list` of `Any`
        The successfully parsed objects.
    """
    __slots__ = ('client', 'content', 'index', 'last_part', 'last_start', 'length', 'message', 'result', )
    
    def __init__(self, client, message, content):
        """
        Creates a new ``ContentParserContext`` instance.
        
        Parameters
        ----------
        client : ``Client``
            The respective client.
        message : ``Message``
            The respective message.
        content : `str`
            A message's content after it's prefix, but only till first linebreak if applicable.
        """
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
        next_ : `str` or `None`
            Returns `None` if the message has no more parts left.
        """
        index = self.index
        length = self.length
        if index == length:
            if self.last_start == index:
                next_ = None
            else:
                next_ = self.last_part
        else:
            parsed = PARSER_RP.match(self.content, index)
            next_ = parsed.group(2)
            if next_ is None:
                next_ = parsed.group(1)
            
            self.last_part = next_
            self.last_start = index
            self.index = parsed.end()
        
        return next_
    
    def mark_last_as_used(self):
        """
        Marks the lastly returned srting as it was used up, making the next call to try to parse a
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

class ParserContextBase(object):
    """
    Base class for parser contexts.
    """
    __slots__ = ()
    
    async def __call__(self, content_parser_ctx):
        """
        Calls the ``ParserContextBase`` with the given content parser context.
        
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

class ParserContext(ParserContextBase):
    """
    Parser context used inside of chanined content parsers.
    
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
            If `flagged_annotation` was gived as `tuple`.
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
            If `flagged_annotation` was gived not given as `tuple` or it contains only 1 (or less) element.
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
            Describes what type on entity and how it whould be parsed.
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
            If `flagged_annotation` was gived as `tuple`.
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
            If `flagged_annotation` was gived not given as `tuple` or it contains only 1 (or less) element.
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

CONVERTER_SETTING_TYPE_RELATION_MAP = {}
CONVERTER_SETTING_NAME_TO_TYPE = {}

class ConverterSetting(object):
    """
    Store settings about a converter.
    
    Attributes
    ----------
    all_flags : ``ConverterFlag``
        All the flags which the converter picks up.
    alternative_type_name : `None` or `str`
        Alternative string name for the parser, what allows picking up a respective converter.
    alternative_type_name : `None` or `str`
        Alternative string name for the parser, what allows picking up a respective converter.
    converter : `function` (async)
        The converter function.
    default_flags : ``ConverterFlag``
        The detault flags whith what teh converter will be used if not defining any specific.
    default_type : `None` or `type`
        The default annotation type of the converter.
    uses_flags : `bool`
        Whether the converter processes any flags.
    """
    __slots__ = ('all_flags', 'alternative_type_name', 'alternative_types', 'converter', 'default_flags', 'default_type', 'uses_flags')
    
    def __new__(cls, converter, uses_flags, default_flags, all_flags, alternative_type_name, default_type, alternative_types):
        """
        Creates a new ``ConverterSetting`` instance to store settings related to a converter function.
        
        Parameters
        ----------
        converter : `function` (async)
            The converter function.
        uses_flags : `bool`
            Whether the converter processes any flags.
        default_flags : ``ConverterFlag``
            The detault flags whith what teh converter will be used if not defining any specific.
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
            - If `converter` is not type function.
            - If `converter` is not async.
            - If `converter` accepts bad amount of arguments.
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
        if (converter_type is not function):
            raise TypeError(f'`converter` shoud have been given as `{function.__name__}` instance, got '
                f'{converter_type.__name__}.')
        
        analyzed = CallableAnalyzer(converter)
        if (not analyzed.is_async()):
            raise TypeError(f'`converter` shoud have been given as an async function instance, got '
                f'{converter!r}.')
        
        non_reserved_positional_argument_count = analyzed.get_non_reserved_positional_argument_count()
        if non_reserved_positional_argument_count!=2:
            raise TypeError(f'`converter` shoud accept `2` non reserved positonal arguments, meanwhile it expects '
                f'{non_reserved_positional_argument_count}.')
        
        if analyzed.accepts_args():
            raise TypeError(f'`converter` shoud accept not expect args, meanwhile it does.')
        
        if analyzed.accepts_kwargs():
            raise TypeError(f'`converter` shoud accept not expect kwargs, meanwhile it does.')
        
        non_default_keyword_only_argument_count = analyzed.get_non_default_keyword_only_argument_count()
        if non_default_keyword_only_argument_count:
            raise TypeError(f'`converter` shoud accept `0` keyword only arguments, meanwhile it expects '
                f'{non_default_keyword_only_argument_count}.')
        
        uses_flags_type = uses_flags.__class__
        if uses_flags_type is bool:
            pass
        elif issubclass(uses_flags_type, int):
            if uses_flags in (0,1):
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
                        guild = message.channel.guild
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
    all_flags = ConverterFlag().update_by_keys(
        everywhere=True, id=True, name=True, mention=True, profile=True),
    alternative_type_name = 'user',
    default_type = User,
    alternative_types = [
        UserBase,
            ],
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
                        channel = guild.all_channel[id_]
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
    all_flags = ConverterFlag().update_by_keys(
        everywhere=True, id=True, name=True, mention=True),
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
                guild = message.channel.guild
                if (guild is not None):
                    try:
                        role = guild.all_role[id_]
                    except KeyError:
                        pass
                    else:
                        return role
    
    if flags&CONVERTER_FLAG_MENTION:
        role = parse_role_mention(part, message)
        if (role is not None):
            return role
    
    if flags&CONVERTER_FLAG_NAME:
        guild = message.channel.guild
        if (guild is not None):
            role = guild.get_role_like(part)
            if (role is not None):
                return role
    
    return None

ConverterSetting(
    converter = role_converter,
    uses_flags = True,
    default_flags = ConverterFlag.role_default,
    all_flags = ConverterFlag().update_by_keys(
        everywhere=True, id=True, name=True, mention=True),
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
                guild = message.channel.guild
                if (guild is not None):
                    try:
                        emoji = guild.EMOJIS[id_]
                    except KeyError:
                        pass
                    else:
                        return emoji
    
    if flags&CONVERTER_FLAG_NAME:
        guild = message.channel.guild
        if (guild is not None):
            emoji = guild.get_emoji_like(part)
            if (emoji is not None):
                return emoji
    
    return None

ConverterSetting(
    converter = emoji_converter,
    uses_flags = True,
    default_flags = ConverterFlag.emoji_default,
    all_flags = ConverterFlag().update_by_keys(
        everywhere=True, id=True, name=True, mention=True),
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
    default_flags = ConverterFlag().guild_default,
    all_flags = ConverterFlag().update_by_keys(
        everywhere=True, id=True),
    alternative_type_name = 'guild',
    default_type = Guild,
    alternative_types = None,
        )

# Gets a message by it's id
async def _message_converter_m_id(parser_ctx, content_parser_ctx, message_id):
    message = MESSAGES.get(message_id)
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
                if message.channel.guild is guild:
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
                    ERROR_CODES.invalid_access, # client removed
                    ERROR_CODES.invalid_permissions, # permissions changed meanwhile
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
    message = MESSAGES.get(message_id)
    if (message is not None):
        # Message found
        if parser_ctx.flags&CONVERTER_FLAG_EVERYWHERE:
            return message
        else:
            # Only local message can be yielded, so check if it is local
            guild = channel.guild
            if (message.channel is channel) if (guild is None) else (message.channel.guild is guild):
                return message
        
        # Message found, but other guild or channel yield None
        return None
    
    message_channel = CHANNELS.get(channel_id)
    if (message_channel is None):
        return None

    if parser_ctx.flags&CONVERTER_FLAG_EVERYWHERE:
        # Lets use that multy client core
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
                            ERROR_CODES.invalid_access, # client removed
                            ERROR_CODES.invalid_permissions, # permissions changed meanwhile
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
                        ERROR_CODES.invalid_access, # client removed
                        ERROR_CODES.invalid_permissions, # permissions changed meanwhile
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
    default_flags = ConverterFlag().message_default,
    all_flags = ConverterFlag().update_by_keys(
        everywhere=True, id=True, url=True),
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
            parsed = INVITE_URL_PATTERN.fullmatch(part)
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
    default_flags = ConverterFlag().invite_default,
    all_flags = ConverterFlag().invite_default,
    alternative_type_name = 'invite',
    default_type = Invite,
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
        return None
    else:
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

TDELTA_KEYS = ('weeks', 'days', 'hours', 'minutes', 'seconds', 'microseconds')

async def tdelta_converter(parser_ctx, content_parser_ctx):
    part = content_parser_ctx.get_next()
    if part is None:
        return None
    
    result = {}
    index = 0
    limit = len(TDELTA_KEYS)
    for amount, name in DELTA_RP.findall(part):
        name = name.lower()
        if index == limit:
            break
        
        while True:
            key = TDELTA_KEYS[index]
            index += 1
            if key.startswith(name):
                result.setdefault(key, int(amount))
                break
            
            if index == limit:
                break
    
    if result:
        return timedelta(**result)

ConverterSetting(
    converter = tdelta_converter,
    uses_flags = False,
    default_flags = ConverterFlag(),
    all_flags = ConverterFlag(),
    alternative_type_name = 'tdelta',
    default_type = timedelta,
    alternative_types = None,
        )

RDELTA_KEYS = ('years','months', *TDELTA_KEYS)

if (relativedelta is not None):
    async def rdelta_converter(parser_ctx, content_parser_ctx):
        part = content_parser_ctx.get_next()
        if part is None:
            return None
        
        result = {}
        index = 0
        limit = len(RDELTA_KEYS)
        for amount, name in DELTA_RP.findall(part):
            name = name.lower()
            if index == limit:
                break
            
            while True:
                key = RDELTA_KEYS[index]
                index += 1
                if key.startswith(name):
                    result.setdefault(key, int(amount))
                    break
                
                if index == limit:
                    break
        
        if result:
            return relativedelta(**result)
    
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
    return content_parser_ctx.message.channel.guild

PREREGISTERED_DEFAULT_CODES['message.guild'] = prdc_mg
PREREGISTERED_DEFAULT_CODES['message.channel.guild'] = prdc_mg
del prdc_mg

async def prdc_c(content_parser_ctx):
    return content_parser_ctx.message.channel.guild

PREREGISTERED_DEFAULT_CODES['client'] = prdc_c
del prdc_c

async def prdc_r(content_parser_ctx):
    return content_parser_ctx.get_rest()

PREREGISTERED_DEFAULT_CODES['rest'] = prdc_r
del prdc_r

def validate_default_code(default_code):
    """
    Valdiates the given `default-code`.
    
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
        - If `default_code` is given as `function`, but accepts bad amount of arguments.
    """
    default_code_type = type(default_code)
    if default_code_type is str:
        pass
    elif issubclass(default_code_type, str):
        default_code = str(default_code)
    elif callable(default_code):
        analyzed = CallableAnalyzer(default_code)
        if (not analyzed.is_async()):
            raise TypeError(f'`default_code` shoud have been given as `str`, or as an `async-callable` `function`, '
                f'got a function, but not an `async` one: an async function instance, got {default_code!r}.')
        
        non_reserved_positional_argument_count = analyzed.get_non_reserved_positional_argument_count()
        if non_reserved_positional_argument_count!=1:
            raise TypeError(f'`default_code` should accept `1` non reserved positonal arguments, meanwhile it expects '
                f'{non_reserved_positional_argument_count}.')
        
        if analyzed.accepts_args():
            raise TypeError(f'`default_code` should accept not expect args, meanwhile it does.')
        
        if analyzed.accepts_kwargs():
            raise TypeError(f'`default_code` should accept not expect kwargs, meanwhile it does.')
        
        non_default_keyword_only_argument_count = analyzed.get_non_default_keyword_only_argument_count()
        if non_default_keyword_only_argument_count:
            raise TypeError(f'`default_code` should accept `0` keyword only arguments, meanwhile it expects '
                f'{non_default_keyword_only_argument_count}.')
        
        return default_code
    
    else:
        raise TypeError(f'`default_code` can be given as `str` instance, identifying a predefined default code '
            f'funcion, or as an `async-callable` `function` type, got {default_code_type.__name__}.')
    
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
        - If `annotation` was given as `type` instance, but that specfied type has no parser settings added to it.
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
        - If `annotation`'s setting allows flags, and given, but the given flags have no interseption with the allowed
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
                    f'allows: {setting.all_flags!r}. The two has no interseption.')
        else:
            new_flags = setting.default_flags
    
    else:
        if flags:
            raise TypeError(f'The annotation {annotation!r}\'s setting do not allows flags, meanwhile given: '
                f'{flags!r}.')
        
        new_flags = flags
    
    return new_flags

class FlaggedAnnotation(object):
    """
    Flagged annotation to store an annotation type with it's flags.
    
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
            - If `annotation` was given as `type` instance, but that specfied type has no parser settings added to it.
            - If `annotation` was given as `str` instance, but there is no added type representation to it.
        TypeError
            - If `annotation` was not given as `str`, neither as `type` instance.
            - If `flags` is not given as ``ConverterFlag`` instance, neither as `int`.
            - If `annotation`'s setting allows flags, and given, but the given flags have no interseption with the
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
    Yields the elements of the given `tuple`. If any of them is a `tuple` as well, then yields thats elements
    and repeat this cycle.
    
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
        if result_length<2:
            if result_length == 0:
                raise TypeError(f'`annotation` is given as a `tuple`, but it contains no real annotation, got '
                    f'{annotation!r}.')
            if result_length == 1:
                result = result[0]
    else:
        result = FlaggedAnnotation(annotation, flags=flags)
    
    return result


class Converter(object):
    """
    Represents a converter typehint for setting additional information for the parser.
    
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
    def __new__(cls, annotation, flags=None, default=_spaceholder, default_code=_spaceholder):
        """
        Creates a ``Converter`` instance with the given parameters.
        
        Parameters
        ----------
        annotation : `str`, `type`, ``Converter``, ``FlaggedAnnotation`` or `tuple` (repeat)
            The type or a typehint to what type the respective value should be converted.
        flags : ``ConverterFlag``, Optional
            Flags to use with the specified type's converter.
        default : `Any`, Optional
            Default object returned if conversion fails.
        default_code : `str` or `async-callable` `funciton`, Optional
            Default code, what will be called, when the conversion fails. Mutually exclusive with `default`.
        
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
            - If `default_code` is given as `function`, but accepts bad amount of arguments.
        """
        if (flags is not None):
           flags = preconvert_flag(flags, 'flags', ConverterFlag)
        
        annotation = validate_annotation(annotation, flags=flags)
        
        if (default is _spaceholder):
            default_type = DEFAULT_TYPE_NONE
            default_value = None
        else:
            default_type = DEFAULT_TYPE_OBJ
            default_value = default
        
        if (default_code is not _spaceholder):
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
        """Returns the converter's represnetation."""
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
                default_name = 'defeault'
            else:
                default_name = 'defualt_code'
            
            result.append(', ')
            result.append(default_name)
            result.append('=')
            result.append(repr(self.default))
        
        result.append(')')
        
        return ''.join(result)

class ContentParserArgumentHinter(object):
    """
    Hinter for content parser about it's arguments.
    
    Arguments
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
        Whether *args parser should be choosed.
    annotation : `None`, ``FlaggedAnnotation``, `tuple` of ``FlaggedAnnotation``
        The type of the parser to be choosed or a typehint about it.
    """
    __slots__ = ('default',  'default_type', 'annotation', 'is_args', )
    
    def __repr__(self):
        """Returns theh inter's represnetation."""
        return f'{self.__class__.__name__}(default={self.default!r}, default_type={self.default_type!r}, annotation=' \
            f'{self.annotation!r}, is_args={self.is_args!r})'

class CommandContentParser(object):
    """
    Content parser for commands.
    
    Parameters
    ----------
    _parsers : `None` or `list` of ``ParserContextBase`` instances
        The parsers of the command content parser. Set as`None` if it would be an empty `list`.
    """
    __slots__ = ('_parsers', )
    def __new__(cls, func):
        """
        Parameters
        ----------
        func : `async-callable`
            The callable function.
        
        Raises
        ------
        LookupError
            If `annotation` was given as `type` or `str` instance, but there is no parser for it.
        TypeError
            - If `func` is not given as `callable`
            - If `func` is not given as `async-callable`, and cannot be instanced to one neither.
            - If `func` (or it's converted form) accepts keyword only arguments.
            - If `func` (or it's converted form) accepts keyword **kwargs.
            - If `func` (or it's converted form) accepts less then 2 non reversed argument without *args.
            - If `func`'s (or it's converted form's) first argument has default value set.
            - If `func`'s (or it's converted form's) first argument has annotation set, but not as type ``Client``.
            - If `func`'s (or it's converted form's) second argument has default value set.
            - If `func`'s (or it's converted form's) second argument has annotation set, but not as type ``Message``.
            - If an argument has annotation as a ``Converter`` instance with default value, meanwhile the argument
                itself also has it's own default value.
            - If an annotation was given as `None` or as empty `tuple` meanwhile.
            - If an annotation was given as `tuple`, but any of it's element is not `None`, or `str`, `type` or `tuple`
                instance.
            - If `*args` argument's annotation was given as ``Converter`` instance with default value set.
        """
        analyzer = CallableAnalyzer(func)
        if analyzer.is_async():
            real_analyzer = analyzer
            should_instance = False
        
        elif analyzer.can_instance_to_async_callable():
            real_analyzer = CallableAnalyzer(func.__call__, as_method=True)
            if not real_analyzer.is_async():
                raise TypeError(f'`func` is not `async-callable` and cannot be instanced to `async` either, got '
                    f'{func!r}.')
            
            should_instance = True
        
        else:
            raise TypeError(f'`func` is not `async-callable` and cannot be instanced to `async` either, got {func!r}.')
        
        keyword_only_argument_count = real_analyzer.get_non_default_keyword_only_argument_count()
        if keyword_only_argument_count:
            raise TypeError(f'`{real_analyzer.real_function!r}` accepts keyword only arguments.')
        
        if real_analyzer.accepts_kwargs():
            raise TypeError(f'`{real_analyzer.real_function!r}` accepts **kwargs.')
        
        arguments = real_analyzer.get_non_reserved_positional_arguments()
        
        argument_count = len(arguments)
        if argument_count<2:
            raise TypeError(f'`{real_analyzer.real_function!r}` should accept at least 2 arguments (without *args): '
                f'`client` and `message`, meanwhile it accepts only {argument_count}.')
        
        client_argument = arguments[0]
        if client_argument.has_default:
            raise TypeError(f'`{real_analyzer.real_function!r}` has default argument set as it\'s first not '
                'reserved, meanwhile it should not have.')
        
        if client_argument.has_annotation and (client_argument.annoation is not Client):
            raise TypeError(f'`{real_analyzer.real_function!r}` has annotation at the client\'s argument slot, '
                f'what is not `{Client.__name__}`.')
        
        message_argument = arguments[1]
        if message_argument.has_default:
            raise TypeError(f'`{real_analyzer.real_function!r}` has default argument set as it\'s first not '
                f'reserved, meanwhile it should not have.')
        
        if message_argument.has_annotation and (message_argument.annoation is not Message):
            raise TypeError(f'`{real_analyzer.real_function!r}` has annotation at the message\'s argument slot '
                f'what is not `{Message.__name__}`.')
        
        hinters = []
        to_check = arguments[2:]
        args_argument = real_analyzer.args_argument
        
        index = 0
        limit = len(to_check)
        while True:
            if index == limit:
                break
            
            argument = to_check[index]
            index += 1
            
            if argument.has_annotation:
                annotation = argument.annotation
                if type(annotation) is Converter:
                    hinter_default = annotation.default
                    hinter_default_type = annotation.default_type
                    hinter_annotation = annotation.annotation
                
                    if argument.has_default:
                        if hinter_default_type:
                            raise TypeError(f'`annotation` of `{argument.name}` is given as '
                                f'`{Converter.__class__.__name__}` instance, as {Converter!r} (with default value '
                                f'set), meanwhile the argument has default value set as well: {argument.default!r}.')
                        
                        hinter_default = argument.default
                        hinter_default_type = DEFAULT_TYPE_OBJ
                
                else:
                    annotation = validate_annotation(annotation)
                    
                    if argument.has_default:
                        hinter_default = argument.default
                        hinter_default_type = DEFAULT_TYPE_OBJ
                    else:
                        hinter_default = None
                        hinter_default_type = DEFAULT_TYPE_NONE
                    
                    hinter_annotation = annotation
                
            else:
                if argument.has_default:
                    default = argument.default
                    if (index == limit) and (args_argument is None):
                        hinter_annotation = None
                    else:
                        hinter_annotation = FlaggedAnnotation(str)
                    
                    hinter_default = default
                    hinter_default_type = DEFAULT_TYPE_OBJ
                    
                else:
                    if (index == limit) and (args_argument is None):
                        hinter_annotation = None
                    else:
                        hinter_annotation = FlaggedAnnotation(str)
                    
                    hinter_default = None
                    hinter_default_type = DEFAULT_TYPE_NONE
            
            hinter = ContentParserArgumentHinter()
            hinter.default = hinter_default
            hinter.default_type = hinter_default_type
            hinter.annotation = hinter_annotation
            hinter.is_args = False
            hinters.append(hinter)
        
        if (args_argument is not None):
            annotation = args_argument.annotation
            if type(annotation) is Converter:
                if annotation.default_type:
                    raise TypeError(f'`*args` annotation is given as `{Converter.__class__.__name__} as '
                        f'{Converter!r}, so with default value set, do not do that!')
                
                hinter_annotation = annotation.annotation
            else:
                hinter_annotation = validate_annotation(annotation)
            
            hinter = ContentParserArgumentHinter()
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
            func = analyzer.instance_to_async_callable()
        
        self = object.__new__(cls)
        self._parsers = parsers
        return func, self
    
    async def get_args(self, client, message, content):
        """
        Parses the given content and returns whether it passed and what was parser.
        
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
            Whether the parsing all the arguments of the message succeeded.
        args : `None` or `list` of `Any`
            The parsed out entities. Can be empty list.
        """
        parsers = self._parsers
        if parsers is None:
            return True, None
        
        content_parser_context = ContentParserContext(client, message, content)
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

class ContentParser(CommandContentParser):
    """
    Represents a content parser, what can be used as a standalone wrapper of a function.
    
    Parameters
    ----------
    _parsers : `None` or `list` of ``ParserContextBase`` instances
        The parsers of the command content parser. Set as`None` if it would be an empty `list`.
    _func : `async-callable`
        The wrapped function.
    _handler : `None` or `async-callable`
        A coroutine function what is ensured, when parseing the arguments fail.
    _is_method : `bool`
        Whether the ``ContentParser`` should act like a method descriptor.
    """
    __slots__ = ('_func', '_handler', '_is_method',)
    def __new__(cls, func=None, handler=None, is_method=False):
        """
        Parameters
        ----------
        func : `None`, `async-callable` or instanceable to `async-callable`, Optional
        
        handler : `None`, `async-callable` or instanceable to `async-callable`, Optional
            An async callable, what is ensured when the parser's cannot parse all the required parameters out.
            
            If given, should accept the following arguments:
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
        
        Raises
        ------
        TypeError
            - If `is_method` is not given as `bool` instance.
            - If `handler` is not async, neither cannot be insatcned to async.
            - If `handler` (or it's converted form) would accept bad amount of arguents.
        """
        is_method = preconvert_bool(is_method, 'is_method')
        
        if (handler is not None):
            handler = check_argcount_and_convert(handler, 6,
                '`ContentParser` expects to pass `6` arguments to it\'s `handler`: client, message, content_parser, '
                'content, args, obj (can be `None`).')
        
        if func is None:
            return cls._wrapper(handler, is_method)
        
        self, func = CommandContentParser.__new__(cls, func)
        self._func = func
        self._handler = handler
        self._is_method = is_method
        return self
    
    class _wrapper(object):
        """
        A wrapper of ``ContentParser`` to allow using it as a decorator.
        
        Parameters
        ----------
        _handler : `None`, `async-callable`
            An async callable, what is ensured when the parser's cannot parse all the required parameters out.
            
            If given as not `None` should accept the following arguments:
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
        """
        __slots__ = ('_handler', '_is_method', )
        
        def __init__(self, handler, is_method):
            """
            Creates a new content parser wrapper.
            
            Parameters
            ----------
            handler : `None`, `async-callable`
                An async callable, what is ensured when the parser's cannot parse all the required parameters out.
                
                If given as not `None` should accept the following arguments:
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
            """
            self._handler = handler
            self._is_method = is_method
        
        def __call__(self, func):
            """
            Calls the content parser wrapper to create a ``ContentParser`` instance.
            
            Parameters
            ----------
            func : `async-callable` or instanceable to `async-callable`
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
            
            return ContentParser(func=func, handler=self._handler, is_method=self._is_method)
    
    async def __call__(self, *args):
        """
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
        
        If the contnet parser is not a method:
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
            Unexpected amount of arguments were passed.
        """
        # Parse out arguments.
        args_count = len(args)
        if self._is_method:
            if args_count < 3 or args_count > 4:
                raise TypeError(f'{self!r} expects 3-4 positional arguments to be given, got {args_count}.')
            
            if args_count == 3:
                parent, client, message = args
                content = ''
            else:
                parent, client, message, content = args
        else:
            if args_count < 2 or args_count > 3:
                raise TypeError(f'{self!r} expects 2-3 positional arguments to be given, got {args_count}.')
            
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
        func = self.func
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

    def __set__(self,obj,value):
        raise AttributeError('can\'t set attribute')

    def __delete__(self,obj):
        raise AttributeError('can\'t delete attribute')

class ContentParserMethod(MethodLike):
    """
    ``ContentParser``'s method wrapper.
    
    Attributes
    ----------
    __self__ : `Any`
        The object with what the method was called.
    _content_parser : ``ContentParser``
        The parent contnet parser, what was called as a method.
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
        """Retuns the wrapped function."""
        return self._content_parser._func
    
    async def __call__(self, *args):
        """
        Calls the content parser method.
        
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
            Unexpected amount of arguments were passed.
        """
        return self._content_parser(self.__self__, *args)
    
    @property
    def __module__(self):
        """Return the module of the wrapped function."""
        return self._content_parser._func.__module__
    
    def __getattr__(self, name):
        """Returns the wrapped function's attribute."""
        return getattr(self._content_parser._func, name)
    
    def __repr__(self):
        """Returns the method's rerpesnetation."""
        return f'{self.__class__.__name__}(content_parser={self._content_parser!r}, obj={self.__self__!r})'

del re
del FlagBase
