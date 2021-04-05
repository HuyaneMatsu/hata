# -*- coding: utf-8 -*-
import re
from datetime import timedelta

from ...backend.utils import cached_property, copy_docs, function
from ...backend.analyzer import CallableAnalyzer
from ...discord.utils import USER_MENTION_RP, ROLE_MENTION_RP, CHANNEL_MENTION_RP, ID_RP, parse_tdelta, parse_rdelta, \
    INVITE_CODE_RP, CHANNEL_MESSAGE_RP
from ...discord.bases import FlagBase
from ...discord.guild import Guild
from ...discord.client_core import USERS, CLIENTS, ROLES, CHANNELS, EMOJIS, GUILDS, MESSAGES
from ...discord.exceptions import DiscordException, ERROR_CODES
from ...discord.user import User, UserBase
from ...discord.channel import ChannelGuildBase, ChannelBase, ChannelTextBase, ChannelText, ChannelPrivate, \
    ChannelVoice, ChannelGroup, ChannelCategory, ChannelStore, ChannelThread, ChannelVoiceBase, ChannelStage
from ...discord.client import Client
from ...discord.emoji import Emoji, parse_emoji
from ...discord.invite import Invite
from ...discord.role import Role
from ...discord.color import Color, parse_color
from ...discord.http.URLS import MESSAGE_JUMP_URL_RP, INVITE_URL_PATTERN
from ...discord.message import Message

from ...env import CACHE_USER

try:
    from dateutil.relativedelta import relativedelta
except ImportError:
    relativedelta = None

from .utils import raw_name_to_display

NUMERIC_CONVERSION_LIMIT = 100

CONTENT_ARGUMENT_PARSERS = {}

DEFAULT_ARGUMENT_SEPARATOR = ('"', '"')
DEFAULT_ARGUMENT_ASSIGNER = ':'


class ContentParameterParserContextBase:
    """
    Parsing context returned by ``ContentParameterParser``.
    
    Attributes
    ----------
    _cache : `dict` of (`str`, `Any`)
        Cache used by cached properties.
    _parsed : re.Match
        The parsed regex.
    """
    __slots__ = ('_cache', '_parsed')
    def __new__(cls, parsed):
        """
        Creates a new ``ContentParameterParserContext`` instance with the given match.
        
        Parameters
        ----------
        parsed : re.Match
            The parsed regex.
        """
        self = object.__new__(cls)
        self._parsed = parsed
        self._cache = {}
        return self
    
    @property
    def has_keyword(self):
        """
        Returns whether keyword could be parsed.
        
        Returns
        -------
        has_keyword : `bool`
        """
        return (self.keyword is not None)
    
    @property
    def end(self):
        """
        Returns the end of the parsed region.
        
        Returns
        -------
        end : `str`
        """
        return self._parsed.end()
    
    @cached_property
    def whole(self):
        """
        Gets the whole parsed string part.
        
        Returns
        -------
        whole : `str`
        """
        return ''
    
    @cached_property
    def keyword(self):
        """
        Gets the parsed keyword from the parsed part.
        
        Returns
        -------
        keyword : `None` or `str`
        """
        return None
    
    @cached_property
    def value(self):
        """
        Returns the parsed value.
        
        Returns
        -------
        value : `str`
        """
        return ''

class ContentParameterParserContextSeparator(ContentParameterParserContextBase):
    """
    Separator pattern based parsing context returned by ``ContentParameterParser``.
    
    Attributes
    ----------
    _cache : `dict` of (`str`, `Any`)
        Cache used by cached properties.
    _parsed : re.Match
        The parsed regex.
    """
    __slots__ = ()
    
    @cached_property
    @copy_docs(ContentParameterParserContextBase.whole)
    def whole(self):
        return self._parsed.group(1)
    
    @cached_property
    @copy_docs(ContentParameterParserContextBase.keyword)
    def keyword(self):
        return self._parsed.group(2)
    
    @cached_property
    @copy_docs(ContentParameterParserContextBase.value)
    def value(self):
        return self._parsed.group(3)

