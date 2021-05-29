__all__ = ('MessageType', 'MessageActivityType', 'StickerFormat', 'StickerType')

from ...backend.export import export
from ...backend.utils import any_to_any

from ..bases import PreinstancedBase, Preinstance as P
from ..utils import sanitize_mentions
from ..activity import ActivityTypes

class MessageActivityType(PreinstancedBase):
    """
    Represents a ``MessageActivity``'s type.
    
    Attributes
    ----------
    name : `str`
        The default name of the message activity type.
    value : `int`
        The Discord side identifier value of the message activity type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``MessageActivityType``) items
        Stores the predefined ``MessageActivityType`` instances. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The message activity types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the verification levels.
    
    Every predefined message activity type can be accessed as class attribute as well:
    
    +-----------------------+---------------+-------+
    | Class attribute name  | name          | value |
    +=======================+===============+=======+
    | none                  | none          | 0     |
    +-----------------------+---------------+-------+
    | join                  | join          | 1     |
    +-----------------------+---------------+-------+
    | spectate              | spectate      | 2     |
    +-----------------------+---------------+-------+
    | listen                | listen        | 3     |
    +-----------------------+---------------+-------+
    | watch                 | watch         | 4     |
    +-----------------------+---------------+-------+
    | join_request          | join_request  | 5     |
    +-----------------------+---------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    join = P(1, 'join')
    spectate = P(2, 'spectate')
    listen = P(3, 'listen')
    watch = P(4, 'watch')
    join_request = P(5, 'join_request')



def MESSAGE_DEFAULT_CONVERTER(self):
    """
    Default message content converter.
    
    Parameters
    ----------
    self : ``Message``
        The message, what's content will be converted.
    
    Returns
    -------
    content : `str`
        The converted content if applicable. Might be empty string.
    """
    content = self.content
    if content:
        content = sanitize_mentions(content, self.guild)
    
    return content


def convert_add_user(self):
    return f'{self.author.name} added {self.user_mentions[0].name} to the group.'

def convert_remove_user(self):
    return f'{self.author.name} removed {self.user_mentions[0].name} from the group.'

def convert_call(self):
    if any_to_any(self.channel.clients, self.call.users):
        return f'{self.author.name} started a call.'
    if self.call.ended_timestamp is None:
        return f'{self.author.name} started a call \N{EM DASH} Join the call.'
    return f'You missed a call from {self.author.name}'

def convert_channel_name_change(self):
    return f'{self.author.name} changed the channel name: {self.content}'

def convert_channel_icon_change(self):
    return f'{self.author.name} changed the channel icon.'

def convert_new_pin(self):
    return f'{self.author.name} pinned a message to this channel.'

# TODO: this system changed, just pulled out the new texts from the js client source, but the calculation is bad
def convert_welcome(self):
    # tuples with immutable elements are stored directly
    join_messages = (
        '{0} just joined the server - glhf!',
        '{0} just joined. Everyone, look busy!',
        '{0} just joined. Can I get a heal?',
        '{0} joined your party.',
        '{0} joined. You must construct additional pylons.',
        'Ermagherd. {0} is here.',
        'Welcome, {0}. Stay awhile and listen.',
        'Welcome, {0}. We were expecting you ( ͡° ͜ʖ ͡°)',
        'Welcome, {0}. We hope you brought pizza.',
        'Welcome {0}. Leave your weapons by the door.',
        'A wild {0} appeared.',
        'Swoooosh. {0} just landed.',
        'Brace yourselves. {0} just joined the server.',
        '{0} just joined... or did they?',
        '{0} just arrived. Seems OP - please nerf.',
        '{0} just slid into the server.',
        'A {0} has spawned in the server.',
        'Big {0} showed up!',
        'Where’s {0}? In the server!',
        '{0} hopped into the server. Kangaroo!!',
        '{0} just showed up. Hold my beer.',
        'Challenger approaching - {0} has appeared!',
        'It\'s a bird! It\'s a plane! Nevermind, it\'s just {0}.',
        'It\'s {0}! Praise the sun! [T]/',
        'Never gonna give {0} up. Never gonna let {0} down.',
        '{0} has joined the battle bus.',
        'Cheers, love! {0}\'s here!',
        'Hey! Listen! {0} has joined!',
        'We\'ve been expecting you {0}',
        'It\'s dangerous to go alone, take {0}!',
        '{0} has joined the server! It\'s super effective!',
        'Cheers, love! {0} is here!',
        '{0} is here, as the prophecy foretold.',
        '{0} has arrived. Party\'s over.',
        'Ready player {0}',
        '{0} is here to kick butt and chew bubblegum. And {0} is all out of gum.',
        'Hello. Is it {0} you\'re looking for?',
        '{0} has joined. Stay a while and listen!',
        'Roses are red, violets are blue, {0} joined this server with you',
    )

    return join_messages[int(self.created_at.timestamp())%len(join_messages)].format(self.author.name)

def convert_new_guild_sub(self):
    guild = self.channel.guild
    if guild is None:
        guild_name = 'None'
    else:
        guild_name = guild.name
    return f'{self.author.name} boosted {guild_name} with Nitro!'

def convert_new_guild_sub_t1(self):
    guild = self.channel.guild
    if guild is None:
        guild_name = 'None'
    else:
        guild_name = guild.name
        
    return f'{self.author.name} boosted {guild_name} with Nitro! {guild_name} has achieved level 1!'

def convert_new_guild_sub_t2(self):
    guild = self.channel.guild
    if guild is None:
        guild_name = 'None'
    else:
        guild_name = guild.name
    
    return f'{self.author.name} boosted {guild_name} with Nitro! {guild_name} has achieved level 2!'

def convert_new_guild_sub_t3(self):
    guild = self.channel.guild
    if guild is None:
        guild_name = 'None'
    else:
        guild_name = guild.name
        
    return f'{self.author.name} boosted {guild_name} with Nitro! {guild_name} has achieved level 3!'

def convert_new_follower_channel(self):
    channel = self.channel
    guild = channel.guild
    if guild is None:
        guild_name = 'None'
    else:
        guild_name = guild.name
    
    user_name = self.author.name_at(guild)
    
    return (f'{user_name} has added {guild_name} #{channel.name} to this channel. Its most important updates '
        'will show up here.')

def convert_stream(self):
    user = self.author
    for activity in user.activities:
        if activity.type == ActivityTypes.stream:
            activity_name = activity.name
            break
    else:
        activity_name = 'Unknown'
    
    user_name = user.name_at(self.guild)
    
    return f'{user_name} is live! Now streaming {activity_name}'

def convert_discovery_disqualified(self):
    return ('This server has been removed from Server Discovery because it no longer passes all the requirements. '
        'Check `Server Settings` for more details.')

def convert_discovery_requalified(self):
    return 'This server is eligible for Server Discovery again and has been automatically relisted!'

def convert_discovery_grace_period_initial_warning(self):
    return ('This server has failed Discovery activity requirements for 1 week. If this server fails for 4 weeks in '
        'a row, it will be automatically removed from Discovery.')

def convert_discovery_grace_period_final_warning(self):
    return ('This server has failed Discovery activity requirements for 3 weeks in a row. If this server fails for 1 '
        'more week, it will be removed from Discovery.')

def convert_thread_created(self):
    user_name = self.author.name_at(self.guild)
    return f'{user_name} started a thread'

def convert_invite_reminder(self):
    return 'Wondering who to invite?\nStart by inviting anyone who can help you build the server!'

class MessageType(PreinstancedBase):
    """
    Represents a ``Message``'s type.
    
    Attributes
    ----------
    convert : `function`
        The converter function of the message type, what tries to convert the message's content to it's Discord side
        representation.
    name : `str`
        The default name of the message type.
    value : `int`
        The Discord side identifier value of the message type.
    VALUE_TYPE : `type` = `int`
        The message types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the message types.
    DEFAULT_CONVERT : `function`
        The default ``.convert`` attribute of the message types.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``MessageType``) items
        Stores the predefined ``MessageType`` instances. These can be accessed with their `value` as key.
    
    Every predefined message type can be accessed as class attribute as well:
    
    +-------------------------------------------+---------------------------------------------------+-------+
    | Class attribute name & name               | convert                                           | value |
    +===========================================+===================================================+=======+
    | default                                   | MESSAGE_DEFAULT_CONVERTER                         | 0     |
    +-------------------------------------------+---------------------------------------------------+-------+
    | add_user                                  | convert_add_user                                  | 1     |
    +-------------------------------------------+---------------------------------------------------+-------+
    | remove_user                               | convert_remove_user                               | 2     |
    +-------------------------------------------+---------------------------------------------------+-------+
    | call                                      | convert_call                                      | 3     |
    +-------------------------------------------+---------------------------------------------------+-------+
    | channel_name_change                       | convert_channel_name_change                       | 4     |
    +-------------------------------------------+---------------------------------------------------+-------+
    | channel_icon_change                       | convert_channel_icon_change                       | 5     |
    +-------------------------------------------+---------------------------------------------------+-------+
    | new_pin                                   | convert_new_pin                                   | 6     |
    +-------------------------------------------+---------------------------------------------------+-------+
    | welcome                                   | convert_welcome                                   | 7     |
    +-------------------------------------------+---------------------------------------------------+-------+
    | new_guild_sub                             | convert_new_guild_sub                             | 8     |
    +-------------------------------------------+---------------------------------------------------+-------+
    | new_guild_sub_t1                          | convert_new_guild_sub_t1                          | 9     |
    +-------------------------------------------+---------------------------------------------------+-------+
    | new_guild_sub_t2                          | convert_new_guild_sub_t2                          | 10    |
    +-------------------------------------------+---------------------------------------------------+-------+
    | new_guild_sub_t3                          | convert_new_guild_sub_t3                          | 11    |
    +-------------------------------------------+---------------------------------------------------+-------+
    | new_follower_channel                      | convert_new_follower_channel                      | 12    |
    +-------------------------------------------+---------------------------------------------------+-------+
    | stream                                    | convert_stream                                    | 13    |
    +-------------------------------------------+---------------------------------------------------+-------+
    | discovery_disqualified                    | convert_discovery_disqualified                    | 14    |
    +-------------------------------------------+---------------------------------------------------+-------+
    | discovery_requalified                     | convert_discovery_requalified                     | 15    |
    +-------------------------------------------+---------------------------------------------------+-------+
    | discovery_grace_period_initial_warning    | convert_discovery_grace_period_initial_warning    | 16    |
    +-------------------------------------------+---------------------------------------------------+-------+
    | discovery_grace_period_final_warning      | convert_discovery_grace_period_final_warning      | 17    |
    +-------------------------------------------+---------------------------------------------------+-------+
    | thread_created                            | convert_thread_created                            | 18    |
    +-------------------------------------------+---------------------------------------------------+-------+
    | inline_reply                              | MESSAGE_DEFAULT_CONVERTER                         | 19    |
    +-------------------------------------------+---------------------------------------------------+-------+
    | application_command                       | MESSAGE_DEFAULT_CONVERTER                         | 20    |
    +-------------------------------------------+---------------------------------------------------+-------+
    | thread_started                            | MESSAGE_DEFAULT_CONVERTER                         | 21    |
    +-------------------------------------------+---------------------------------------------------+-------+
    | invite_reminder                           | convert_invite_reminder                           | 22    |
    +-------------------------------------------+---------------------------------------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ('convert',)
    
    @classmethod
    def _from_value(cls, value):
        """
        Creates a new message type with the given value.
        
        Parameters
        ----------
        value : `int`
            The message type's identifier value.
        
        Returns
        -------
        self : ``MessageType``
            The created instance.
        """
        self = object.__new__(cls)
        self.name = cls.DEFAULT_NAME
        self.value = value
        self.convert = MESSAGE_DEFAULT_CONVERTER
        
        return self
    
    def __init__(self, value, name, convert):
        """
        Creates an ``MessageType`` and stores it at the class's `.INSTANCES` class attribute as well.
        
        Parameters
        ----------
        value : `int`
            The Discord side identifier value of the message type.
        name : `str`
            The default name of the message type.
        convert : `function`
            The converter function of the message type.
        """
        self.value = value
        self.name = name
        self.convert = convert
        
        self.INSTANCES[value] = self
    
    def __repr__(self):
        """Returns the representation of the message type."""
        return f'{self.__class__.__name__}(value={self.value!r}, name={self.name!r}, covert={self.convert!r})'
    
    # predefined
    default = P(0, 'default', MESSAGE_DEFAULT_CONVERTER)
    add_user = P(1, 'add_user', convert_add_user)
    remove_user = P(2, 'remove_user', convert_remove_user)
    call = P(3, 'call', convert_call)
    channel_name_change = P(4, 'channel_name_change', convert_channel_name_change)
    channel_icon_change = P(5, 'channel_icon_change', convert_channel_icon_change)
    new_pin = P(6, 'new_pin', convert_new_pin)
    welcome = P(7, 'welcome', convert_welcome)
    new_guild_sub = P(8, 'new_guild_sub', convert_new_guild_sub)
    new_guild_sub_t1 = P(9, 'new_guild_sub_t1', convert_new_guild_sub_t1)
    new_guild_sub_t2 = P(10, 'new_guild_sub_t2', convert_new_guild_sub_t2)
    new_guild_sub_t3 = P(11, 'new_guild_sub_t3', convert_new_guild_sub_t3)
    new_follower_channel = P(12, 'new_follower_channel', convert_new_follower_channel)
    stream = P(13, 'stream', convert_stream)
    discovery_disqualified = P(14, 'discovery_disqualified', convert_discovery_disqualified)
    discovery_requalified = P(15, 'discovery_requalified', convert_discovery_requalified)
    discovery_grace_period_initial_warning = P(16, 'discovery_grace_period_initial_warning',
        convert_discovery_grace_period_initial_warning)
    discovery_grace_period_final_warning = P(17, 'discovery_grace_period_final_warning',
        convert_discovery_grace_period_final_warning)
    thread_created = P(18, 'thread_created', convert_thread_created)
    inline_reply = P(19, 'inline_reply', MESSAGE_DEFAULT_CONVERTER)
    application_command = P(20, 'application_command', MESSAGE_DEFAULT_CONVERTER)
    thread_started = P(21, 'thread_started', MESSAGE_DEFAULT_CONVERTER)
    invite_reminder = P(22, 'invite_reminder', convert_invite_reminder)

