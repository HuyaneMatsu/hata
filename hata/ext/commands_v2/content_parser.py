__all__ = ('ConverterFlag', )

import re
from datetime import timedelta
from types import FunctionType

from scarletio import CallableAnalyzer, RichAttributeErrorBaseType, cached_property, copy_docs

from ...discord.bases import FlagBase
from ...discord.channel import Channel
from ...discord.client import Client
from ...discord.color import Color, parse_color
from ...discord.core import CHANNELS, CLIENTS, EMOJIS, GUILDS, MESSAGES, ROLES, USERS
from ...discord.emoji import Emoji, parse_emoji
from ...discord.exceptions import DiscordException, ERROR_CODES
from ...discord.guild import Guild
from ...discord.http import INVITE_URL_RP, MESSAGE_JUMP_URL_RP
from ...discord.invite import Invite
from ...discord.message import Message
from ...discord.role import Role, parse_role_mention
from ...discord.sticker import Sticker
from ...discord.user import User, UserBase
from ...discord.utils import (
    CHANNEL_MENTION_RP, CHANNEL_MESSAGE_RP, ID_RP, INVITE_CODE_RP, USER_MENTION_RP, parse_rdelta, parse_tdelta
)
from ...env import CACHE_USER

from .context import CommandContext
from .exceptions import CommandParameterParsingError
from .utils import raw_name_to_display


try:
    from dateutil.relativedelta import relativedelta
except ImportError:
    relativedelta = None


NUMERIC_CONVERSION_LIMIT = 100

CONTENT_ARGUMENT_PARSERS = {}

DEFAULT_PARAMETER_SEPARATOR = ('"', '"')
DEFAULT_PARAMETER_ASSIGNER = ':'


class ContentParameterParserContextBase(RichAttributeErrorBaseType):
    """
    Parsing context returned by ``ContentParameterParser``.
    
    Attributes
    ----------
    _cache : `dict` of (`str`, `Any`)
        Cache used by cached properties.
    _parsed : `re.Match`
        The parsed regex.
    """
    __slots__ = ('_cache', '_parsed')
    
    def __new__(cls, parsed):
        """
        Creates a new ``ContentParameterParserContext`` with the given match.
        
        Parameters
        ----------
        parsed : `re.Match`
            The parsed regex.
        """
        self = object.__new__(cls)
        self._parsed = parsed
        self._cache = {}
        return self
    
    
    def __repr__(self):
        """Returns the content parameter parser context's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' parsed=')
        repr_parts.append(repr(self._parsed))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two content parameter parser contexts are the same"""
        if type(self) is not type(other):
            return NotImplemented
        
        if self._parsed != other._parsed:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the content parameter parser context's hash value."""
        return hash(self._parsed)
    
    
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
        keyword : `None`, `str`
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
    _parsed : `re.Match`
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
    _parsed : `re.Match`
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
        return self._parsed.group(1)
    
    
    @cached_property
    @copy_docs(ContentParameterParserContextBase.value)
    def value(self):
        parsed = self._parsed
        part = parsed.group(3)
        if part is None:
            part = parsed.group(2)
        
        return part


class ContentParameterParser(RichAttributeErrorBaseType):
    """
    Content parameter parser used inside of a ``ContentParameterParserContext`` and stored by ``CommandContentParser``
    instances.
    
    Attributes
    ----------
    _context_class : ``ContentParameterParserContextBase``
        Context class to interact with the parsed string.
    _rp : `_sre.SRE_Pattern`
        The regex pattern what is passed and used by the caller.
    assigner : `str`
        Assigner executed by the ``ContentParameterParser``.
    separator : `str`, `tuple` (`str`, `str`)
        The executed separator by the ``ContentParameterParser``.
    """
    __slots__ = ('_context_class', '_rp', 'assigner', 'separator')
    
    def __new__(cls, separator, assigner):
        """
        Creates a new ``ContentParameterSeparator``. If one already exists with the given parameters, returns
        that instead.
        
        Parameters
        ----------
        separator : `None`, `str`, `tuple` (`str`, `str`)
            The executed separator by the ``ContentParameterSeparator``.
        assigner : `None`, `str`
            The assigner for keyword-only parameters.
        
        Raises
        ------
        TypeError
            - If `separator` is not given as `None`, `str`, neither as `tuple`.
            - If `separator` was given as `tuple`, but it's element are not `str`-s.
            - If `assigner` was not given neither as `None`, `str`.
        ValueError
            - If `separator` is given as `str`, but it's length is not `1`.
            - If `separator` is given as `str`, but it is a space character.
            - If `separator` is given as `tuple`, but one of it's element's length is not `1`.
            - If `separator` is given as `tuple`, but one of it's element's is a space character.
            - If `assigner`'s length is not `1`.
        """
        if separator is None:
            separator = DEFAULT_PARAMETER_SEPARATOR
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
                raise TypeError(
                    f'`separator` can be `None`, `str`, `tuple`, got {separator_type.__name__}; {separator!r}.'
                )
            
            if separator_type is str:
                if len(processed_separator) != 1:
                    raise ValueError(
                        f'`str` separator length can be only `1`, got {len(processed_separator)!r}; {separator!r}.'
                    )
                
                if processed_separator.isspace():
                    raise ValueError(
                        f'`str` separator cannot be a space character, got {separator!r}.'
                    )
                
                separator = processed_separator
            
            else:
                if len(processed_separator) != 2:
                    raise ValueError(
                        f'`tuple` separator length can be only `2`, got {len(processed_separator)!r}; {separator!r}.'
                    )
                
                for index in range(2):
                    element = processed_separator[index]
                    
                    element_type = element.__class__
                    if element_type is str:
                        processed_element = element
                    elif issubclass(element_type, str):
                        processed_element = str(element)
                        processed_separator[index] = processed_element
                    else:
                        raise TypeError(
                            f'`separator[{index}]` is not `str` as expected, got {element_type.__name__};'
                            f' {element}; separator={processed_separator!r}.'
                        )
                    
                    if len(processed_element) != 1:
                        raise ValueError(
                            f'`separator[{index}]` length should have been `1`, got {len(processed_element)}; '
                            f'{processed_element!r}; separator={processed_separator!r}.'
                        )
                    
                    if processed_element.isspace():
                        raise ValueError(
                            f'`separator[{index}]` cannot be a space character, got {len(processed_element)}; '
                            f'{processed_element!r}; separator={processed_separator!r}.'
                        )
                
                separator = tuple(processed_separator)
        
        if assigner is None:
            assigner = DEFAULT_PARAMETER_ASSIGNER
        else:
            assigner_type = type(assigner)
            if assigner_type is str:
                pass
            elif issubclass(assigner_type, str):
                assigner = str(assigner)
            else:
                raise TypeError(
                    f'`assigner` can be `None`, `str`, got {assigner_type.__name__}; {assigner!r}.'
                )
        
        if len(assigner) != 1:
            raise ValueError(
                f'`assigner` length can be `1`, got {len(assigner)}; {assigner!r}.'
            )
        
        try:
            return CONTENT_ARGUMENT_PARSERS[(separator, assigner)]
        except KeyError:
            pass
        
        assigner_escaped = re.escape(assigner)
        if separator_type is str:
            escaped_separator = re.escape(separator)
            rp = re.compile(f'[{escaped_separator}\s]*((?:([^\s{assigner_escaped}]+?)\s*{assigner_escaped}\s+)?(.+?))\s*(?:$|[{escaped_separator})]+)', re.M | re.S)
            
            context_class = ContentParameterParserContextSeparator
        else:
            start, end = separator
            if start == end:
                escaped_separator = re.escape(start)
                rp = re.compile(f'\s*(?:([^\s{assigner_escaped}]+?)\s*{assigner_escaped}\s+)?(?:(?:{escaped_separator}(.+?)(?:$|{escaped_separator}))|(?:(.+?)(?:$|[{escaped_separator}\s]+)))', re.M | re.S)
            
            else:
                separator_start_escaped = re.escape(start)
                separator_end_escaped = re.escape(end)
                rp = re.compile(f'\s*(?:([^\s{assigner_escaped}]+?)\s*{assigner_escaped}\s+)?(?:(?:{separator_start_escaped}(.+?)(?:$|{separator_end_escaped}))|(?:(.+?)(?:$|[{separator_start_escaped}\s]+)))', re.M | re.S)
            
            context_class = ContentParameterParserContextEncapsulator
        
        self = object.__new__(cls)
        self.assigner = assigner
        self.separator = separator
        self._rp = rp
        self._context_class = context_class
        
        CONTENT_ARGUMENT_PARSERS[(separator, assigner)] = self
        return self
    
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
        keyword : `None`, `str`
            The parsed out part's keyword if any.
        value : `str`
            The parsed out value.
        end : `int`
            The index where the next parsing should start from.
        """
        context = self._context_class(self._rp.match(content, index))
        return context.keyword, context.value, context.end
    
    def __repr__(self):
        """Returns the content parameter separator's representation."""
        return f'{self.__class__.__name__}({self.separator!r}, {self.assigner!r})'
    
    def __hash__(self):
        """Returns the content parameter parser's hash."""
        return hash(self.separator) ^ hash(self.assigner)
    
    def __eq__(self, other):
        """Returns whether the two content parameter separator are the same."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.separator != other.separator:
            return False
        
        if self.assigner != other.assigner:
            return False
        
        return True


DEFAULT_SEPARATOR = ContentParameterParser(DEFAULT_PARAMETER_SEPARATOR, DEFAULT_PARAMETER_ASSIGNER)


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
    user : `None`, ``UserBase``
    """
    user_mentions = message.user_mentions
    if user_mentions is None:
        return
    
    parsed = USER_MENTION_RP.fullmatch(part)
    if parsed is None:
        return
    
    user_id = int(parsed.group(1))
    return USERS.get(user_id, None)


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
    channel : `None`, ``Channel``
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

REST_PARSER_RP = re.compile('\s*(.*?)\s*', re.M | re.S)