class ContentParameterParserContextEncapsulator(ContentParameterParserContextBase):
    """
    Encapsulator pattern based parsing context returned by ``ContentParameterParser``.
    
    Attributes
    ----------
    _cache : `dict` of (`str`, `Any`)
        Cache used by cached properties.
    _parsed : re.Match
        The parsed regex.
    """
    __slots__ = ()
    
    @cached_property
    @copy_docs(ContentParameterParserContextBase.whole)
    def whole(self):
        parsed = self._parsed
        part = parsed.group(3)
        if part is None:
            part = parsed.group(2)
        
        return part
    
    @cached_property
    @copy_docs(ContentParameterParserContextBase.keyword)
    def keyword(self):
        return self._parsed.group(2)
    
    @cached_property
    @copy_docs(ContentParameterParserContextBase.value)
    def value(self):
        parsed = self._parsed
        part = parsed.group(3)
        if part is None:
            part = parsed.group(2)
        
        return part


class ContentParameterParser:
    """
    Content argument parser used inside of a ``ContentParserContext`` and stored by ``CommandContentParser``
    instances.
    
    Attributes
    ----------
    _context_class : ``ContentParameterParserContextBase``
        Context class to interact with the parsed string.
    _rp : `_sre.SRE_Pattern`
        The regex pattern what is passed and used by the caller.
    separator : `str` or `tuple` (`str`, `str`)
        The executed separator by the ``ContentParameterSeparator`` instance.
    """
    __slots__ = ('_context_class', '_rp', 'separator', 'assigner')
    def __new__(cls, separator, assigner):
        """
        Creates a new ``ContentParameterSeparator`` instance. If one already exists with the given parameters, returns
        that instead.
        
        Parameters
        ----------
        separator : `None`, `str`, `tuple` (`str`, `str`)
            The executed separator by the ``ContentParameterSeparator`` instance.
        assigner : `None`, `str`
            The assigner for keyword-only arguments.
        
        Raises
        ------
        TypeError
            - If `separator` is not given as `None`, `str`, neither as `tuple` instance.
            - If `separator` was given as `tuple`, but it's element are not `str` instances.
            - If `assigner` was not given neither as `None` or as `str` instance.
        ValueError
            - If `separator` is given as `str`, but it's length is not `1`.
            - If `separator` is given as `str`, but it is a space character.
            - If `separator` is given as `tuple`, but one of it's element's length is not `1`.
            - If `separator` is given as `tuple`, but one of it's element's is a space character.
            - If `assigner`'s length is not `1`.
        """
        if separator is None:
            separator = DEFAULT_ARGUMENT_SEPARATOR
            separator_type = type(separator)
        else:
            separator_type = type(separator)
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
                raise TypeError(f'`separator` can be given as `None`, `str` or as `tuple` instance, got '
                    f'{separator_type.__name__}.')
            
            if separator_type is str:
                if len(processed_separator) != 1:
                    raise ValueError(f'`str` separator length can be only `1`, got {separator!r}.')
                
                if processed_separator.isspace():
                    raise ValueError(f'`str` separator cannot be a space character`, meanwhile it is, got '
                        f'{separator!r}.')
                
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
                        raise ValueError(f'`tuple` separator\'s elements can be only `str` with length of `1`, '
                            f'meanwhile it\'s element under index `{index}` is not, got {element!r}.')
                    
                    if processed_element.isspace():
                        raise ValueError(f'`tuple` separator\'s elements cannot be space character`, meanwhile it\'s '
                            f'element under index `{index}` is, got {element!r}.')
                
                separator = tuple(processed_separator)
        
        if assigner is None:
            assigner = DEFAULT_ARGUMENT_ASSIGNER
        else:
            assigner_type = type(assigner)
            if assigner_type is str:
                pass
            elif issubclass(assigner_type, str):
                assigner = str(assigner)
            else:
                raise TypeError(f'`assigner` can be given as `None` or `str` instance, got {assigner_type.__name__}.')
        
        if len(assigner) != 1:
            raise ValueError(f'`assigner` length can be `1`, got {len(assigner)}; {assigner!r}.')
        
        try:
            return CONTENT_ARGUMENT_PARSERS[(separator, assigner)]
        except KeyError:
            pass
        
        assigner_escaped = re.escape(assigner)
        if separator_type is str:
            escaped_separator = re.escape(separator)
            rp = re.compile(f'[{escaped_separator}\s]*((?:([^\s{assigner_escaped}]+?)\s*{assigner_escaped}\s*)?(.+?))\s*(?:$|[{escaped_separator})]+)', re.M|re.S)
            
            context_class = ContentParameterParserContextSeparator
        else:
            start, end = separator
            if start == end:
                escaped_separator = re.escape(start)
                rp = re.compile(f'\s*(?:([^\s{assigner_escaped}]+?)\s*{assigner_escaped}\s*)?(?:(?:{escaped_separator}(.+?)(?:$|{escaped_separator}))|(?:(.+?)(?:$|[{escaped_separator}\s]+)))', re.M|re.S)
            
            else:
                separator_start_escaped = re.escape(start)
                separator_end_escaped = re.escape(end)
                rp = re.compile(f'\s*(?:([^\s{assigner_escaped}]+?)\s*{assigner_escaped}\s*)?(?:(?:{separator_start_escaped}(.+?)(?:$|{separator_end_escaped}))|(?:(.+?)(?:$|[{separator_start_escaped}\s]+)))', re.M|re.S)
            
            context_class = ContentParameterParserContextEncapsulator
        
        self = object.__new__(cls)
        self.separator = separator
        self._rp = rp
        self._context_class = context_class
        
        CONTENT_ARGUMENT_PARSERS[(separator, assigner)] = self
        return self
    
    def __call__(self, content, index):
        """
        Calls the content argument separator to get the next part of the given content.
        
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
        return self._context_class(self._rp.match(content, index))
    
    def __repr__(self):
        """Returns the content argument separator's representation."""
        return f'{self.__class__.__name__}({self.separator!r}, {self.assigner!r})'
    
    def __hash__(self):
        """Returns the content argument parser's hash."""
        return hash(self.separator) ^ hash(self.assigner)
    
    def __eq__(self, other):
        """Returns whether the two content argument separator are the same."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.separator != other.separator:
            return False
        
        if self.assigner != other.assigner:
            return False
        
        return True


DEFAULT_SEPARATOR = ContentParameterParser(DEFAULT_ARGUMENT_SEPARATOR, DEFAULT_ARGUMENT_ASSIGNER)


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
    
    Some parsers, like `int`, or `str` do not have any flags, what means, their behaviour cannot be altered.
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



CONVERTER_SETTING_TYPE_TO_SETTING = {}
CONVERTER_SETTING_NAME_TO_SETTING = {}
CONVERTER_NAME_TO_TYPE = {}


class ConverterSetting:
    """
    Store settings about a converter.
    
    Attributes
    ----------
    all_flags : ``ConverterFlag``
        All the flags which the converter picks up.
    alternative_type_name : `None` or `str`
        Alternative string name for the parser, which allows picking up a respective converter.
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
        if (converter_type is not function):
            raise TypeError(f'`converter` should have been given as `{function.__name__}` instance, got '
                f'{converter_type.__name__}.')
        
        analyzed = CallableAnalyzer(converter)
        if (not analyzed.is_async()):
            raise TypeError(f'`converter` should have been given as an async function instance, got '
                f'{converter!r}.')
        
        non_reserved_positional_argument_count = analyzed.get_non_reserved_positional_argument_count()
        if non_reserved_positional_argument_count != 3:
            raise TypeError(f'`converter` should accept `3` non reserved positional arguments, meanwhile it expects '
                f'{non_reserved_positional_argument_count}.')
        
        if analyzed.accepts_args():
            raise TypeError(f'`converter` should accept not expect args, meanwhile it does.')
        
        if analyzed.accepts_kwargs():
            raise TypeError(f'`converter` should accept not expect kwargs, meanwhile it does.')
        
        non_default_keyword_only_argument_count = analyzed.get_non_default_keyword_only_argument_count()
        if non_default_keyword_only_argument_count:
            raise TypeError(f'`converter` should accept `0` keyword only arguments, meanwhile it expects '
                f'{non_default_keyword_only_argument_count}.')
        
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
            CONVERTER_SETTING_TYPE_TO_SETTING[default_type] = self
            CONVERTER_SETTING_NAME_TO_SETTING[default_type.__name__] = self
            CONVERTER_NAME_TO_TYPE[default_type.__name__] = default_type
            
            if (alternative_type_name is not None):
                CONVERTER_SETTING_NAME_TO_SETTING[alternative_type_name] = self
                CONVERTER_NAME_TO_TYPE[alternative_type_name] = default_type
            
        if (alternative_types_processed is not None):
            for alternative_type in alternative_types_processed:
                CONVERTER_SETTING_TYPE_TO_SETTING[alternative_type] = self
                CONVERTER_SETTING_NAME_TO_SETTING[alternative_type.__name__] = self
                CONVERTER_NAME_TO_TYPE[alternative_type.__name__] = alternative_type
    
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
                    index += 1
                    
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