del convert_add_user
del convert_remove_user
del convert_call
del convert_channel_name_change
del convert_channel_icon_change
del convert_new_pin
del convert_welcome
del convert_new_guild_sub
del convert_new_guild_sub_t1
del convert_new_guild_sub_t2
del convert_new_guild_sub_t3
del convert_new_follower_channel
del convert_stream
del convert_discovery_disqualified
del convert_discovery_requalified
del convert_discovery_grace_period_initial_warning
del convert_discovery_grace_period_final_warning
del convert_thread_created
del convert_invite_reminder


@export
class StickerFormat(PreinstancedBase):
    """
    Represents a message sticker's format's type.
    
    Attributes
    ----------
    name : `str`
        The name of the message sticker format type.
    value : `int`
        The Discord side identifier value of the message sticker format type.
    extension : `str`
        The extension of the sticker format type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``StickerFormat``) items
        Stores the predefined ``StickerFormat`` instances. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The message sticker format type' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the sticker format types.
    DEFAULT_EXTENSION : `str` = `'png'`
        The default extension of the sticker format type.
    
    Every predefined sticker format type can be accessed as class attribute as well:
    
    +-----------------------+-----------+-------+---------------+
    | Class attribute name  | name      | value | extension     |
    +=======================+===========+=======+===============+
    | none                  | none      | 0     | png           |
    +-----------------------+-----------+-------+---------------+
    | png                   | png       | 1     | png           |
    +-----------------------+-----------+-------+---------------+
    | apng                  | apng      | 2     | png           |
    +-----------------------+-----------+-------+---------------+
    | lottie                | lottie    | 3     | json          |
    +-----------------------+-----------+-------+---------------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    DEFAULT_EXTENSION = 'png'
    
    __slots__ = ('extension', )
    
    @classmethod
    def _from_value(cls, value):
        """
        Creates a sticker format type from the given id and stores it at class's `.INSTANCES`.
        
        Called by `.get` when no sticker format type was found with the given id.
        
        Parameters
        ----------
        id_ : `int`
            The identifier of the sticker format type.
        
        Returns
        -------
        sticker_format_type : ``StickerFormat``
        """
        self = object.__new__(cls)
        self.name = cls.DEFAULT_NAME
        self.value = value
        self.extension = cls.DEFAULT_EXTENSION
        self.INSTANCES[value] = self
        return self
    
    def __init__(self, value, name, extension):
        """
        Creates a new sticker format type with the given parameters and stores it at the class's `.INSTANCES`.
        
        Parameters
        ----------
        value : `int`
            The Discord side identifier value of the message sticker format type.
        name : `str`
            The name of the message sticker format type.
        extension : `str`
            The extension of the sticker format type.
        """
        self.name = name
        self.value = value
        self.extension = extension
        self.INSTANCES[value] = self
    
    # predefined
    none = P(0, 'none', 'png')
    png = P(1, 'png', 'png')
    apng = P(2, 'apng', 'png')
    lottie = P(3, 'lottie', 'json')


class StickerType(PreinstancedBase):
    """
    Represents a message sticker's type.
    
    Attributes
    ----------
    name : `str`
        The name of the message sticker type.
    value : `int`
        The Discord side identifier value of the message sticker type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``StickerType``) items
        Stores the predefined ``StickerType`` instances. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The message sticker types' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the sticker types.
    
    Every predefined sticker type can be accessed as class attribute as well:
    
    +-----------------------+-----------+-------+
    | Class attribute name  | name      | value |
    +=======================+===========+=======+
    | none                  | none      | 0     |
    +-----------------------+-----------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