def parse_rest_content(content, index):
    """
    Parses everything till the content's end.
    
    Parameters
    ----------
    content : `str`
        A message's content after a respective prefix.
    index : `int`
        The start till we should cut down the content.
    
    Returns
    -------
    rest : `str`
        The content's end.
    """
    return REST_PARSER_RP.fullmatch(content, index).group(1)


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
    | sticker_default   | name, id                                  |
    +-------------------+-------------------------------------------+
    | sticker_all       | name, id, everywhere                      |
    +-------------------+-------------------------------------------+
    
    Note, if you use for example a `'user'` parser, then by default it will use the `user_default` flags, and it
    will ignore everything else, than `user_all`.
    
    Some parsers, like `int` / `str` do not have any flags, what means, their behaviour cannot be altered.
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
    sticker_default = NotImplemented
    sticker_all = NotImplemented

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
ConverterFlag.message_default = ConverterFlag().update_by_keys(url = True, id=True)
ConverterFlag.message_all = ConverterFlag.message_default.update_by_keys(everywhere=True)
ConverterFlag.invite_default = ConverterFlag().update_by_keys(url = True, id=True)
ConverterFlag.invite_all = ConverterFlag.invite_default
ConverterFlag.sticker_default = ConverterFlag().update_by_keys(name=True, id=True)
ConverterFlag.sticker_all = ConverterFlag.sticker_default.update_by_keys(everywhere=True)


CONVERTER_FLAG_URL = 1 << ConverterFlag.__keys__['url']
CONVERTER_FLAG_MENTION = 1 << ConverterFlag.__keys__['mention']
CONVERTER_FLAG_NAME = 1 << ConverterFlag.__keys__['name']
CONVERTER_FLAG_ID = 1 << ConverterFlag.__keys__['id']
CONVERTER_FLAG_EVERYWHERE = 1 << ConverterFlag.__keys__['everywhere']
CONVERTER_FLAG_PROFILE = 1 << ConverterFlag.__keys__['profile']



CONVERTER_SETTING_TYPE_TO_SETTING = {}
CONVERTER_SETTING_NAME_TO_SETTING = {}
CONVERTER_NAME_TO_TYPE = {}


class ConverterSetting(RichAttributeErrorBaseType):
    """
    Store settings about a converter.
    
    Attributes
    ----------
    all_flags : ``ConverterFlag``
        All the flags which the converter picks up.
    alternative_checked_types : `None`, `dict` of (`str`, `callable`) items
        Alternative string names to checkers.
    alternative_type_name : `None`, `str`
        Alternative string name for the parser, which allows picking up a respective converter.
    alternative_types : `None`, `list` of `type`
        Alternative type specifications, which are supported by the parser.
    converter : `FunctionType`
        The converter coroutine function.
    default_flags : ``ConverterFlag``
        The default flags with what the converter will be used if not defining any specific.
    default_type : `None`, `type`
        The default annotation type of the converter.
    requires_part : `bool`
        Whether the converter requires data to parse or it just produces it's result on the fly.
    uses_flags : `bool`
        Whether the converter processes any flags.
    """
    __slots__ = (
        'all_flags', 'alternative_checked_types', 'alternative_type_name', 'alternative_types', 'converter',
        'default_flags', 'default_type', 'requires_part', 'uses_flags'
    )
    
    def __new__(cls, converter, uses_flags, default_flags, all_flags, alternative_type_name, default_type,
            alternative_types, requires_part, *, alternative_checked_types = None):
        """
        Creates a new ``ConverterSetting`` to store settings related to a converter function.
        
        Parameters
        ----------
        converter : `FunctionType`
            The converter coroutine function.
        uses_flags : `bool`
            Whether the converter processes any flags.
        default_flags : ``ConverterFlag``
            The default flags with what the converter will be used if not defining any specific.
        all_flags : ``ConverterFlag``
             All the flags which the converter picks up.
        alternative_type_name : `None`, `str`
            Alternative string name for the parser, what allows picking up a respective converter.
        default_type : `None`, `type`
            The default annotation type of the converter.
        alternative_types : `None` `iterable` of `type`
            A list of the alternatively accepted types.
        requires_part : `bool`
            Whether the converter requires data to parse or it just produces it's result on the fly.
        alternative_checked_types : `None`, `dict` of (`str`, `callable`) items, Optional (Keyword only)
            Alternative `type-name` - `checker` pairs.
        
        Raises
        -------
        TypeError
            - If any parameter's type is incorrect.
        ValueError
            - If `uses_flags` is given as `true`, but at the same time `all_flags` was not given as
            `ConverterFlag(0)`
        """
        if not isinstance(converter, FunctionType):
            raise TypeError(
                f'`converter` can be `{FunctionType.__name__}`, got '
                f'{converter.__class__.__name__}; {converter!r}.'
            )
        
        if type(requires_part) is not bool:
            raise TypeError(
                f'`requires_part` can be `bool`, got {requires_part.__class__.__name__}; {requires_part!r}.'
            )
        
        analyzed = CallableAnalyzer(converter)
        if (not analyzed.is_async()):
            raise TypeError(
                f'`converter` can be an async function, got {converter!r}.'
            )
        
        non_reserved_positional_parameter_count = analyzed.get_non_reserved_positional_parameter_count()
        if non_reserved_positional_parameter_count != (3 if requires_part else 2):
            raise TypeError(
                f'`converter` should accept `3` (or 2 if `requires_part` is `False`) non reserved '
                f'positional parameters , meanwhile it expects {non_reserved_positional_parameter_count}, got '
                f'{converter!r}.'
            )
        
        if analyzed.accepts_args():
            raise TypeError(
                f'`converter` should accept not expect args, meanwhile it does, got {converter!r}.'
            )
        
        if analyzed.accepts_kwargs():
            raise TypeError(
                f'`converter` should accept not expect kwargs, meanwhile it does, got {converter!r}.'
            )
        
        non_default_keyword_only_parameter_count = analyzed.get_non_default_keyword_only_parameter_count()
        if non_default_keyword_only_parameter_count:
            raise TypeError(
                f'`converter` should accept `0` keyword only parameters, meanwhile it expects '
                f'{non_default_keyword_only_parameter_count}, got {converter!r}.'
            )
        
        if type(uses_flags) is not bool:
            raise TypeError(
                f'`uses_flags` can be `bool`, got {uses_flags.__class__.__name__}; {uses_flags!r}.'
            )
        
        if type(default_flags) is not ConverterFlag:
            raise TypeError(
                f'`default_flags` can be `{ConverterFlag.__name__}`, got '
                f'{default_flags.__class__.__name__}; {default_flags!r}.'
            )
        
        if type(all_flags) is not ConverterFlag:
            raise TypeError(
                f'`all_flags` can be `{ConverterFlag.__name__}`, got '
                f'{all_flags.__class__.__name__}; {all_flags!r}.'
            )
        
        if (alternative_type_name is not None) and (type(alternative_type_name) is not str):
            raise TypeError(
                f'`alternative_type_name` can be `None`, `str`, got '
                f'{alternative_type_name.__class__.__name__}; {alternative_type_name!r}.'
            )
        
        if (default_type is not None) and (not isinstance(default_type, type)):
            raise TypeError(
                f'`default_type` can be `None`, `type`, got '
                f'{default_type.__class__.__name__}; {default_type!r}.'
            )
        
        if (alternative_types is None):
            alternative_types_processed = None
        
        else:
            alternative_types_type = type(alternative_types)
            if not hasattr(alternative_types_type, '__iter__'):
                raise TypeError(
                    f'`alternative_types` can be `None`, `iterable` of `type`, got '
                    f'{alternative_types_type.__name__}; {alternative_types_type!r}.'
                )
            
            alternative_types_processed = []
            
            index = 1
            for alternative_type in alternative_types:
                if not isinstance(alternative_type, type):
                    raise TypeError(
                        f'`alternative_types[{index}]` can be `type`, got {alternative_type.__class__.__name__}; '
                        f'{alternative_type!r}; alternative_types = {alternative_types!r}.'
                    )
                
                alternative_types_processed.append(alternative_type)
                index += 1
            
            if not alternative_types_processed:
                 alternative_types_processed = None
        
        if (not uses_flags) and all_flags:
            raise ValueError(
                f'If `uses_flags` is given as `true`, then `all_flags` should be given as '
                f'`{ConverterFlag.__name__}(0)`, got {all_flags!r}.'
            )
        
        
        if (alternative_checked_types is None):
            alternative_checked_types_processed = None
        
        else:
            if not isinstance(alternative_checked_types, dict):
                raise TypeError(
                    f'`alternative_checked_types` can be `dict`, got {alternative_checked_types.__class__.__name__}; '
                    f'{alternative_checked_types!r}.'
                )
            
            alternative_checked_types_processed = {}
            
            for key, value in alternative_checked_types.items():
                if not isinstance(key, str):
                    raise TypeError(
                        f'`alternative_checked_types`\'s keys can be `str`, got {key.__class__.__name__}; {key!r}.'
                    )
                
                if not callable(value):
                    raise TypeError(
                        f'`alternative_checked_types`\'s values can be `callable`, got '
                        f'{key.__class__.__name__}; {key!r}.'
                    )
                
                alternative_checked_types_processed[key] = value
            
            
            if not alternative_checked_types_processed:
                alternative_checked_types_processed = None
        
        
        self = object.__new__(cls)
        self.converter = converter
        self.uses_flags = uses_flags
        self.default_flags = default_flags
        self.all_flags = all_flags
        self.alternative_type_name = alternative_type_name
        self.default_type = default_type
        self.alternative_types = alternative_types_processed
        self.requires_part = requires_part
        self.alternative_checked_types = alternative_checked_types_processed
        
        
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
        
        if (alternative_checked_types_processed is not None):
            for alternative_type_name in alternative_checked_types_processed.keys():
                CONVERTER_SETTING_NAME_TO_SETTING[alternative_type_name] = self
        
        
        return self
    
    def __repr__(self):
        """Returns the converter setting's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
            ' converter=',
            self.converter.__name__,
        ]
        
        default_type = self.default_type
        if default_type is None:
            alternative_type_name = self.alternative_type_name
            if (alternative_type_name is not None):
                repr_parts.append(', alternative_type_name=')
                repr_parts.append(repr(alternative_type_name))
        else:
            default_type_name = default_type.__name__
            repr_parts.append(', default_type=')
            repr_parts.append(default_type_name)
            
            
            alternative_type_name = self.alternative_type_name
            if alternative_type_name != default_type_name:
                repr_parts.append(', alternative_type_name=')
                repr_parts.append(repr(alternative_type_name))
            
            
            alternative_checked_types = self.alternative_checked_types
            if (alternative_checked_types is not None):
                alternative_checked_types_names = list(alternative_checked_types.keys())
                
                repr_parts.append(', alternative_checked_types = [')
                
                index = 0
                limit = len(alternative_checked_types_names)
                while True:
                    alternative_checked_types_name= alternative_checked_types_names[index]
                    index += 1
                    
                    repr_parts.append(alternative_checked_types_name)
                    
                    if index == limit:
                        break
                    
                    repr_parts.append(', ')
                    continue
                
                repr_parts.append(']')
            
            
            alternative_types = self.alternative_types
            if (alternative_types is not None):
                repr_parts.append(', alternative_types = [')
                
                index = 0
                limit = len(alternative_types)
                while True:
                    alternative_type_= alternative_types[index]
                    index += 1
                    
                    repr_parts.append(alternative_type_.__name__)
                    
                    if index == limit:
                        break
                    
                    repr_parts.append(', ')
                    continue
                
                repr_parts.append(']')
        
        
        if self.uses_flags:
            default_flags = self.default_flags
            repr_parts.append(', default_flags=')
            repr_parts.append(int.__repr__(default_flags))
            
            all_flags = self.all_flags
            if default_flags != all_flags:
                repr_parts.append(', all_flags=')
                repr_parts.append(int.__repr__(all_flags))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two converter settings are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.all_flags != other.all_flags:
            return False
        
        if self.alternative_checked_types != other.alternative_checked_types:
            return False
        
        if self.alternative_type_name != other.alternative_type_name:
            return False
        
        if self.alternative_types != other.alternative_types:
            return False
        
        if self.converter != other.converter:
            return False
        
        if self.default_flags != other.default_flags:
            return False
        
        if self.default_type != other.default_type:
            return False
        
        if self.requires_part != other.requires_part:
            return False
        
        if self.uses_flags != other.uses_flags:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the converter setting's hash value."""
        hash_value = 0
        
        # all_flags
        hash_value ^= self.all_flags
        
        # alternative_checked_types
        alternative_checked_types = self.alternative_checked_types
        if (alternative_checked_types is not None):
            hash_value ^= len(alternative_checked_types) << 14
            for alternative_checked_type_name, alternative_checked_type_checker in alternative_checked_types.items():
                hash_value ^= hash(alternative_checked_type_name)
                
                try:
                    alternative_checked_type_checker_hash = hash(alternative_checked_type_checker)
                except TypeError:
                    alternative_checked_type_checker_hash = object.__hash__(alternative_checked_type_checker)
                hash_value ^= alternative_checked_type_checker_hash
        
        # alternative_type_name
        alternative_type_name = self.alternative_type_name
        if (alternative_type_name is not None):
            hash_value ^= hash(alternative_type_name)
        
        # alternative_types
        alternative_types = self.alternative_types
        if (alternative_types is not None):
            hash_value ^= len(alternative_types)
            for alternative_type in alternative_types:
                try:
                    alternative_type_hash = hash(alternative_type)
                except TypeError:
                    alternative_type_hash = object.__hash__(alternative_type)
                hash_value ^= alternative_type_hash
        
        # converter
        converter = self.converter
        try:
            converter_hash = hash(converter)
        except TypeError:
            converter_hash = object.__hash__(converter)
        hash_value ^= converter_hash
        
        # default_flags
        hash_value ^= self.default_flags
        
        # default_type
        default_type = self.default_type
        if (default_type is not None):
            try:
                default_type_hash = hash(default_type)
            except TypeError:
                default_type_hash = object.__hash__(default_type)
            hash_value ^= default_type_hash
        
        # requires_part
        hash_value ^= self.requires_part << 8
        
        # uses_flags
        hash_value ^= self.uses_flags << 9
        
        return hash_value
    