async def none_converter(command_context, content_parsing_parameter, content_parser_context):
    return None


CONVERTER_NONE = ConverterSetting(
    converter = none_converter,
    uses_flags = False,
    default_flags = ConverterFlag(),
    all_flags = ConverterFlag(),
    alternative_type_name = 'none',
    default_type = None,
    alternative_types = None,
        )


if CACHE_USER:
    async def user_converter(command_context, content_parser_context, content_parsing_parameter):
        part = content_parser_context.get_next()
        if (part is None):
            return None
        
        flags = content_parsing_parameter.flags
        message = command_context.message
        
        if flags&CONVERTER_FLAG_ID:
            parsed = ID_RP.fullmatch(part)
            if (parsed is not None):
                id_ = int(parsed.group(1))
                
                if flags&CONVERTER_FLAG_EVERYWHERE:
                    try:
                        user = USERS[id_]
                    except KeyError:
                        try:
                            user = await command_context.client.user_get(id_)
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
    async def user_converter(command_context, content_parser_context, content_parsing_parameter):
        part = content_parser_context.get_next()
        if (part is None):
            return None
        
        flags = content_parsing_parameter.flags
        message = command_context.message
        
        if flags&CONVERTER_FLAG_ID:
            parsed = ID_RP.fullmatch(part)
            if (parsed is not None):
                id_ = int(parsed.group(1))
                
                if flags&CONVERTER_FLAG_EVERYWHERE:
                    if flags&CONVERTER_FLAG_PROFILE:
                        guild = message.channel.guild
                        if (guild is not None):
                            try:
                                user = await command_context.client.guild_user_get(guild, id_)
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
                        user = await command_context.client.user_get(id_)
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
                            user = await command_context.client.guild_user_get(guild, id_)
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
                    user = await command_context.client.guild_user_search(guild, part)
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

