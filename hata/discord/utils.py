﻿__all__ = ('DATETIME_FORMAT_CODE', 'DISCORD_EPOCH', 'Gift', 'Relationship', 'Unknown', 'cchunkify', 'chunkify',
    'elapsed_time', 'filter_content', 'id_to_time', 'is_id', 'is_invite_code', 'is_mention', 'is_role_mention',
    'is_user_mention', 'now_as_id', 'parse_message_reference', 'parse_rdelta', 'parse_tdelta', 'random_id',
    'sanitize_content', 'sanitize_mentions', 'time_to_id',)

import random, sys
from re import compile as re_compile
from datetime import datetime, timedelta, timezone
from base64 import b64encode
from time import time as time_now
from email._parseaddr import _parsedate_tz as parse_date_timezone

try:
    from dateutil.relativedelta import relativedelta
except ImportError:
    relativedelta = None

from ..backend.export import export, include

from .bases import DiscordEntity
from .core import USERS, CHANNELS, ROLES

MESSAGE_JUMP_URL_RP = include('MESSAGE_JUMP_URL_RP')
create_partial_user_from_id = include('create_partial_user_from_id')
RelationshipType = include('RelationshipType')

DATETIME_FORMAT_CODE = '%Y-%m-%d %H:%M:%S'

def endswith_xFFxD9(data):
    """
    Checks whether the given data endswith `b'\xD9\xFF'` ignoring empty bytes at the end of it.
    
    Parameters
    ----------
    data : `bytes-like`
    
    Returns
    -------
    result : `bool`
    """
    index = len(data)-1
    while index > 1:
        actual = data[index]
        if actual == b'\xD9'[0] and data[index-1] == b'\xFF'[0]:
            return True
        
        if actual:
            return False
        
        index -= 1
        continue