async def none_converter(command_context, content_parser_parameter_detail):
    return None


CONVERTER_NONE = ConverterSetting(
    converter = none_converter,
    uses_flags = False,
    default_flags = ConverterFlag(),
    all_flags = ConverterFlag(),
    alternative_type_name = None,
    default_type = None,
    alternative_types = None,
    requires_part = False
)


async def command_context_converter(command_context, content_parser_parameter_detail):
    return command_context

CONVERTER_SELF_CONTEXT = ConverterSetting(
    converter = command_context_converter,
    uses_flags = False,
    default_flags = ConverterFlag(),
    all_flags = ConverterFlag(),
    alternative_type_name = None,
    default_type = CommandContext,
    alternative_types = None,
    requires_part = False
)


async def self_client_converter(command_context, content_parser_parameter_detail):
    return command_context.client

CONVERTER_SELF_CLIENT = ConverterSetting(
    converter = self_client_converter,
    uses_flags = False,
    default_flags = ConverterFlag(),
    all_flags = ConverterFlag(),
    alternative_type_name = None,
    default_type = None,
    alternative_types = None,
    requires_part = False
)


async def self_message_converter(command_context, content_parser_parameter_detail):
    return command_context.message

CONVERTER_SELF_MESSAGE = ConverterSetting(
    converter = self_message_converter,
    uses_flags = False,
    default_flags = ConverterFlag(),
    all_flags = ConverterFlag(),
    alternative_type_name = None,
    default_type = None,
    alternative_types = None,
    requires_part = False
)



if CACHE_USER:
    async def user_converter(command_context, content_parser_parameter_detail, part):
        flags = content_parser_parameter_detail.flags
        message = command_context.message
        
        if flags & CONVERTER_FLAG_ID:
            parsed = ID_RP.fullmatch(part)
            if (parsed is not None):
                id_ = int(parsed.group(1))
                
                if flags & CONVERTER_FLAG_EVERYWHERE:
                    try:
                        user = USERS[id_]
                    except KeyError:
                        try:
                            user = await command_context.client.user_get(id_)
                        except BaseException as err:
                            if not (
                                isinstance(err, ConnectionError) or
                                (
                                    isinstance(err, DiscordException) and
                                    err.code in (
                                        ERROR_CODES.unknown_user,
                                        ERROR_CODES.unknown_member,
                                    )
                                )
                            ):
                                raise
                        
                        else:
                            return user
                    else:
                        return user
                
                else:
                    channel = message.channel
                    guild = message.guild
                    if guild is None:
                        if not channel.is_in_group_guild():
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
        
        if flags & CONVERTER_FLAG_MENTION:
            user = parse_user_mention(part, message)
            if (user is not None):
                return user
        
        if flags & CONVERTER_FLAG_NAME:
            channel = message.channel
            guild = channel.guild
            if (guild is None):
                if channel.is_in_group_guild():
                    user = None
                else:
                    user = channel.get_user_like(part)
            else:
                user = guild.get_user_like(part)
            
            if (user is not None):
                return user
        
        return None
else:
    async def user_converter(command_context, content_parser_parameter_detail, part):
        flags = content_parser_parameter_detail.flags
        message = command_context.message
        
        if flags & CONVERTER_FLAG_ID:
            parsed = ID_RP.fullmatch(part)
            if (parsed is not None):
                id_ = int(parsed.group(1))
                
                if flags & CONVERTER_FLAG_EVERYWHERE:
                    if flags & CONVERTER_FLAG_PROFILE:
                        guild = message.guild
                        if (guild is not None):
                            try:
                                user = await command_context.client.guild_user_get(guild, id_)
                            except BaseException as err:
                                if not (
                                    isinstance(err, ConnectionError) or
                                    (
                                        isinstance(err, DiscordException) and
                                        err.code in (
                                            ERROR_CODES.unknown_user,
                                            ERROR_CODES.unknown_member,
                                        )
                                    )
                                ):
                                    raise
                            else:
                                return user
                    
                    try:
                        user = await command_context.client.user_get(id_)
                    except BaseException as err:
                        if not (
                            isinstance(err, ConnectionError) or
                            (
                                isinstance(err, DiscordException) and
                                err.code in (
                                    ERROR_CODES.unknown_user,
                                    ERROR_CODES.unknown_member,
                                )
                            )
                        ):
                            raise
                    else:
                        return user
                
                else:
                    channel = message.channel
                    guild = message.guild
                    if guild is None:
                        if not channel.is_in_group_guild():
                            for user in channel.users:
                                if user.id == id_:
                                    return user
                    
                    else:
                        try:
                            user = await command_context.client.guild_user_get(guild, id_)
                        except BaseException as err:
                            if not(
                                isinstance(err, ConnectionError) or
                                (
                                    isinstance(err, DiscordException) and
                                    err.code in (
                                        ERROR_CODES.unknown_user,
                                        ERROR_CODES.unknown_member,
                                    )
                                )
                            ):
                                raise
                        else:
                            return user
        
        if flags & CONVERTER_FLAG_MENTION:
            user = parse_user_mention(part, message)
            if (user is not None):
                return user
        
        if flags & CONVERTER_FLAG_NAME:
            channel = message.channel
            guild = channel.guild
            if (guild is None):
                if not channel.is_in_group_guild():
                    user = channel.get_user_like(part)
                    if (user is not None):
                        return user
            
            else:
                try:
                    user = await command_context.client.guild_user_search(guild, part)
                except BaseException as err:
                    if not (
                        isinstance(err, ConnectionError) or
                        (
                            isinstance(err, DiscordException) and
                            err.code in (
                                ERROR_CODES.unknown_user,
                                ERROR_CODES.unknown_member,
                            )
                        )
                    ):
                        raise
                else:
                    return user
        
        return None

CONVERTER_USER = ConverterSetting(
    converter = user_converter,
    uses_flags = True,
    default_flags = ConverterFlag.user_default,
    all_flags = ConverterFlag.user_all,
    alternative_type_name = 'user',
    default_type = User,
    alternative_types = [
        UserBase,
    ],
    requires_part = True,
)

async def client_converter(command_context, content_parser_parameter_detail, part):
    flags = content_parser_parameter_detail.flags
    message = command_context.message
    
    if flags & CONVERTER_FLAG_ID:
        parsed = ID_RP.fullmatch(part)
        if (parsed is not None):
            id_ = int(parsed.group(1))
            
            try:
                client = CLIENTS[id_]
            except KeyError:
                pass
            else:
                if flags & CONVERTER_FLAG_EVERYWHERE:
                    return client
                
                else:
                    if client in message.channel.clients:
                        return client
    
    if flags & CONVERTER_FLAG_MENTION:
        client = parse_user_mention(part, message)
        if (client is not None) and isinstance(client, Client):
            return client
    
    if flags & CONVERTER_FLAG_NAME:
        if flags & CONVERTER_FLAG_EVERYWHERE:
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
    