async def client_converter(command_context, content_parser_context, content_parsing_parameter):
    part = content_parser_context.get_next()
    if (part is None):
        return None
    
    flags = content_parsing_parameter.flags
    message = command_context.message
    
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
            clients = list(CLIENTS)
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
                
                guild = message.channel.guild
                if (guild is not None):
                    for client in clients:
                        try:
                            guild_profile = client.guild_profiles[guild]
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

async def channel_converter(command_context, content_parser_context, content_parsing_parameter):
    part = content_parser_context.get_next()
    if (part is None):
        return None
    
    flags = content_parsing_parameter.flags
    channel_type = content_parsing_parameter.type
    message = command_context.message
    
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
        ChannelVoiceBase,
        ChannelText,
        ChannelPrivate,
        ChannelVoice,
        ChannelGroup,
        ChannelCategory,
        ChannelStore,
        ChannelThread,
        ChannelStage,
            ],
        )

async def role_converter(command_context, content_parser_context, content_parsing_parameter):
    part = content_parser_context.get_next()
    if (part is None):
        return None
    
    flags = content_parsing_parameter.flags
    message = command_context.message
    
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
    all_flags = ConverterFlag.role_all,
    alternative_type_name = 'role',
    default_type = Role,
    alternative_types = None,
        )

async def emoji_converter(command_context, content_parser_context, content_parsing_parameter):
    part = content_parser_context.get_next()
    if (part is None):
        return None
    
    flags = content_parsing_parameter.flags
    if flags&CONVERTER_FLAG_MENTION:
        emoji = parse_emoji(part)
        if (emoji is not None):
            return emoji
    
    message = command_context.message
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
                        emoji = guild.emojis[id_]
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
    all_flags = ConverterFlag.emoji_all,
    alternative_type_name = 'emoji',
    default_type = Emoji,
    alternative_types = None,
        )