def get_image_extension(data):
    """
    Gets the given raw image data's extension and returns it.
    
    Parameters
    ----------
    data : `bytes-like`
        Image data.
    
    Returns
    -------
    extension_name : `str`
    """
    if data.startswith(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'):
        extension_name = 'png'
    elif data.startswith(b'\xFF\xD8') and endswith_xFFxD9(data):
        extension_name = 'jpeg'
    elif data.startswith(b'\x47\x49\x46\x38\x37\x61') or data.startswith(b'\x47\x49\x46\x38\x39\x61'):
        extension_name = 'gif'
    else:
        extension_name = ''
    
    return extension_name

def image_to_base64(data):
    """
    Converts a bytes image to a base64 one.
    
    Parameter
    ----------
    data : `bytes-like`
        Image data.
    
    Returns
    -------
    base64 : `str`
    
    Raises
    ------
    ValueError
        If `ext` was not given and the given `data`'s image format is not any of the expected ones.
    """
    if data.startswith(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'):
        extension_value = 'image/png'
    elif data.startswith(b'\xFF\xD8') and endswith_xFFxD9(data):
        extension_value = 'image/jpeg'
    elif data.startswith(b'\x47\x49\x46\x38\x37\x61') or data.startswith(b'\x47\x49\x46\x38\x39\x61'):
        extension_value = 'image/gif'
    else:
        raise ValueError('Unsupported image type given.')
    
    return ''.join(['data:', extension_value, ';base64,', b64encode(data).decode('ascii')])

DISCORD_EPOCH = 1420070400000
# example dates:
# "2016-03-31T19:15:39.954000+00:00"
# "2019-04-28T15:14:38+00:00"
# at edit:
# "2019-07-17T18:52:50.758993+00:00" #this is before desuppress!
# at desuppress:
# "2019-07-17T18:52:50.758000+00:00"

PARSE_TIME_RP = re_compile('(\\d{4})-(\\d{2})-(\\d{2})T(\\d{2}):(\\d{2}):(\\d{2})(?:\\.(\\d{3})?)?.*')

def parse_time(timestamp):
    """
    Parses the given timestamp.
    
    The expected timestamp formats are the following:
        - `2019-04-28T15:14:38+00:00`
        - `2019-07-17T18:52:50.758993+00:00`
        - `2019-07-17T18:52:50.758000+00:00`
        
    Discord might give timestamps with different accuracy, so we use an optimal middle way at parsing them.
    Some events depend on timestamp accuracy, so we really do not want to be wrong about them, or it might cause
    same internal derpage.
    
    If parsing a timestamp failed, the start of the discord epoch is returned and an error message is given at
    `sys.stderr`.
    
    Parameters
    ----------
    timestamp : `str`
        The timestamp to parse.
    
    Returns
    -------
    time : `datetime`
    
    Notes
    -----
    I already noted that timestamp formats are inconsistent, but even our baka Chiruno could have fix it...
    """
    parsed = PARSE_TIME_RP.fullmatch(timestamp)
    if parsed is None:
        sys.stderr.write(f'Cannot parse timestamp: `{timestamp}`, returning `DISCORD_EPOCH_START`\n')
        return DISCORD_EPOCH_START
    
    year = int(parsed.group(1))
    month = int(parsed.group(2))
    day = int(parsed.group(3))
    hour = int(parsed.group(4))
    minute = int(parsed.group(5))
    second = int(parsed.group(6))
    micro = parsed.group(7)
    
    if micro is None:
        micro = 0
    else:
        micro = int(micro)
    
    return datetime(year, month, day, hour, minute, second, micro)

@export
def id_to_time(id_):
    """
    Converts the given id to datetime.
    
    Parameters
    ----------
    id_ : `int`
        Unique identifier number of a Discord entity.
    
    Returns
    -------
    time : `datetime`
    """
    return datetime.utcfromtimestamp(((id_>>22)+DISCORD_EPOCH)/1000.)

DISCORD_EPOCH_START = id_to_time(0)

def time_to_id(time):
    """
    Converts the given time to it's respective discord identifier number.
    
    Parameters
    ----------
    time : `datetime`
    
    Returns
    -------
    id_ `int`
    """
    return ((time.timestamp()*1000.).__int__()-DISCORD_EPOCH)<<22

def random_id():
    """
    Generates a random Discord identifier number what's datetime value did not surpass the current time.
    
    Returns
    -------
    id_ `int`
    """
    return (((time_now()*1000.).__int__()-DISCORD_EPOCH)<<22)+(random.random()*4194304.).__int__()


def log_time_converter(value):
    """
    Converts the given value to it's snowflake representation.
    
    Parameters
    ----------
    value : `int`, ``DiscordEntity`` instance or `datetime`
        If the value is given as `int`, returns it. If given as a ``DiscordEntity``, then returns it's id and if it
        is given as a `datetime` object, then converts that to snowflake then returns it.
    
    Returns
    -------
    snowflake : `int`
    
    Raises
    ------
    TypeError
        If the given `value`'s type is not any of the expected ones.
    """
    if isinstance(value, int):
        return value
    
    if isinstance(value, DiscordEntity):
        return value.id
    
    if type(value) is datetime:
        return time_to_id(value)
    
    raise TypeError(f'Expected `int`, `{DiscordEntity.__name__}` instance, or a `datetime` object, got '
        f'`{value.__class__.__name__}`.')

APPLICATION_COMMAND_NAME_RP = re_compile('[a-zA-Z0-9_\-]{1,32}')

ID_RP = re_compile('(\d{7,21})')
IS_MENTION_RP = re_compile('@(?:everyone|here)|<(?:@[!&]?|#|/[a-zA-Z0-9_\-]{3,32}:)\d{7,21}>')

USER_MENTION_RP = re_compile('<@!?(\d{7,21})>')
CHANNEL_MENTION_RP = re_compile('<#(\d{7,21})>')
ROLE_MENTION_RP = re_compile('<@&(\d{7,21})>')
APPLICATION_COMMAND_MENTION_RP = re_compile('</([a-zA-Z0-9_\-]{3,32}):(\d{7,21})>')

EMOJI_RP = re_compile('<(a)?:([a-zA-Z0-9_]{2,32})(?:~[1-9])?:(\d{7,21})>')
REACTION_RP = re_compile('([a-zA-Z0-9_]{2,32}):(\d{7,21})')
EMOJI_NAME_RP = re_compile(':?([a-zA-Z0-9_\\-~]{1,32}):?')
FILTER_RP = re_compile('("(.+?)"|\S+)')
INVITE_CODE_RP = re_compile('([a-zA-Z0-9-]+)')

def is_valid_application_command_name(name):
    """
    Returns whether the given application command name is valid.
    
    Parameters
    ----------
    name : `str`
        The name of the application command.
    
    Returns
    -------
    valid : `bool`
    """
    return (APPLICATION_COMMAND_NAME_RP.fullmatch(name) is not None)

def is_id(text):
    """
    Returns whether the given text is a valid snowflake.
    
    Parameters
    ----------
    text : `str`
    
    Returns
    -------
    result : `bool`
    """
    return ID_RP.fullmatch(text) is not None

def is_mention(text):
    """
    Returns whether the given text is a mention.
    
    Parameters
    ----------
    text : `str`
    
    Returns
    -------
    result : `bool`
    """
    return IS_MENTION_RP.fullmatch(text) is not None

def is_user_mention(text):
    """
    Returns whether the given text mentions a user.
    
    Parameters
    ----------
    text : `str`
    
    Returns
    -------
    result : `str`
    """
    return USER_MENTION_RP.fullmatch(text) is not None

def is_channel_mention(text):
    """
    Returns whether the given text mentions a channel.
    
    Parameters
    ----------
    text : `str`
    
    Returns
    -------
    result : `bool`
    """
    return CHANNEL_MENTION_RP.fullmatch(text) is not None

def is_role_mention(text):
    """
    Returns whether the given text mentions a role.
    
    Parameters
    ----------
    text : `str`
    
    Returns
    -------
    result : `bool`
    """
    return ROLE_MENTION_RP.fullmatch(text) is not None

def is_application_command_mention(text):
    """
    Returns whether the given text is an interaction command mention.
    
    Parameters
    ----------
    text : `str`
    
    Returns
    -------
    result : `bool`
    """
    return (APPLICATION_COMMAND_MENTION_RP.fullmatch(text) is not None)

def is_invite_code(text):
    """
    Returns whether the given text is an invite code
    
    Parameters
    ----------
    text : `str`
    
    Returns
    -------
    result : `bool`
    """
    return (INVITE_CODE_RP.fullmatch(text) is not None)

def now_as_id():
    """
    Returns the current time as a Discord snowflake.
    
    Returns
    -------
    snowflake : `int`
    """
    return ((time_now()*1000.)-DISCORD_EPOCH).__int__()<<22

def filter_content(content):
    """
    Filters the given content to parts separated with spaces. Parts surrounded with `"` character will count as one
    even if they contain spaces.
    
    Parameters
    ----------
    content : `str`
    
    Returns
    -------
    parts : `list` of `str`
    """
    return [match[1] or match[0] for match in FILTER_RP.findall(content)]

def chunkify(lines, limit=2000):
    """
    Creates chunks of strings from the given lines.
    
    Parameters
    ----------
    lines : `list` of `str`
        Lines of text to be chunkified.
    limit : `int`, Optional
        The maximal length of a generated chunk.
    
    Returns
    -------
    result : `list` of `str`
    
    Raises
    ------
    ValueError`
        If limit is less than `500`.
    """
    if limit < 500:
        raise ValueError(f'Minimal limit should be at least 500, got {limit!r}.')
    
    result = []
    chunk_length = 0
    chunk = []
    for line in lines:
        while True:
            ln = len(line)+1
            if chunk_length+ln > limit:
                position = limit-chunk_length
                if position < 250:
                    result.append('\n'.join(chunk))
                    chunk.clear()
                    chunk.append(line)
                    chunk_length=ln
                    break
                
                position = line.rfind(' ', position-250, position-3)
                if position == -1:
                    position = limit-chunk_length-3
                    post_part = line[position:]
                else:
                    post_part = line[position+1:]
                
                pre_part = line[:position]+'...'
                
                chunk.append(pre_part)
                result.append('\n'.join(chunk))
                chunk.clear()
                if len(post_part) > limit:
                    line = post_part
                    chunk_length = 0
                    continue
                
                chunk.append(post_part)
                chunk_length = len(post_part)+1
                break
            
            chunk.append(line)
            chunk_length += ln
            break
    
    result.append('\n'.join(chunk))
    
    return result

def cchunkify(lines, lang='', limit=2000):
    """
    Creates code block chunks from the given lines.
    
    Parameters
    ----------
    lines : `list` of `str`
        Lines of text to be chunkified.
    lang : `str`, Optional
        Language prefix of the code-block.
    limit : `int`, Optional
        The maximal length of a generated chunk.
    
    Returns
    -------
    result : `list` of `str`
    
    Raises
    ------
    ValueError`
        If limit is less than `500`.
    """
    if limit < 500:
        raise ValueError(f'Minimal limit should be at least 500, got {limit!r}.')
    
    starter = f'```{lang}'
    limit = limit-len(starter)-5
    
    result = []
    chunk_length = 0
    chunk = [starter]
    for line in lines:
        while True:
            ln = len(line)+1
            if chunk_length+ln > limit:
                position = limit-chunk_length
                if position < 250:
                    chunk.append('```')
                    result.append('\n'.join(chunk))
                    chunk.clear()
                    chunk.append(starter)
                    chunk.append(line)
                    chunk_length = ln
                    break
                
                position = line.rfind(' ', position-250, position-3)
                if position == -1:
                    position = limit-chunk_length-3
                    post_part = line[position:]
                else:
                    post_part = line[position+1:]
                
                pre_part = line[:position]+'...'
                
                chunk.append(pre_part)
                chunk.append('```')
                result.append('\n'.join(chunk))
                chunk.clear()
                chunk.append(starter)
                
                if len(post_part) > limit:
                    line = post_part
                    chunk_length = 0
                    continue
                
                chunk.append(post_part)
                chunk_length = len(post_part)+1
                break
            
            chunk.append(line)
            chunk_length += ln
            break
    
    if len(chunk)>1:
        chunk.append('```')
        result.append('\n'.join(chunk))
    
    return result

if relativedelta is None:
    elapsed_time = None
else:
    def elapsed_time(delta, limit=3, names=(
            ('year', 'years',),
            ('month', 'months'),
            ('day', 'days', ),
            ('hour', 'hours'),
            ('minute', 'minutes'),
            ('second', 'seconds'),)):
        """
        Generates an elapsed time formula from the given time delta.
        
        Parameters
        ----------
        delta : `datetime` or `relativedelta`
            The time delta. If given as `datetime`, then the delta will be based on the difference between the given
            datetime and the actual time. If given as `relativedelta`, then that will be used directly.
        limit : `int`, Optional
            The maximal amount of connected time units. Defaults to `3`.
        names : `iterable` of `tuple` (`str`, `str`), Optional
            The names of the time units starting from years. Each element of the iterable should yield a `tuple` of two
            `str` elements. The first should be always the singular form of the time unit's name and the second the
            plural. Defaults to the time units' names in engrisssh.
        
        Returns
        -------
        result : `str`
        
        Raises
        ------
        TypeError
            If delta was neither passed as `datetime` or as `relativedelta` instance.
        """
        if isinstance(delta, datetime):
            delta = relativedelta(datetime.utcnow(), delta)
        elif isinstance(delta, relativedelta):
            pass
        else:
            raise TypeError(f'Expected, `relativedelta` or `datetime`, got {delta.__class__.__name__}.')
        
        parts = []
        for value, name_pair in zip((delta.years, delta.months, delta.days, delta.hours, delta.minutes, delta.seconds), names):
            if limit == 0:
                break
            
            if value < 0:
                 value = -value
            elif value == 0:
                continue
            
            parts.append(str(value))
            parts.append(' ')
            
            name = name_pair[value!=1]
            
            parts.append(name)
            parts.append(', ')
            
            limit -= 1
        
        if parts:
            del parts[-1]
            result = ''.join(parts)
        else:
            result = f'0 {names[5][0]}'
        
        return result


class Relationship:
    """
    Represents a Discord relationship.
    
    Attributes
    ----------
    type : ``RelationshipType``
        The relationship's type.
    user : ``User`` or ``Client`` instance
        The target user of the relationship.
    """
    __slots__ = ('type', 'user',)
    def __init__(self, client, data, user_id):
        """
        Creates a relationship instance with the given parameters.
        
        Parameters
        ----------
        client : ``Client``
            The client, who's relationship is created.
        data : `dict` of (`str`, `Any`)
            Relationship data.
        user_id : `int`
            The relationship's target user's id.
        """
        self.user = create_partial_user_from_id(user_id)
        self.type = RelationshipType.get(data['type'])
        client.relationships[user_id] = self
    
    def __repr__(self):
        """Returns the representation of the relationship."""
        return f'<{self.__class__.__name__} {self.type.name} user={self.user.full_name!r}>'


class Unknown(DiscordEntity):
    """
    Represents a not found object when creating an ``AuditLog``.
    
    Attributes
    ----------
    id : `int`
        The entity's unique identifier number.
    name : `str`
        The entity's name.
    type : `str`
        The entity's respective type's respective name.
        
        Can be one of:
        - `'Channel'`
        - `'Emoji'`
        - `'Integration'`
        - `'Invite'`
        - `'Message'`
        - `'Role'`
        - `'User'`
        - `'Webhook'`
    """
    __slots__ = ('name', 'type', )
    
    def __init__(self, type_, id_, name=None):
        """
        Creates a new ``Unknown`` object from the given parameters.
        
        Parameters
        ----------
        type_ : `str`
            The entity's respective type's respective name.
        id_ : `int`
            The entity's unique identifier number.
        name : `str`, Optional
            The name of the entity if applicable. If not, `type_` will be used as name instead.
        """
        self.type = type_
        self.id = id_
        if name is None:
            name = type_
        self.name = name
    
    def __repr__(self):
        """Returns the representation of the entity."""
        return f'<{self.__class__.__name__} type={self.type} id={self.id} name={self.name!r}>'
    
    def __gt__(self, other):
        """Returns whether this entity's respective type matches with the other's and it's id is greater than the
        other's."""
        if type(other) is type(self):
            if self.type != other.type:
                return NotImplemented
        elif isinstance(other, DiscordEntity):
            if self.type not in other.__class__.__name__:
                return NotImplemented
        else:
            return NotImplemented
        
        return (self.id > other.id)
    
    def __ge__(self ,other):
        """Returns whether this entity's respective type matches with the other's and it's id is greater or equal to
        the other's."""
        if type(other) is type(self):
            if self.type != other.type:
                return NotImplemented
        elif isinstance(other, DiscordEntity):
            if self.type not in other.__class__.__name__:
                return NotImplemented
        else:
            return NotImplemented
        
        return (self.id >= other.id)
    
    def __eq__(self, other):
        """Returns whether this entity's respective type matches with the other's and it's id equals to the other's."""
        if type(other) is type(self):
            if self.type != other.type:
                return NotImplemented
        elif isinstance(other, DiscordEntity):
            if self.type not in other.__class__.__name__:
                return NotImplemented
        else:
            return NotImplemented
        
        return (self.id == other.id)
    
    def __ne__(self,other):
        """Returns whether this entity's respective type matches with the other's and it's id not equals to the
        other's."""
        if type(other) is type(self):
            if self.type != other.type:
                return NotImplemented
        elif isinstance(other, DiscordEntity):
            if self.type not in other.__class__.__name__:
                return NotImplemented
        else:
            return NotImplemented
        
        return (self.id != other.id)
    
    def __le__(self,other):
        """Returns whether this entity's respective type matches with the other's and it's id is less or equal to
        the other's."""
        if type(other) is type(self):
            if self.type != other.type:
                return NotImplemented
        elif isinstance(other, DiscordEntity):
            if self.type not in other.__class__.__name__:
                return NotImplemented
        else:
            return NotImplemented
        
        return (self.id <= other.id)
    
    def __lt__(self,other):
        """Returns whether this entity's respective type matches with the other's and it's id is less than the
        other's."""
        if type(other) is type(self):
            if self.type != other.type:
                return NotImplemented
        elif isinstance(other, DiscordEntity):
            if self.type not in other.__class__.__name__:
                return NotImplemented
        else:
            return NotImplemented
        
        return (self.id < other.id)

class Gift:
    """
    Represents a Discord gift.
    
    Attributes
    ----------
    code : `str`
        The code of the gift.
    uses : `int`
        The amount how much time the gift can be used.
    """
    __slots__ = ('code', 'uses', )
    def __init__(self, data):
        """
        Creates a new ``Gift`` object from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Gift data received from Discord.
        """
        self.uses = data['uses']
        self.code = data['code']


def url_cutter(url):
    """
    Cuts down the given url to a more suitable length.
    
    Parameters
    ----------
    url : `str`
    
    Returns
    -------
    result : `str`
    """
    if len(url) < 50:
        return url
    
    position = url.find('/')
    
    if position == -1:
        return f'{url[:28]}...{url[-19:]}'
    
    position += 1
    if url[position] == '/':
        position += 1
        if position == len(url):
            return f'{url[:28]}...{url[-19:]}'
        
        position = url.find('/', position)
        position +=1
        if position == 0 or position == len(url):
            return f'{url[:28]}...{url[-19:]}'
    
    positions = [position]
    
    while True:
        position = url.find('/', position)
        if position == -1:
            break
        position +=1
        if position == len(url):
            break
        positions.append(position)
    
    from_start = 0
    from_end = 0
    top_limit = len(url)
    index = 0
    
    while True:
        value = positions[index]
        if value+from_end > 47:
            if from_start+from_end < 33:
                from_start = 47-from_end
                break
            else:
                index +=1
                if index == len(positions):
                    value  =0
                else:
                    value = positions[len(positions)-index]
                value = top_limit-value
                if value+from_start>47:
                    break
                else:
                    from_end = value
                    break
        from_start = value
        
        index = index+1
        value = positions[len(positions)-index]
        value = top_limit-value
        if value+from_start > 47:
            if from_start+from_end < 33:
                from_end = 47-from_start
                break
            else:
                if index == len(positions):
                    value = top_limit
                else:
                    value = positions[index]
                
                if value+from_end > 47:
                    break
                else:
                    from_start = value
                    break
        from_end = value
        
    return f'{url[:from_start]}...{url[top_limit-from_end-1:]}'

DELTA_RP = re_compile('([\+\-]?\d+)[ \t]*([a-zA-Z]+)')
TDELTA_KEYS = ('weeks', 'days', 'hours', 'minutes', 'seconds', 'microseconds')
RDELTA_KEYS = ('years', 'months', *TDELTA_KEYS)

def parse_tdelta(text):
    """
    Tries to parse out a ``timedelta`` from the inputted text.
    
    Returns
    -------
    tdelta : `None` or `datetime.timedelta`
    """
    text = text.lower()
    
    result = {}
    index = 0
    limit = len(TDELTA_KEYS)
    for amount, name in DELTA_RP.findall(text):
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

if relativedelta is None:
    parse_rdelta = None
else:
    def parse_rdelta(text):
        """
        Tries to parse out a ``relativedelta`` from the inputted text.
        
        Returns
        -------
        rdelta : `None` or `dateutil.relativedelta.relativedelta`
        """
        text = text.lower()
        
        result = {}
        index = 0
        limit = len(RDELTA_KEYS)
        for amount, name in DELTA_RP.findall(text):
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

CHANNEL_MESSAGE_RP = re_compile('(\d{7,21})-(\d{7,21})')

def parse_message_reference(text):
    """
    Tries the parse a ``Message``'s reference from the inputted text.
    
    Accepts the following formats:
    - `{message.id}`
    - `{channel.id}-{message.id}`
    - `{message.url}`
    
    Returns
    -------
    reference : `None` or `tuple` (`int`, `int`, `int`)
        On successful parsing returns a tuple of 3 elements:
        +-------------------+-------------------+-------------------------------+-------------------+---------------+
        | Respective name   | Parse-able from   | Parse-able from               | Parse-able from   | Default value |
        |                   | `{message.id}`    | `{channel.id}-{message.id}`   | `{message.url}`   |               |
        +===================+===================+===============================+=================+++===============+
        | `guild.id`        | False             | False                         | True              | `0`           |
        +-------------------+-------------------+-------------------------------+-------------------+---------------+
        | `channel.id       | False             | True                          | True              | `0`           |
        +-------------------+-------------------+-------------------------------+-------------------+---------------+
        | `message.id`      | True              | True                          | True              | N/A           |
        +-------------------+-------------------+-------------------------------+-------------------+---------------+
    """
    parsed = ID_RP.fullmatch(text)
    if (parsed is not None):
        message_id = int(parsed.group(1))
        
        guild_id = 0
        channel_id = 0
    else:
        parsed = CHANNEL_MESSAGE_RP.fullmatch(text)
        if (parsed is not None):
            channel_id, message_id = parsed.groups()
            channel_id = int(channel_id)
            message_id = int(message_id)
            
            guild_id = 0
        else:
            parsed = MESSAGE_JUMP_URL_RP.fullmatch(text)
            if (parsed is not None):
                guild_id, channel_id, message_id = parsed.groups()
                if guild_id == '@me':
                    guild_id = 0
                else:
                    guild_id = int(guild_id)
                channel_id = int(channel_id)
                message_id = int(message_id)
            else:
                return None
    
    return guild_id, channel_id, message_id


def sanitize_mentions(content, guild=None):
    """
    Sanitizes the given content, removing the mentions from it.
    
    Parameters
    ----------
    content : `str`
        The content to sanitize.
    guild : `None` or ``Guild``, Optional
        Respective context to look up guild specific names of entities.
    
    Returns
    -------
    content : `str`
    """
    transformations = {
        '@everyone':'@\u200beveryone',
        '@here':'@\u200bhere',
    }
    
    for id_ in USER_MENTION_RP.findall(content):
        id_ = int(id_)
        user = USERS.get(id_, None)
        if (user is None) or user.partial:
            sanitized_mention = '@invalid-user'
        else:
            sanitized_mention = '@'+user.name_at(guild)
        
        transformations[f'<@{id_}>'] = sanitized_mention
        transformations[f'<@!{id_}>'] = sanitized_mention
        
    for id_ in CHANNEL_MENTION_RP.findall(content):
        id_ = int(id_)
        channel = CHANNELS.get(id_, None)
        if (channel is None) or channel.partial:
            sanitized_mention = '@deleted channel'
        else:
            sanitized_mention = '#'+channel.name
        
        transformations[f'<#{id_}>'] = sanitized_mention
    
    for id_ in ROLE_MENTION_RP.findall(content):
        id_ = int(id_)
        role = ROLES.get(id_, None)
        if (role is None) or role.partial:
            sanitized_mention = '@deleted role'
        else:
            sanitized_mention = '@'+role.name
        
        transformations[f'<@&{id_}>'] = sanitized_mention
    
    return re_compile('|'.join(transformations)).sub(
        lambda mention: transformations[mention.group(0)], content)


def sanitize_content(content, guild=None):
    """
    Sanitizes the markdown and the mentions in the given content.
    
    Parameters
    ----------
    content : `str`
        The content to sanitize.
    guild : `None` or ``Guild``, Optional
        Respective context to look up guild specific names of entities.
    
    Returns
    -------
    content : `str`
    """
    content = content.replace('\\', '\\\\')
    content = content.replace('_', '\\_')
    content = content.replace('*', '\\*')
    content = content.replace('|', '\\|')
    content = content.replace('~', '\\~')
    content = content.replace('`', '\\`')
    content = sanitize_mentions(content, guild=guild)
    return content


def parse_date_header_to_datetime(date_data):
    """
    Parsers header date value to `datetime`.
    
    Parameters
    ----------
    date_data : ``str``
        Date value inside of a header.

    Returns
    -------
    date : `datetime`
        The parsed out date time.
    """
    *date_tuple, tz = parse_date_timezone(date_data)
    if tz is None:
        date = datetime(*date_tuple[:6])
    else:
        date = datetime(*date_tuple[:6], tzinfo=timezone(timedelta(seconds=tz)))
    return date