CONVERTER_CLIENT = ConverterSetting(
    converter = client_converter,
    uses_flags = True,
    default_flags = ConverterFlag.client_default,
    all_flags = ConverterFlag.client_all,
    alternative_type_name = 'client',
    default_type = Client,
    alternative_types = None,
    requires_part = True,
)


async def _channel_converter_internal(command_context, content_parser_parameter_detail, part):
    flags = content_parser_parameter_detail.flags
    message = command_context.message
    
    if flags & CONVERTER_FLAG_ID:
        parsed = ID_RP.fullmatch(part)
        if (parsed is not None):
            id_ = int(parsed.group(1))
            
            if flags & CONVERTER_FLAG_EVERYWHERE:
                try:
                    channel = CHANNELS[id_]
                except KeyError:
                    pass
                else:
                    return channel
            
            else:
                channel = message.channel
                guild = message.guild
                if guild is None:
                    if channel.id == id_:
                        return channel
                
                else:
                    try:
                        channel = guild.channels[id_]
                    except KeyError:
                        pass
                    else:
                        return channel
    
    if flags & CONVERTER_FLAG_MENTION:
        channel = parse_channel_mention(part, message)
        if (channel is not None):
            return channel
    
    if flags & CONVERTER_FLAG_NAME:
        channel = message.channel
        guild = channel.guild
        if guild is None:
            if channel.has_name_like(part):
                return channel
        else:
            channel = guild.get_channel_like(part)
            if (channel is not None):
                return channel
    
    return None


async def channel_converter(command_context, content_parser_parameter_detail, part):
    channel = await _channel_converter_internal(command_context, content_parser_parameter_detail, part)
    if (channel is not None):
        type_checker = content_parser_parameter_detail.type_checker
        if type_checker is None:
            channel_type = content_parser_parameter_detail.type
            if (channel_type is not None):
                if not isinstance(channel, channel_type):
                    channel = None
        
        else:
            if not type_checker(channel):
                channel = None
    
    return channel


CONVERTER_CHANNEL = ConverterSetting(
    converter = channel_converter,
    uses_flags = True,
    default_flags = ConverterFlag.channel_default,
    all_flags = ConverterFlag.channel_all,
    alternative_type_name = 'channel',
    default_type = Channel,
    alternative_types = None,
    requires_part = True,
    alternative_checked_types = {
        'group_messageable': Channel.is_in_group_textual,
        'group_textual': Channel.is_in_group_textual,
        'group_guild_messageable': Channel.is_in_group_guild_textual,
        'group_guild_textual': Channel.is_in_group_guild_textual,
        'group_guild_main_text': Channel.is_in_group_guild_system,
        'group_guild_system': Channel.is_in_group_guild_system,
        'group_connectable': Channel.is_in_group_connectable,
        'group_guild_connectable': Channel.is_in_group_guild_connectable,
        'group_private': Channel.is_in_group_private,
        'group_guild': Channel.is_in_group_guild,
        'group_thread': Channel.is_in_group_thread,
        'group_can_contain_threads': Channel.is_in_group_threadable,
        'group_can_threadable': Channel.is_in_group_threadable,
        'group_can_create_invite_to': Channel.is_in_group_invitable,
        'group_can_create_invitable': Channel.is_in_group_invitable,
        'group_guild_movable': Channel.is_in_group_guild_sortable,
        'group_guild_sortable': Channel.is_in_group_guild_sortable,
        'guild_text': Channel.is_guild_text,
        'private': Channel.is_private,
        'guild_voice': Channel.is_guild_voice,
        'private_group': Channel.is_private_group,
        'guild_category': Channel.is_guild_category,
        'guild_announcements': Channel.is_guild_announcements,
        'guild_store': Channel.is_guild_store,
        'thread': Channel.is_thread,
        'guild_thread_announcements': Channel.is_guild_thread_announcements,
        'guild_thread_public': Channel.is_guild_thread_public,
        'guild_thread_private': Channel.is_guild_thread_private,
        'guild_stage': Channel.is_guild_stage,
        'guild_directory': Channel.is_guild_directory,
        'guild_forum': Channel.is_guild_forum,
    }
)

async def role_converter(command_context, content_parser_parameter_detail, part):
    flags = content_parser_parameter_detail.flags
    message = command_context.message
    
    if flags & CONVERTER_FLAG_ID:
        parsed = ID_RP.fullmatch(part)
        if (parsed is not None):
            id_ = int(parsed.group(1))
            
            if flags & CONVERTER_FLAG_EVERYWHERE:
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
    
    if flags & CONVERTER_FLAG_MENTION:
        role = parse_role_mention(part)
        if (role is not None):
            return role
    
    if flags & CONVERTER_FLAG_NAME:
        guild = message.guild
        if (guild is not None):
            role = guild.get_role_like(part)
            if (role is not None):
                return role
    
    return None

CONVERTER_ROLE = ConverterSetting(
    converter = role_converter,
    uses_flags = True,
    default_flags = ConverterFlag.role_default,
    all_flags = ConverterFlag.role_all,
    alternative_type_name = 'role',
    default_type = Role,
    alternative_types = None,
    requires_part = True,
)

async def emoji_converter(command_context, content_parser_parameter_detail, part):
    flags = content_parser_parameter_detail.flags
    if flags & CONVERTER_FLAG_MENTION:
        emoji = parse_emoji(part)
        if (emoji is not None):
            return emoji
    
    message = command_context.message
    if flags & CONVERTER_FLAG_ID:
        parsed = ID_RP.fullmatch(part)
        if (parsed is not None):
            id_ = int(parsed.group(1))
            
            if flags & CONVERTER_FLAG_EVERYWHERE:
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
    
    if flags & CONVERTER_FLAG_NAME:
        guild = message.guild
        if (guild is not None):
            emoji = guild.get_emoji_like(part)
            if (emoji is not None):
                return emoji
    
    return None

CONVERTER_EMOJI = ConverterSetting(
    converter = emoji_converter,
    uses_flags = True,
    default_flags = ConverterFlag.emoji_default,
    all_flags = ConverterFlag.emoji_all,
    alternative_type_name = 'emoji',
    default_type = Emoji,
    alternative_types = None,
    requires_part = True,
)


async def sticker_converter(command_context, content_parser_parameter_detail, part):
    flags = content_parser_parameter_detail.flags
    
    message = command_context.message
    if flags & CONVERTER_FLAG_ID:
        parsed = ID_RP.fullmatch(part)
        if (parsed is not None):
            id_ = int(parsed.group(1))
            
            if flags & CONVERTER_FLAG_EVERYWHERE:
                try:
                    sticker = await command_context.client.sticker_get(id_)
                except BaseException as err:
                    if not (
                        isinstance(err, ConnectionError) or
                        (
                            isinstance(err, DiscordException) and
                            err.code == ERROR_CODES.unknown_sticker
                        )
                    ):
                        raise
                else:
                    return sticker
            
            else:
                guild = message.guild
                if (guild is not None):
                    try:
                        sticker = await command_context.client.sticker_get(id_)
                    except BaseException as err:
                        if not (
                            isinstance(err, ConnectionError) or
                            (
                                isinstance(err, DiscordException) and
                                err.code == ERROR_CODES.unknown_sticker
                            )
                        ):
                            raise
                    else:
                        return sticker
    
    if flags & CONVERTER_FLAG_NAME:
        guild = message.guild
        if (guild is not None):
            sticker = guild.get_sticker_like(part)
            if (sticker is not None):
                return sticker
    
    return None

STICKER_EMOJI = ConverterSetting(
    converter = sticker_converter,
    uses_flags = True,
    default_flags = ConverterFlag.sticker_default,
    all_flags = ConverterFlag.sticker_all,
    alternative_type_name = 'sticker',
    default_type = Sticker,
    alternative_types = None,
    requires_part = True,
)


async def guild_converter(command_context, content_parser_parameter_detail, part):
    parsed = ID_RP.fullmatch(part)
    if (parsed is None):
        return None
    
    id_ = int(parsed.group(1))
    
    try:
        guild = GUILDS[id_]
    except KeyError:
        return None
    
    if content_parser_parameter_detail.flags & CONVERTER_FLAG_EVERYWHERE:
        return guild
    
    if guild in command_context.client.guild_profiles:
        return guild
    
    return None

CONVERTER_GUILD = ConverterSetting(
    converter = guild_converter,
    uses_flags = True,
    default_flags = ConverterFlag.guild_default,
    all_flags = ConverterFlag.guild_all,
    alternative_type_name = 'guild',
    default_type = Guild,
    alternative_types = None,
    requires_part = True
)

# Gets a message by it's id
async def _message_converter_m_id(command_context, content_parser_parameter_detail, message_id):
    message = MESSAGES.get(message_id, None)
    channel = command_context.message.channel
    if (message is not None):
        # Message found
        if content_parser_parameter_detail.flags & CONVERTER_FLAG_EVERYWHERE:
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
    client = command_context.client
    if channel.cached_permissions_for(client).can_read_message_history:
        try:
            message = await client.message_get((channel.id, message_id))
        except BaseException as err:
            if not (
                isinstance(err, ConnectionError) or
                (
                    isinstance(err, DiscordException) and
                    err.code in (
                        ERROR_CODES.unknown_channel, # message deleted
                        ERROR_CODES.unknown_message, # channel deleted
                        ERROR_CODES.missing_access, # client removed
                        ERROR_CODES.missing_permissions, # permissions changed meanwhile
                    )
                )
            ):
                raise
            
            # Message do not exists at the respective channel, or any other acceptable error
            return None
        else:
            return message
    else:
        # The message is given by id, but the client request it.
        return None