async def guild_converter(command_context, content_parser_context, content_parsing_parameter):
    part = content_parser_context.get_next()
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
    
    if content_parsing_parameter.flags&CONVERTER_FLAG_EVERYWHERE:
        return guild
    
    if guild in command_context.client.guild_profiles:
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
async def _message_converter_m_id(command_context, content_parsing_parameter, message_id):
    message = MESSAGES.get(message_id)
    channel = command_context.message.channel
    if (message is not None):
        # Message found
        if content_parsing_parameter.flags&CONVERTER_FLAG_EVERYWHERE:
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
    client = command_context.client
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
async def _message_converter_cm_id(command_context, content_parsing_parameter, channel_id, message_id):
    channel = command_context.message.channel
    message = MESSAGES.get(message_id)
    if (message is not None):
        # Message found
        if content_parsing_parameter.flags&CONVERTER_FLAG_EVERYWHERE:
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

    if content_parsing_parameter.flags&CONVERTER_FLAG_EVERYWHERE:
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
        client = command_context.client
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

async def message_converter(command_context, content_parser_context, content_parsing_parameter):
    part = content_parser_context.get_next()
    if (part is None):
        return None
    
    if content_parsing_parameter.flags&CONVERTER_FLAG_ID:
        parsed = ID_RP.fullmatch(part)
        if (parsed is not None):
            message_id = int(parsed.group(1))
            return await _message_converter_m_id(command_context, content_parsing_parameter, message_id)
        
        parsed = CHANNEL_MESSAGE_RP.fullmatch(part)
        if (parsed is not None):
            channel_id, message_id = parsed.groups()
            channel_id = int(channel_id)
            message_id = int(message_id)
            return await _message_converter_cm_id(command_context, content_parsing_parameter, channel_id, message_id)
    
    if content_parsing_parameter.flags&CONVERTER_FLAG_URL:
        parsed = MESSAGE_JUMP_URL_RP.fullmatch(part)
        if (parsed is not None):
            _, channel_id, message_id = parsed.groups()
            channel_id = int(channel_id)
            message_id = int(message_id)
            return await _message_converter_cm_id(command_context, content_parsing_parameter, channel_id, message_id)
    
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

async def invite_converter(command_context, content_parser_context, content_parsing_parameter):
    part = content_parser_context.get_next()
    if (part is None):
        return None
    
    flags = content_parsing_parameter.flags
    
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
        invite = await command_context.client.invite_get(code)
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


async def color_converter(command_context, content_parser_context, content_parsing_parameter):
    part = content_parser_context.get_next()
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


async def str_converter(command_context, content_parser_context, content_parsing_parameter):
    return content_parser_context.get_next()

ConverterSetting(
    converter = str_converter,
    uses_flags = False,
    default_flags = ConverterFlag(),
    all_flags = ConverterFlag(),
    alternative_type_name = None,
    default_type = str,
    alternative_types = None,
        )


async def int_converter(command_context, content_parser_context, content_parsing_parameter):
    part = content_parser_context.get_next()
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

async def tdelta_converter(command_context, content_parser_context, content_parsing_parameter):
    part = content_parser_context.get_next()
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
    async def rdelta_converter(command_context, content_parser_context, content_parsing_parameter):
        part = content_parser_context.get_next()
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