# Gets a message by it's and it's channel's id
async def _message_converter_cm_id(command_context, content_parser_parameter_detail, channel_id, message_id):
    channel = command_context.message.channel
    message = MESSAGES.get(message_id, None)
    if (message is not None):
        # Message found
        if content_parser_parameter_detail.flags & CONVERTER_FLAG_EVERYWHERE:
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

    if content_parser_parameter_detail.flags & CONVERTER_FLAG_EVERYWHERE:
        # Lets use that multi client core
        for client in message_channel.clients:
            if message_channel.cached_permissions_for(client).can_read_message_history:
                try:
                    message = await client.message_get((message_channel.id,  message_id))
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
        client = command_context.client
        if channel.cached_permissions_for(client).can_read_message_history:
            try:
                message = await client.message_get((message_channel.id, message_id))
            except BaseException as err:
                if not (
                    isinstance(err, ConnectionError) or
                    (
                        isinstance(err, DiscordException) and
                        err.code in (
                            ERROR_CODES.unknown_channel, # message deleted
                            ERROR_CODES.unknown_message, # channel deleted
                            ERROR_CODES.missing_access, # client removed
                            ERROR_CODES.missing_permissions, # permissions changed meanwhile
                        )
                    )
                ):
                    raise
            else:
                return message
        
        return None

async def message_converter(command_context, content_parser_parameter_detail, part):
    if content_parser_parameter_detail.flags & CONVERTER_FLAG_ID:
        parsed = ID_RP.fullmatch(part)
        if (parsed is not None):
            message_id = int(parsed.group(1))
            return await _message_converter_m_id(command_context, content_parser_parameter_detail, message_id)
        
        parsed = CHANNEL_MESSAGE_RP.fullmatch(part)
        if (parsed is not None):
            channel_id, message_id = parsed.groups()
            channel_id = int(channel_id)
            message_id = int(message_id)
            return await _message_converter_cm_id(command_context, content_parser_parameter_detail, channel_id,
                message_id)
    
    if content_parser_parameter_detail.flags & CONVERTER_FLAG_URL:
        parsed = MESSAGE_JUMP_URL_RP.fullmatch(part)
        if (parsed is not None):
            _, channel_id, message_id = parsed.groups()
            channel_id = int(channel_id)
            message_id = int(message_id)
            return await _message_converter_cm_id(command_context, content_parser_parameter_detail, channel_id,
                message_id)
    
    return None

CONVERTER_MESSAGE = ConverterSetting(
    converter = message_converter,
    uses_flags = True,
    default_flags = ConverterFlag.message_default,
    all_flags = ConverterFlag.message_all,
    alternative_type_name = 'message',
    default_type = Message,
    alternative_types = None,
    requires_part = True,
)

async def invite_converter(command_context, content_parser_parameter_detail, part):
    flags = content_parser_parameter_detail.flags
    
    # It would not be a Huyane code without some GOTO
    while True:
        if flags & CONVERTER_FLAG_URL:
            parsed = INVITE_URL_RP.fullmatch(part)
            if parsed is not None:
                break
        
        if flags & CONVERTER_FLAG_ID:
            parsed = INVITE_CODE_RP.fullmatch(part)
            if (parsed is not None):
                break
        
        return None
    
    code = parsed.group(1)
    
    try:
        invite = await command_context.client.invite_get(code)
    except BaseException as err:
        if not (
            isinstance(err, ConnectionError) or
            (
                isinstance(err, DiscordException) and
                err.code == ERROR_CODES.unknown_invite # Invite not exists
            )
        ):
            raise
        
        return None
    
    return invite

CONVERTER_INVITE = ConverterSetting(
    converter = invite_converter,
    uses_flags = True,
    default_flags = ConverterFlag.invite_default,
    all_flags = ConverterFlag.invite_all,
    alternative_type_name = 'invite',
    default_type = Invite,
    alternative_types = None,
    requires_part = True,
)


async def color_converter(command_context, content_parser_parameter_detail, part):
    return parse_color(part)

CONVERTER_COLOR = ConverterSetting(
    converter = color_converter,
    uses_flags = False,
    default_flags = ConverterFlag(),
    all_flags = ConverterFlag(),
    alternative_type_name = 'color',
    default_type = Color,
    alternative_types = None,
    requires_part = True,
)


async def str_converter(command_context, content_parser_parameter_detail, part):
    return part

CONVERTER_STR = ConverterSetting(
    converter = str_converter,
    uses_flags = False,
    default_flags = ConverterFlag(),
    all_flags = ConverterFlag(),
    alternative_type_name = None,
    default_type = str,
    alternative_types = None,
    requires_part = True,
)


async def int_converter(command_context, content_parser_parameter_detail, part):
    if len(part) > NUMERIC_CONVERSION_LIMIT:
        return None
    
    try:
        int_ = int(part)
    except ValueError:
        int_ = None
    
    return int_

CONVERTER_INT = ConverterSetting(
    converter = int_converter,
    uses_flags = False,
    default_flags = ConverterFlag(),
    all_flags = ConverterFlag(),
    alternative_type_name = None,
    default_type = int,
    alternative_types = None,
    requires_part = True,
)

async def tdelta_converter(command_context, content_parser_parameter_detail, part):
    return parse_tdelta(part)

CONVERTER_TDELTA = ConverterSetting(
    converter = tdelta_converter,
    uses_flags = False,
    default_flags = ConverterFlag(),
    all_flags = ConverterFlag(),
    alternative_type_name = 'tdelta',
    default_type = timedelta,
    alternative_types = None,
    requires_part = True,
)

if (relativedelta is not None):
    async def rdelta_converter(command_context, content_parser_parameter_detail, part):
        return parse_rdelta(part)

    CONVERTER_RDELTA = ConverterSetting(
        converter = rdelta_converter,
        uses_flags = False,
        default_flags = ConverterFlag(),
        all_flags = ConverterFlag(),
        alternative_type_name = 'rdelta',
        default_type = relativedelta,
        alternative_types = None,
        requires_part = True,
    )

else:
    rdelta_converter = None
    CONVERTER_RDELTA = None


class ContentParserParameterDetail(RichAttributeErrorBaseType):
    """
    Stores details about a converter.
    
    Attributes
    ----------
    converter_setting : ``ConverterSetting``
        The converter setting used by the parameter.
    flags : ``ConverterFlag``
        Converter flags to customize the events.
    type : `None`, `type`
        The type or subtype of the annotation to parse.
    type_checker : `None`, `callable`
        Additional type checker.
    """
    __slots__ = ('converter_setting', 'flags', 'type', 'type_checker')
    
    def __new__(cls, converter_setting, type_, type_checker):
        """
        Creates a new ``ContentParserParameterDetail`` with the given parameters.
        
        Parameters
        ----------
        converter_setting : ``ConverterSetting``
            The converter setting used by the parameter.
        type_ : `None`, `type`
            The type or subtype of the annotation to parse.
    type_checker : `None`, `callable`
        Additional type checker.
        """
        self = object.__new__(cls)
        self.converter_setting = converter_setting
        self.flags = converter_setting.default_flags
        self.type = type_
        self.type_checker = type_checker
        return self
    
    
    def __repr__(self):
        """Returns the ``ContentParserParameterDetail``'s representation."""
        repr_parts = ['<', self.__class__.__name__, ' converter_setting=']
        converter_setting = self.converter_setting
        repr_parts.append(repr(converter_setting))
        
        type_ = self.type
        if (type_ is not converter_setting.default_type):
            repr_parts.append(', type=')
            repr_parts.append(repr(type_))
        
        type_checker = self.type_checker
        if (type_checker is not None):
            repr_parts.append(', type_checker=')
            repr_parts.append(repr(type_checker))
            
        flags = self.flags
        if (flags != converter_setting.default_flags):
            repr_parts.append(', flags=')
            repr_parts.append(repr(flags))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two content parser parameter details are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.converter_setting != other.converter_setting:
            return False
        
        if self.flags != other.flags:
            return False
        
        if self.type != other.type:
            return False
        
        if self.type_checker != other.type_checker:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the converter parser parameter detail's hash value."""
        hash_value = hash(self.converter_setting) ^ self.flags
        
        type_ = self.type
        if (type_ is not None):
            try:
                type_hash = hash(type_)
            except TypeError:
                type_hash = object.__hash__(type_)
            hash_value ^= type_hash
        
        type_checker = self.type_checker
        if (type_checker is not None):
            try:
                type_checker_hash = hash(type_checker)
            except TypeError:
                type_checker_hash = object.__hash__(type_checker)
            hash_value ^= type_checker_hash
            
        return hash_value


class ContentParserParameter(RichAttributeErrorBaseType):
    """
    Represents a parameter to parse.
    
    Parameters
    ----------
    default : `None`, `Any`
        The default object to return if the parser fails.
    description : `None`, `str`
        The description of the parameter if any.
    detail : `None`, ``ContentParserParameterDetail``
        Converting details for single-type annotation.
    details : `None`, `list` of ``ContentParserParameterDetail``
        Converting details for multi-type annotations.
    display_name : `str`
        The parameter's display name.
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
    is_rest : `bool`
        Whether the parameter is rest parser.
    name : `str`
        The parameter's name.
    """
    __slots__ = (
        'default', 'description', 'detail', 'details', 'display_name', 'flags', 'has_default', 'index',
        'is_args', 'is_keyword', 'is_kwargs', 'is_positional', 'is_rest', 'name'
    )
    
    def __new__(cls, parameter, index):
        """
        Creates a new ``ContentParserParameter`` with the given parameters.
        
        Parameters
        ----------
        parameter : ``Parameter``
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
        RuntimeError
            - Multi-type annotation without requiring parsing is forbidden.
        """
        display_name = parameter.name
        
        details = []
        
        while True:
            if not parameter.has_annotation:
                description = None
                break
            
            annotation = parameter.annotation
            if annotation is None:
                description = None
                break
            
            detail = get_detail_for_value(annotation)
            if (detail is not None):
                details.append(detail)
                description = None
                break
            
            if isinstance(annotation, set):
                details.extend(get_details_from_set(annotation))
                description = None
                break
            
            if isinstance(annotation, tuple):
                if type(annotation) is not tuple:
                    annotation = tuple(annotation)
                
                annotation_length = len(annotation)
                if annotation_length not in (2, 3):
                    raise ValueError(
                        f'`tuple` annotation\'s length can be either `2`, `3`, got '
                        f'{annotation_length!r}: {annotation!r}'
                    )
                
                annotation_tuple_type = annotation[0]
                if (annotation_tuple_type is not None):
                    detail = get_detail_for_value(annotation_tuple_type)
                    if (detail is not None):
                        details.append(detail)
                    else:
                        if isinstance(annotation_tuple_type, set):
                            details.extend(get_details_from_set(annotation_tuple_type))
                        else:
                            raise TypeError(
                                f'`annotation` was given as `tuple`, but it\'s 0th element was not given '
                                f'as any of the expected values: `None`, `type`, `str`, `set`, got '
                                f'{annotation_tuple_type.__class__.__name__}; {annotation_tuple_type!r}.'
                            )
                
                
                annotation_tuple_description = annotation[1]
                if type(annotation_tuple_description) is str:
                    description = annotation_tuple_description
                elif isinstance(annotation_tuple_description, str):
                    description = str(annotation_tuple_description)
                else:
                    raise TypeError(
                        f'`annotation` description can be `str`, got '
                        f'{annotation_tuple_description.__class__.__name__}; {annotation_tuple_description!r}.'
                    )
                
                
                if annotation_length == 3:
                    annotation_tuple_name = annotation[2]
                    if type(annotation_tuple_name) is str:
                        display_name = annotation_tuple_name
                    elif isinstance(annotation_tuple_name, str):
                        display_name = str(annotation_tuple_name)
                    else:
                        raise TypeError(
                            f'`annotation` name can be `str`, got '
                            f'{annotation_tuple_name.__class__.__name__}; {annotation_tuple_name!r}.'
                        )
                
                break
            
            raise TypeError(
                f'`annotation` can be `None`, `type`, `str`, `tuple`, `set`, got '
                f'{annotation.__class__.__name__}; {annotation!r}.'
            )
        
        
        details_length = len(details)
        if details_length == 0:
            detail = ContentParserParameterDetail(CONVERTER_NONE, CONVERTER_NONE.default_type, None)
            details = None
        elif details_length == 1:
            detail = details[0]
            details = None
        else:
            for detail in details:
                if not detail.converter_setting.requires_part:
                    raise RuntimeError(
                        'Multi-type annotation without requiring parsing is forbidden.'
                    )
            
            detail = None
        
        display_name = raw_name_to_display(display_name)
        
        has_default = parameter.has_default
        if has_default:
            default = parameter.default
        else:
            default = None
        
        is_positional = parameter.is_positional()
        is_keyword = parameter.is_keyword_only()
        is_args = parameter.is_args()
        is_kwargs = parameter.is_kwargs()
        
        name = parameter.name
        
        self = object.__new__(cls)
        self.detail = detail
        self.details = details
        self.default = default
        self.description = description
        self.display_name = display_name
        self.has_default = has_default
        self.index = index
        self.is_args = is_args
        self.is_rest = False
        self.is_keyword = is_keyword
        self.is_kwargs = is_kwargs
        self.is_positional = is_positional
        self.name = name
        return self
    
    def __repr__(self):
        """Returns the content parser parameter's representation."""
        repr_parts = ['<', self.__class__.__name__,
            ' name = ', repr(self.name),
         ]
        
        if self.has_default:
            repr_parts.append(', default = ')
            repr_parts.append(repr(self.default))
        
        detail = self.detail
        if (detail is None):
            repr_parts.append(', details = ')
            repr_parts.append(repr(self.details))
        else:
            if (detail.converter_setting is CONVERTER_NONE):
                if self.is_rest:
                    repr_parts.append(', is_rest = True')
            else:
                repr_parts.append(', details = [')
                repr_parts.append(repr(detail))
                repr_parts.append(']')
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two content parsers parameters are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.default != other.default:
            return False
        
        if self.description != other.description:
            return False
        
        if self.detail != other.detail:
            return False
        
        if self.details != other.details:
            return False
        
        if self.display_name != other.display_name:
            return False
        
        if self.has_default != other.has_default:
            return False
        
        if self.index != other.index:
            return False
        
        if self.is_args != other.is_args:
            return False
        
        if self.is_keyword != other.is_keyword:
            return False
        
        if self.is_kwargs != other.is_kwargs:
            return False
        
        if self.is_positional != other.is_positional:
            return False
        
        if self.is_rest != other.is_rest:
            return False
        
        if self.name != other.name:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the hash value of the content parser parameter."""
        hash_value = 0
        
        # default
        default = self.default
        try:
            default_hash = hash(default)
        except TypeError:
            default_hash = object.__hash__(default)
        
        hash_value ^= default_hash
        
        # description
        description = self.description
        if (description is not None):
            hash_value ^= hash(description)
        
        # detail
        detail = self.detail
        if (detail is not None):
            hash_value ^= hash(detail)
        
        # details
        details = self.details
        if (details is not None):
            hash_value ^= len(details)
            for detail in details:
                hash_value ^= hash(detail)
        
        # display_name
        display_name = self.display_name
        hash_value ^= hash(display_name)
        
        # has_default
        hash_value ^= self.has_default << 8
        
        # index
        hash_value ^= self.index << 9
        
        # is_args
        hash_value ^= self.is_args << 18
        
        # is_keyword
        hash_value ^= self.is_keyword << 19
        
        # is_kwargs
        hash_value ^= self.is_kwargs << 20
        
        # is_positional
        hash_value ^= self.is_positional << 21
        
        # is_rest
        hash_value ^= self.is_rest << 22
        
        # name
        name = self.name
        if (display_name != name):
            hash_value ^= hash(name)
        
        return hash_value
    
    
    def set_converter_setting(self, converter_setting):
        """
        Sets a new converter setting to the ``ContentParserParameter``.
        
        Parameters
        ----------
        converter_setting : ``ConverterSetting``
        
        Raises
        ------
        RuntimeError
            Converter setting cannot be set if the parser is multi type events.
        """
        if self.detail is None:
            raise RuntimeError('Converter setting cannot be set if the parser is multi type.')
        
        self.detail = ContentParserParameterDetail(converter_setting, converter_setting.default_type, None)
    
    
    async def parse(self, command_context, part):
        """
        Tries to parse the parameter from the given part.
        
        This method is a coroutine.
        
        Parameters
        ----------
        command_context : ``CommandContext``
            The respective command's context.
        part : `None`, `str`
            The received content's part to check.
        
        Returns
        -------
        parsed : `None`, `Any`
            The parsed object if any.
        """
        detail = self.detail
        if (detail is None):
            for detail in self.details:
                parsed = await detail.converter_setting.converter(command_context, detail, part)
                if (parsed is not None):
                    break
            else:
                parsed = None
        else:
            converter_setting = detail.converter_setting
            converter = converter_setting.converter
            if converter_setting.requires_part:
                parsed = await converter(command_context, detail, part)
            else:
                parsed = await converter(command_context, detail)
        
        return parsed
    
    
    def _iter_details(self):
        """
        Iterates over the details of the converter.
        
        This method is a generator.
        
        Yields
        ------
        detail : ``ContentParserParameterDetail``
        """
        detail = self.detail
        if (detail is None):
            yield from self.details
        else:
            yield self.detail


COMMAND_CONTENT_PARSER_POST_PROCESSORS = []


def get_detail_for_str(annotation):
    """
    Creates a ``ContentParserParameterDetail`` for the given string annotation value.
    
    Parameters
    ----------
    annotation : `str`
        The respective annotation.

    Returns
    -------
    detail : ``ContentParserParameterDetail``
    
    Raises
    ------
    ValueError
        There is no converter setting for the annotation.
    """
    try:
        converter_setting = CONVERTER_SETTING_NAME_TO_SETTING[annotation]
    except KeyError:
        raise ValueError(
            f'There is no converter registered for {annotation!r}.'
        ) from None
    
    annotation_type = CONVERTER_NAME_TO_TYPE.get(annotation, None)
    
    alternative_checked_types = converter_setting.alternative_checked_types
    if alternative_checked_types is None:
        type_checker = None
    else:
        type_checker = alternative_checked_types.get(annotation, None)
    
    return ContentParserParameterDetail(converter_setting, annotation_type, type_checker)


def get_detail_for_type(annotation):
    """
    Creates a ``ContentParserParameterDetail`` for the given type annotation value.
    
    Parameters
    ----------
    annotation : `str`
        The respective annotation.
    
    Returns
    -------
    detail : ``ContentParserParameterDetail``
    
    Raises
    ------
    ValueError
        There is no converter setting for the annotation.
    """
    try:
        converter_setting = CONVERTER_SETTING_TYPE_TO_SETTING[annotation]
    except KeyError:
        raise ValueError(
            f'There is no converter registered for {annotation!r}.'
        ) from None
    
    return ContentParserParameterDetail(converter_setting, annotation, None)



def get_detail_for_value(annotation):
    """
    Creates a ``ContentParserParameterDetail`` for the given value.
    
    Parameters
    ----------
    annotation : `str`, `type`
        The respective annotation.
    
    Returns
    -------
    detail : ``ContentParserParameterDetail``
    
    Raises
    ------
    ValueError
        The is no converter setting for the annotation.
    """
    if isinstance(annotation, type):
        detail = get_detail_for_type(annotation)
    
    elif type(annotation) is str:
        detail = get_detail_for_str(annotation)
    
    elif isinstance(annotation, str):
        annotation = str(annotation)
        detail = get_detail_for_str(annotation)
    
    else:
        detail = None
    
    return detail

def get_details_from_set(annotation):
    """
    Generates ``ContentParserParameterDetail`` from the given annotation value.
    
    This function is a generator.
    
    Parameters
    ----------
    annotation : `set` of (`str`, `type`)
        The respective annotation.
    
    Yields
    -------
    detail : ``ContentParserParameterDetail``
    
    Raises
    ------
    ValueError
        The is no converter setting for the annotation.
    TypeError
        If a sub-annotation's type is incorrect.
    """
    for sub_annotation in annotation:
        if sub_annotation is None:
            continue
        
        detail = get_detail_for_value(sub_annotation)
        if (detail is None):
            raise TypeError(
                f'`annotation` set can contain only `str` and `type` elements, got '
                f'{sub_annotation.__class__.__name__}; {sub_annotation!r}; annotation={annotation!r}.'
            )
        
        yield detail
        continue


class CommandContentParser(RichAttributeErrorBaseType):
    """
    Content parser for commands.
    
    Attributes
    ----------
    _parameters : `list` of ``ContentParserParameter``
        The parameters of the respective function.
    _content_parameter_parser : ``ContentParameterParser``
        The parameter separator of the parser.
    """
    __slots__ = ('_content_parameter_parser', '_parameters',)
    
    def __new__(cls, func, separator, assigner):
        """
        Creates a new ``CommandContentParser`` returning the parser for the function and the function itself
        as well.
        
        Parameters
        ----------
        func : `async-callable`
            The callable function.
        separator : `None`, ``ContentParameterSeparator``, `str`, `tuple` (`str`, `str`)
            The parameter separator of the parser.
        
        Returns
        -------
        self : ``CommandContentParser``
            The created parser.
        func : `async-callable`
            The function to which the parser is created for.
        
        Raises
        ------
        TypeError
            - If `separator` is not given as `None`, `str`, neither as `tuple`.
            - If `separator` was given as `tuple`, but it's element are not `str`-s.
            - If `assigner` was not given neither as `None`, `str`.
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
                raise TypeError(
                    f'`func` is not `async-callable` and cannot be instanced to `async` either, got {func!r}.'
                )
            
            should_instance = True
        
        else:
            raise TypeError(
                f'`func` is not `async-callable` and cannot be instanced to `async` either, got {func!r}.'
            )
        
        parameters = []
        
        index = 0
        for parameter in real_analyzer.parameters:
            if not parameter.reserved:
                content_parser_parameter = ContentParserParameter(parameter, index)
                parameters.append(content_parser_parameter)
                index += 1
        
        if should_instance:
            func = analyzer.insatnce()
        
        self = object.__new__(cls)
        self._parameters = parameters
        self._content_parameter_parser = content_parameter_parser
        
        for postprocessor in CONTENT_PARSER_PARAMETER_POSTPROCESSORS:
            postprocessor(self)
        
        return self, func
    
    
    def __repr__(self):
        """Returns the command content parser's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' content_parameter_parser=')
        repr_parts.append(repr(self._content_parameter_parser))
        
        repr_parts.append(', parameters=')
        repr_parts.append(repr(self._parameters))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two command content parsers are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self._content_parameter_parser != other._content_parameter_parser:
            return False
        
        if self._parameters != other._parameters:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the command content parser's hash value."""
        hash_value = 0
        
        hash_value ^= hash(self._content_parameter_parser)
        
        parameters = self._parameters
        hash_value ^= len(parameters)
        
        for parameter in parameters:
            hash_value ^= parameter
        
        return hash_value
    
    
    async def parse_content(self, command_context, index):
        """
        Parses the message's content to fulfill a command's parameters.
        
        This method is a coroutine.
        
        Parameters
        ----------
        command_context : ``CommandContext``
            A command context of the command.
        index : `int`
            The index of the content's character since the command's parameters should be parsed from.
        
        Returns
        -------
        parameter_parsing_states : `list` of ``ParameterParsingStateBase``
        """
        content_parameter_parser = self._content_parameter_parser
        parameter_parsing_states = create_parameter_parsing_states(self)
        
        for parameter_parsing_state in iter_no_part_parameter_states(parameter_parsing_states):
            parsed_value = await parameter_parsing_state.content_parser_parameter.parse(command_context, None)
            parameter_parsing_state.add_parsed_value(parsed_value, None)
        
        content = command_context.content
        length = len(content)
        while True:
            if index >= length:
                break
            
            if get_is_all_parameter_parser_state_satisfied(parameter_parsing_states):
                parameter_parsing_state = get_rest_parameter_state(parameter_parsing_states)
                if (parameter_parsing_state is not None):
                    rest = parse_rest_content(content, index)
                    parameter_parsing_state.add_parsed_value(rest, None)
                
                break
            
            keyword, part, index = content_parameter_parser(content, index)
            if keyword is None:
                parameter_parsing_state = get_next_non_filled_parameter_state(parameter_parsing_states)
                if parameter_parsing_state is None:
                    continue
                
                parsed_value = await parameter_parsing_state.content_parser_parameter.parse(command_context, part)
                parameter_parsing_state.add_parsed_value(parsed_value, None)
            else:
                keyword = raw_name_to_display(keyword)
                parameter_parsing_state = get_keyword_parameter_state(parameter_parsing_states, keyword)
                if parameter_parsing_state is None:
                    continue
                
                parsed_value = await parameter_parsing_state.content_parser_parameter.parse(command_context, part)
                parameter_parsing_state.add_parsed_value(parsed_value, keyword)
        
        return parameter_parsing_states