class ContentParserParameter:
    """
    Represents a parameter to parse.
    
    Parameters
    ---------
    annotation_name : `None` or `str`
        Identifier of the respective parser if any.
    annotation_type : `None` or `type` instance
        The type or subtype of the annotation to parse.
    converter : `async-function`
        The function used to parse the parameter.
    converter_setting : ``ConverterSetting``
        The converter setting used by the parameter.
    default : `None` or `Any`
        Default value to the parser
    has_default : `bool`
        Whether the parser has default value.
    default : `None` or `Any`
        The default object to return if the parser fails.
    description : `None` or `str`
        The description of the parameter if any.
    display_name : `str`
        The parameter's display name.
    flags : ``ConverterFlag``
        Converter flags to customize the parsers
    has_default : `bool`
        Whether the parameter has default value set.
    index : `int`
        The parameter's index.
    is_args : `bool`
        Whether the parameter is `*args` parameter.
    is_keyword : `bool`
        Whether the parameter is keyword only parameter.
    is_kwargs : `bool`
        Whether the parameter is `**kwargs` parameter.
    is_positional : `bool`
        Whether the parameter is positional.
    name : `str`
        The parameter's name.
    """
    __slots__ = ('annotation_name', 'annotation_type', 'converter', 'converter_setting', 'default', 'description',
        'display_name', 'flags', 'has_default', 'index', 'is_args', 'is_keyword', 'is_kwargs', 'is_positional', 'name')
    
    def __new__(cls, parameter, index):
        """
        Creates a new ``ContentParserParameter`` with the given parameters.
        
        Parameters
        ----------
        parameter : ``Argument``
            The analyzed parameter to process.
        index : `int`
            The parameter's index.
        
        Raises
        ------
        TypeError
            - If `annotation`'s type is invalid.
            - If `description`'s type is invalid.
            - If `name`'s type is invalid.
        ValueError
            - There is no converter for the given `annotation`.
            - The `annotation` is a `tuple`, but it's length is not 2 or 3.
        """
        display_name = parameter.name
        
        if parameter.has_annotation:
            annotation = parameter.annotation
            if annotation is None:
                description = None
                converter_setting = CONVERTER_NONE
                annotation_name = converter_setting.alternative_type_name
                annotation_type = converter_setting.default_type
            
            elif isinstance(annotation, type):
                try:
                    converter_setting = CONVERTER_SETTING_TYPE_TO_SETTING[annotation]
                except KeyError:
                    raise ValueError(f'There is no converter registered for {annotation!r}.') from None
                
                description = None
                annotation_name = converter_setting.alternative_type_name
                annotation_type = annotation
            
            elif isinstance(annotation, str):
                # Make sure
                if type(annotation) is not str:
                    annotation = str
                
                try:
                    converter_setting = CONVERTER_SETTING_NAME_TO_SETTING[annotation]
                except KeyError:
                    raise ValueError(f'There is no converter registered for {annotation!r}.') from None
                
                description = None
                annotation_name = converter_setting.alternative_type_name
                annotation_type = CONVERTER_NAME_TO_TYPE.get(annotation)
            
            elif isinstance(annotation, tuple):
                if type(annotation) is not tuple:
                    annotation = tuple(annotation)
                
                annotation_length = len(annotation)
                if annotation_length not in (2, 3):
                    raise ValueError(f'`tuple` annotation\'s length can be either `2` or `3`, got '
                        f'{annotation_length!r}: {annotation!r}')
                
                annotation_tuple_type = annotation[0]
                if annotation_tuple_type is None:
                    converter_setting = CONVERTER_NONE
                    annotation_name = converter_setting.alternative_type_name
                    annotation_type = converter_setting.default_type
                
                elif isinstance(annotation_tuple_type, type):
                    try:
                        converter_setting = CONVERTER_SETTING_TYPE_TO_SETTING[annotation_tuple_type]
                    except KeyError:
                        raise ValueError(f'There is no converter registered for {annotation_tuple_type!r}.') from None
                    
                    annotation_name = converter_setting.alternative_type_name
                    annotation_type = annotation_tuple_type
                
                elif isinstance(annotation_tuple_type, str):
                    # Make sure
                    if type(annotation_tuple_type) is not str:
                        annotation_tuple_type = str
                    
                    try:
                        converter_setting = CONVERTER_SETTING_NAME_TO_SETTING[annotation_tuple_type]
                    except KeyError:
                        raise ValueError(f'There is no converter registered for {annotation_tuple_type!r}.') from None
                    
                    annotation_name = converter_setting.alternative_type_name
                    annotation_type = CONVERTER_NAME_TO_TYPE.get(annotation_tuple_type)
                
                else:
                    raise TypeError(f'`annotation` was given as `tuple`, but it\'s 0th element was not given as any '
                        f'of the expected values: `None`, `type` or `str` instance, got '
                        f'{annotation_tuple_type.__class__.__name__}; {annotation_tuple_type!r}.')
                
                
                annotation_tuple_description = annotation[1]
                if type(annotation_tuple_description) is str:
                    description = annotation_tuple_description
                elif isinstance(annotation_tuple_description, str):
                    description = str(annotation_tuple_description)
                else:
                    raise TypeError(f'`annotation` description can be `str` instance, got '
                        f'{annotation_tuple_description.__class__.__name__}.')
                
                
                if annotation_length == 3:
                    annotation_tuple_name = annotation[2]
                    if type(annotation_tuple_name) is str:
                        display_name = annotation_tuple_name
                    elif isinstance(annotation_tuple_name, str):
                        display_name = str(annotation_tuple_name)
                    else:
                        raise TypeError(f'`annotation` name can be `str` instance, got '
                            f'{annotation_tuple_name.__class__.__name__}.')
                
            else:
                raise TypeError(f'`annotation` can be either given as `None`, `type`, `str` or `tuple`, got '
                    f'{annotation.__class__.__name__}; {annotation!r}.')
            
        else:
            description = None
            converter_setting = CONVERTER_NONE
            annotation_name = converter_setting.alternative_type_name
            annotation_type = converter_setting.default_type
        
        display_name = raw_name_to_display(display_name)
        
        has_default = parameter.has_default
        if has_default:
            default = parameter.default
        else:
            default = None
        
        converter = converter_setting.converter
        
        is_positional = parameter.is_positional()
        is_keyword = parameter.is_keyword_only()
        is_args = parameter.is_args()
        is_kwargs = parameter.is_kwargs()
        
        self = object.__new__(cls)
        self.annotation_name = annotation_name
        self.annotation_type = annotation_type
        self.converter = converter
        self.converter_setting = converter_setting
        self.default = default
        self.description = description
        self.display_name = display_name
        self.flags = flags
        self.has_default = has_default
        self.index = index
        self.is_args = is_args
        self.is_keyword = is_keyword
        self.is_kwargs = is_kwargs
        self.is_positional = is_positional
        self.name = name
        return self
    
    def __repr__(self):
        """Returns the inter's representation."""
        result = ['<', self.__class__.__name__,
            ' name=', repr(self.name),
            ', annotation=', repr(self.annotation),
                 ]
        
        if self.has_default:
            result.append(', default=')
            result.append(repr(self.default))
        
        result.append('>')
        return ''.join(result)