def get_next_non_filled_parameter_state(parameter_parsing_states):
    """
    Gets the next non-filled parameter parsing state.
    
    Parameters
    ----------
    parameter_parsing_states : `list` of ``ParameterParsingState``
        Parameters parsing states to choose from.
    
    Returns
    -------
    parameter_parsing_state : ``ParameterParsingState``, `None`
    """
    for parameter_parsing_state in parameter_parsing_states:
        content_parser_parameter = parameter_parsing_state.content_parser_parameter
        if content_parser_parameter.is_keyword or content_parser_parameter.is_kwargs:
            return None
        
        if content_parser_parameter.is_args:
            return parameter_parsing_state
        
        if not parameter_parsing_state.is_satisfied():
            return parameter_parsing_state
        
        continue
    
    return None


def iter_no_part_parameter_states(parameter_parsing_states):
    """
    Iterates over the parameter parsing states, and yields which do not require
    
    Parameters
    ----------
    parameter_parsing_states : `list` of ``ParameterParsingState``
        Parameters parsing states to choose from.

    Yields
    ------
    parameter_parsing_state : ``ParameterParsingState``
    """
    for parameter_parsing_state in parameter_parsing_states:
        content_parser_parameter = parameter_parsing_state.content_parser_parameter
        if content_parser_parameter.is_rest:
            continue
        
        detail = content_parser_parameter.detail
        if detail is None:
            continue
        
        if detail.converter_setting.requires_part:
            continue
        
        yield parameter_parsing_state


def get_keyword_parameter_state(parameter_parsing_states, keyword):
    """
    Tries to get the parameter state for the given name.
    
    Parameters
    ----------
    parameter_parsing_states : `list` of ``ParameterParsingState``
        Parameters parsing states to choose from.
    keyword : `str`
        The keyword to get the parameter for.
    
    Returns
    -------
    parameter_parsing_state : ``ParameterParsingState``, `None`
    """
    for parameter_parsing_state in parameter_parsing_states:
        content_parser_parameter = parameter_parsing_state.content_parser_parameter
        if content_parser_parameter.is_kwargs:
            return parameter_parsing_state
        
        if content_parser_parameter.display_name == keyword:
            return parameter_parsing_state
    
    return None


def get_rest_parameter_state(parameter_parsing_states):
    """
    Gets the rest parameter from the given content if there is any.
    
    Parameters
    ----------
    parameter_parsing_states `list` of ``ParameterParsingStateBase``
        The created parameter parser state instances.

    Returns
    -------
    parameter_parsing_state : ``ParameterParsingState``, `None`
    """
    for parameter_parsing_state in parameter_parsing_states:
        if parameter_parsing_state.content_parser_parameter.is_rest:
            return parameter_parsing_state


def create_parameter_parsing_states(command_content_parser):
    """
    Creates parser states for the given content parser parameters.
    
    Parameters
    ----------
    command_content_parser : ``CommandContentParser``
        The parameters of a ``CommandContentParser``.
    
    Returns
    -------
    parameter_parsing_states : `list` of ``ParameterParsingStateBase``
        The created parameter parser state instances.
    """
    parameter_parsing_states = []
    for content_parser_parameters in command_content_parser._parameters:
        if content_parser_parameters.is_kwargs:
            parameter_parser_state_type = KwargsParameterParsingState
        elif content_parser_parameters.is_rest:
            parameter_parser_state_type = RestParameterParsingState
        else:
            parameter_parser_state_type = GenericParameterParsingState
        
        parameter_parser_state = parameter_parser_state_type(content_parser_parameters)
        parameter_parsing_states.append(parameter_parser_state)
    
    return parameter_parsing_states


def get_is_all_parameter_parser_state_satisfied(parameter_parsing_states):
    """
    Returns whether all the parser states are satisfied.
    
    Parameters
    ----------
    parameter_parsing_states : `list` of ``ParameterParsingStateBase``
        The used parameter parsing states.
    
    Returns
    -------
    is_all_parameter_parser_state_satisfied : `bool`
    """
    for parameter_parser_state in parameter_parsing_states:
        if not parameter_parser_state.is_satisfied():
            return False
    
    return True


class ParameterParsingStateBase:
    """
    Base class for parsing states used meanwhile parsing parameters of a command.
    
    Attributes
    ----------
    content_parser_parameter : ``ContentParserParameter``
        The respective parameter.
    """
    __slots__ = ('content_parser_parameter', )
    
    def __new__(cls, content_parser_parameter):
        """
        Creates a new ``ParameterParsingState`` from the given ``content_parser_parameter``.
        
        Parameters
        ----------
        content_parser_parameter : ``ContentParserParameter``
            The respective parameter.
        """
        self = object.__new__(cls)
        self.content_parser_parameter = content_parser_parameter
        return self
    
    
    def add_parsed_value(self, parsed_value, keyword):
        """
        Adds a value to the ``ParameterParsingState``.
        
        Parameters
        ----------
        parsed_value : `Any`
            The parsed value.
        keyword : `None`, `str`
            The keyword used to reference the value.
        """
        pass
    
    
    def get_parser_value(self, args, kwargs):
        """
        Gets the parser's value.
        
        Parameters
        ----------
        args : `list`
            Parameters to pass to a command's function.
        kwargs : `dict`
            Keyword parameter to pass to a command's function.

        Raises
        ------
        CommandParameterParsingError
            Parsing was unsuccessful.
        """
        pass

    
    def is_satisfied(self):
        """
        Returns whether the respective parameter is satisfied.
        
        Returns
        -------
        is_satisfied : `bool`
        """
        return True
    
    
    def __repr__(self):
        """Returns the parsing state's representation."""
        repr_parts = [
            '<',
            self.__class__.__name__,
            ' content_parser_parameter=',
            repr(self.content_parser_parameter),
            '>',
        ]
        
        return ''.join(repr_parts)


class GenericParameterParsingState(ParameterParsingStateBase):
    """
    Generic parsing state used meanwhile parsing parameters of a command.
    
    Attributes
    ----------
    content_parser_parameter : ``ContentParserParameter``
        The respective parameter.
    satisfied : `bool`
        Whether the parser is satisfied.
    parsed_values : `None`, `list` of `Any`
        The parsed values for the respective ``ContentParserParameter``.
    """
    __slots__ = ('satisfied', 'parsed_values', )
    
    @copy_docs(ParameterParsingStateBase.__new__)
    def __new__(cls, content_parser_parameter):
        self = object.__new__(cls)
        self.content_parser_parameter = content_parser_parameter
        self.parsed_values = None
        self.satisfied = False
        return self
    
    
    @copy_docs(ParameterParsingStateBase.add_parsed_value)
    def add_parsed_value(self, parsed_value, keyword):
        parsed_values = self.parsed_values
        if parsed_values is None:
            self.parsed_values = parsed_values = []
        
        parsed_values.append(parsed_value)
        
        if (parsed_value is not None):
            content_parser_parameter = self.content_parser_parameter
            if content_parser_parameter.is_positional or content_parser_parameter.is_keyword:
                self.satisfied = True
    
    
    @copy_docs(ParameterParsingStateBase.get_parser_value)
    def get_parser_value(self, args, kwargs):
        content_parser_parameter = self.content_parser_parameter
        if content_parser_parameter.is_positional:
            parsed_value = get_first_non_none_parsed_value(self.parsed_values)
            if parsed_value is None:
                if (not content_parser_parameter.has_default):
                    raise CommandParameterParsingError(content_parser_parameter)
                
                parsed_value = content_parser_parameter.default
                
            args.append(parsed_value)
            return
        
        if content_parser_parameter.is_keyword:
            parsed_value = get_first_non_none_parsed_value(self.parsed_values)
            if parsed_value is None:
                if (not content_parser_parameter.has_default):
                    raise CommandParameterParsingError(content_parser_parameter)
                
                parsed_value = content_parser_parameter.default
            
            kwargs[content_parser_parameter.name] = parsed_value
            return
        
        if content_parser_parameter.is_args:
            parsed_values = get_all_non_none_parsed_value(self.parsed_values)
            args.extend(parsed_values)
    
    
    @copy_docs(ParameterParsingStateBase.is_satisfied)
    def is_satisfied(self):
        return self.satisfied
    
    
    @copy_docs(ParameterParsingStateBase.__repr__)
    def __repr__(self):
        repr_parts = [
            '<',
            self.__class__.__name__,
            ' content_parser_parameter=',
            repr(self.content_parser_parameter),
            ', parsed_values=',
            repr(self.parsed_values),
            '>',
        ]
        
        return ''.join(repr_parts)


class KwargsParameterParsingState(ParameterParsingStateBase):
    """
    `**kwargs`` specific parsing state used meanwhile parsing parameters of a command.
    
    Attributes
    ----------
    content_parser_parameter : ``ContentParserParameter``
        The respective parameter.
    parsed_items : `None`, `list` of `tuple` (`str`, `Any`)
        The parsed values for the respective ``ContentParserParameter``.
    """
    __slots__ = ('parsed_items', )
    
    @copy_docs(ParameterParsingStateBase.__new__)
    def __new__(cls, content_parser_parameter):
        self = object.__new__(cls)
        self.content_parser_parameter = content_parser_parameter
        self.parsed_items = None
        return self
    
    
    @copy_docs(ParameterParsingStateBase.add_parsed_value)
    def add_parsed_value(self, parsed_value, keyword):
        parsed_items = self.parsed_items
        if parsed_items is None:
            self.parsed_items = parsed_items = []
        
        parsed_items.append((keyword, parsed_value))
    
    
    @copy_docs(ParameterParsingStateBase.get_parser_value)
    def get_parser_value(self, args, kwargs):
        parsed_items = self.parsed_items
        if (parsed_items is not None):
            for key, value in parsed_items:
                if (value is not None):
                    kwargs.setdefault(key, value)
    
    
    @copy_docs(ParameterParsingStateBase.is_satisfied)
    def is_satisfied(self):
        return False
    
    
    @copy_docs(ParameterParsingStateBase.__repr__)
    def __repr__(self):
        repr_parts = [
            '<',
            self.__class__.__name__,
            ' content_parser_parameter=',
            repr(self.content_parser_parameter),
            ', parsed_items=',
            repr(self.parsed_items),
            '>',
        ]
        
        return ''.join(repr_parts)


class RestParameterParsingState(ParameterParsingStateBase):
    """
    Parameter parsing state which consumes all the unused content. Used parsing state used meanwhile parsing
    parameters of a command.
    
    Attributes
    ----------
    content_parser_parameter : ``ContentParserParameter``
        The respective parameter.
    value : `None`, `str`
        The set rest value.
    """
    __slots__ = ('value', )
    
    @copy_docs(ParameterParsingStateBase.__new__)
    def __new__(cls, content_parser_parameter):
        self = object.__new__(cls)
        self.content_parser_parameter = content_parser_parameter
        self.value = None
        return self
    
    
    @copy_docs(ParameterParsingStateBase.add_parsed_value)
    def add_parsed_value(self, parsed_value, keyword):
        if parsed_value:
            self.value = parsed_value
    
    
    @copy_docs(ParameterParsingStateBase.get_parser_value)
    def get_parser_value(self, args, kwargs):
        parsed_value = self.value
        if parsed_value is None:
            content_parser_parameter = self.content_parser_parameter
            if content_parser_parameter.has_default:
                parsed_value = content_parser_parameter.default
            else:
                parsed_value = ''
        
        args.append(parsed_value)
    
    
    @copy_docs(ParameterParsingStateBase.__repr__)
    def __repr__(self):
        repr_parts = [
            '<',
            self.__class__.__name__,
            ' content_parser_parameter=',
            repr(self.content_parser_parameter),
            ', value=',
            repr(self.value),
            '>',
        ]
        
        return ''.join(repr_parts)

def get_first_non_none_parsed_value(parsed_values):
    """
    Gets the first non-`None` parsed value.
    
    Parameters
    ----------
    parsed_values : `None`, `list` of `Any`
        The parsed value.

    Returns
    -------
    value : `None`, `Any`
        The parsed value if any.
    """
    if (parsed_values is not None):
        for parsed_value in parsed_values:
            if (parsed_value is not None):
                return parsed_value
    
    return None


def get_all_non_none_parsed_value(parsed_values):
    """
    Gets all the non-`None` parsed values.
    
    Parameters
    ----------
    parsed_values : `None`, `list` of `Any`
        The parsed value.

    Returns
    -------
    values : `None`, `Any`
        The parsed value if any.
    """
    values = []
    if (parsed_values is not None):
        for parsed_value in parsed_values:
            if (parsed_value is not None):
                values.append(parsed_value)
    
    return values


def content_parser_parameter_postprocessor_try_find_context(command_context_parser):
    """
    Tries to find context variable inside of a command context parser's parameters.
    
    Parameters
    ----------
    command_context_parser : ``CommandContentParser``
        The respective command content parser.
    """
    parameters = command_context_parser._parameters
    for parameter in parameters:
        detail = parameter.detail
        if (detail is not None):
            if detail.converter_setting is CONVERTER_SELF_CONTEXT:
                return
    
    for parameter in parameters:
        detail = parameter.detail
        if (detail is not None):
            if detail.converter_setting is CONVERTER_NONE and parameter.name in ('ctx', 'context', 'command_context'):
                parameter.set_converter_setting(CONVERTER_SELF_CONTEXT)
                return


def content_parser_parameter_postprocessor_try_find_message_and_client(command_context_parser):
    """
    Tries to find client and the message variables inside of a command context parser's parameters.
    
    Parameters
    ----------
    command_context_parser : ``CommandContentParser``
        The respective command content parser.
    """
    parameters = command_context_parser._parameters
    if len(parameters) < 2:
        return
    
    parameter_1, parameter_2 = parameters[:2]
    if parameter_1.name not in ('client', 'clnt', 'c'):
        return
    
    if parameter_2.name not in ('message', 'msg', 'm'):
        return
    
    detail = parameter_1.detail
    if detail is None:
        return
    
    converter_setting = detail.converter_setting
    if (converter_setting is not CONVERTER_NONE) and (converter_setting is not CONVERTER_CLIENT):
        return
    
    detail = parameter_2.detail
    if detail is None:
        return
    
    converter_setting = detail.converter_setting
    if (converter_setting is not CONVERTER_NONE) and (converter_setting is not CONVERTER_MESSAGE):
        return
    
    parameter_1.set_converter_setting(CONVERTER_SELF_CLIENT)
    parameter_2.set_converter_setting(CONVERTER_SELF_MESSAGE)


def content_parser_parameter_postprocessor_try_find_rest_parser(command_context_parser):
    """
    Tries to find rest parser
    
    Parameters
    ----------
    command_context_parser : ``CommandContentParser``
        The respective command content parser.
    """
    parameters = command_context_parser._parameters
    if not parameters:
        return
    
    for parameter in parameters:
        if parameter.is_args or parameter.is_kwargs or parameter.is_keyword:
            return
    
    parameter = parameters[-1]
    detail = parameter.detail
    if (detail is None):
        return
    
    if (detail.converter_setting is not CONVERTER_NONE):
        return
    
    parameter.is_rest = True


def convert_parser_parameter_postprocessor_try_find_string(command_context_parser):
    """
    Sets the unset parameters to use string converters.
    
    Parameters
    ----------
    command_context_parser : ``CommandContentParser``
        The respective command content parser.
    """
    parameters = command_context_parser._parameters
    for parameter in parameters:
        detail = parameter.detail
        if (detail is None):
            continue
        
        if (detail.converter_setting is CONVERTER_NONE) and (not parameter.is_rest):
            parameter.set_converter_setting(CONVERTER_STR)


CONTENT_PARSER_PARAMETER_POSTPROCESSORS = [
    content_parser_parameter_postprocessor_try_find_context,
    content_parser_parameter_postprocessor_try_find_message_and_client,
    content_parser_parameter_postprocessor_try_find_rest_parser,
    convert_parser_parameter_postprocessor_try_find_string,
]