COMMAND_CONTENT_PARSER_POST_PROCESSORS = []

class CommandContentParser:
    """
    Content parser for commands.
    
    Attributes
    ----------
    _parameters : `list` of ``ContentParserParameter``
        The parameters of the respective function.
    _content_parameter_parser : ``ContentParameterParser``
        The argument separator of the parser.
    """
    __slots__ = ('_content_parameter_parser', '_parameters',)
    
    def __new__(cls, func, separator, assigner):
        """
        Creates a new ``CommandContentParser`` instance returning the parser for teh function and the function itself
        as well.
        
        Parameters
        ----------
        func : `async-callable`
            The callable function.
        separator : `None`, ``ContentParameterSeparator``, `str` or `tuple` (`str`, `str`)
            The argument separator of the parser.
        
        Returns
        -------
        self : ``CommandContentParser``
            The created parser.
        func : `async-callable`
            The function to which teh parser is created for.
        
        Raises
        ------
        TypeError
            - If `separator` is not given as `None`, `str`, neither as `tuple` instance.
            - If `separator` was given as `tuple`, but it's element are not `str` instances.
            - If `assigner` was not given neither as `None` or as `str` instance.
            - If an `annotation`'s type is invalid.
            - If a `description`'s type is invalid.
            - If a `name`'s type is invalid.
            - If `func` is not `async-callable` and cannot instanced into `async-callable` either.
        ValueError
            - If `separator` is given as `str`, but it's length is not `1`.
            - If `separator` is given as `str`, but it is a space character.
            - If `separator` is given as `tuple`, but one of it's element's length is not `1`.
            - If `separator` is given as `tuple`, but one of it's element's is a space character.
            - If `assigner`'s length is not `1`.
            - There is no converter for a given `annotation`.
            - The an `annotation` is a `tuple`, but it's length is not 2 or 3.
        """
        content_parameter_parser = ContentParameterParser(separator, assigner)
        
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
        
        parameters = []
        
        index = 0
        for argument in real_analyzer.arguments:
            if not argument.reserved:
                content_parser_parameter = ContentParserParameter(argument, index)
                parameters.append(content_parser_parameter)
                index += 1
        
        if should_instance:
            func = analyzer.insatnce()
    
        self = object.__new__(cls)
        self._parameters = parameters
        self._content_parameter_parser = content_parameter_parser
        return self, func



