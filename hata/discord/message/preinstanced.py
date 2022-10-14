__all__ = ('MessageType', 'MessageActivityType')

import warnings

from scarletio import any_to_any, class_property

from ..activity import ACTIVITY_TYPES
from ..bases import Preinstance as P, PreinstancedBase
from ..utils import sanitize_mentions


class MessageActivityType(PreinstancedBase):
    """
    Represents a ``MessageActivity``'s type.
    
    Attributes
    ----------
    name : `str`
        The name of the message activity type.
    value : `int`
        The Discord side identifier value of the message activity type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``MessageActivityType``) items
        Stores the predefined ``MessageActivityType``-s. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The message activity types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the message activity types.
    
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
    content : `None`, `str`
        The converted content if applicable. Might be empty string.
    """
    content = self.content
    if (content is not None):
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

    return join_messages[int(self.created_at.timestamp()) % len(join_messages)].format(self.author.name)

def convert_guild_boost(self):
    guild = self.channel.guild
    if guild is None:
        guild_name = 'None'
    else:
        guild_name = guild.name
    return f'{self.author.name} boosted {guild_name} with Nitro!'

def convert_guild_boost_tier_1(self):
    guild = self.channel.guild
    if guild is None:
        guild_name = 'None'
    else:
        guild_name = guild.name
        
    return f'{self.author.name} boosted {guild_name} with Nitro! {guild_name} has achieved level 1!'

def convert_guild_boost_tier_2(self):
    guild = self.channel.guild
    if guild is None:
        guild_name = 'None'
    else:
        guild_name = guild.name
    
    return f'{self.author.name} boosted {guild_name} with Nitro! {guild_name} has achieved level 2!'

def convert_guild_boost_tier_3(self):
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
    
    return (
        f'{user_name} has added {guild_name} #{channel.name} to this channel. '
        f'Its most important updates will show up here.'
    )

def convert_stream(self):
    user = self.author
    for activity in user.activities:
        if activity.type == ACTIVITY_TYPES.stream:
            activity_name = activity.name
            break
    else:
        activity_name = 'Unknown'
    
    user_name = user.name_at(self.guild)
    
    return f'{user_name} is live! Now streaming {activity_name}'

def convert_discovery_disqualified(self):
    return (
        'This server has been removed from Server Discovery because it no longer passes all the requirements. '
        'Check `Server Settings` for more details.'
    )

def convert_discovery_requalified(self):
    return 'This server is eligible for Server Discovery again and has been automatically relisted!'

def convert_discovery_grace_period_initial_warning(self):
    return (
        'This server has failed Discovery activity requirements for 1 week. '
        'If this server fails for 4 weeks in a row, it will be automatically removed from Discovery.'
    )

def convert_discovery_grace_period_final_warning(self):
    return (
        'This server has failed Discovery activity requirements for 3 weeks in a row. '
        'If this server fails for 1 more week, it will be removed from Discovery.'
    )

def convert_thread_created(self):
    guild_id = self.guild_id
    user = self.author
    
    if guild_id:
        try:
            guild_profile = user.guild_profiles[guild_id]
        except KeyError:
            user_name = user.name
        else:
            user_name = guild_profile.nick
            if (user_name is None):
                user_name = user.name
    else:
        user_name = user.name
    
    return f'{user_name} started a thread'


def convert_invite_reminder(self):
    return (
        'Wondering who to invite?\n'
        'Start by inviting anyone who can help you build the server!'
    )


class MessageType(PreinstancedBase):
    """
    Represents a ``Message``'s type.
    
    Attributes
    ----------
    name : `str`
        The default name of the message type.
    value : `int`
        The Discord side identifier value of the message type.
    converter : `FunctionType`
        The converter function of the message type, what tries to convert the message's content to it's Discord side
        representation.
    deletable : `bool`
        Whether the message with this type can be deleted.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``MessageType``) items
        Stores the predefined ``MessageType``-s. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The message types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the message types.
    
    Every predefined message type can be accessed as class attribute as well:
    
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | Class attribute name                      | Name                                      | Value | Converter                                         | Deletable |
    +===========================================+===========================================+=======+===================================================+===========+
    | default                                   | default                                   | 0     | MESSAGE_DEFAULT_CONVERTER                         | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | add_user                                  | add user                                  | 1     | convert_add_user                                  | false     |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | remove_user                               | remove user                               | 2     | convert_remove_user                               | false     |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | call                                      | call                                      | 3     | convert_call                                      | false     |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | channel_name_change                       | channel name change                       | 4     | convert_channel_name_change                       | false     |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | channel_icon_change                       | channel icon change                       | 5     | convert_channel_icon_change                       | false     |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | new_pin                                   | new pin                                   | 6     | convert_new_pin                                   | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | welcome                                   | welcome                                   | 7     | convert_welcome                                   | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | guild_boost                               | guild boost                               | 8     | convert_guild_boost                               | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | guild_boost_tier_1                        | guild boost tier 1                        | 9     | convert_guild_boost_tier_1                        | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | guild_boost_tier_2                        | guild boost tier 2                        | 10    | convert_guild_boost_tier_2                        | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | guild_boost_tier_3                        | guild boost tier 3                        | 11    | convert_guild_boost_tier_3                        | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | new_follower_channel                      | new follower channel                      | 12    | convert_new_follower_channel                      | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | stream                                    | stream                                    | 13    | convert_stream                                    | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | discovery_disqualified                    | discovery disqualified                    | 14    | convert_discovery_disqualified                    | false     |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | discovery_requalified                     | discovery requalified                     | 15    | convert_discovery_requalified                     | false     |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | discovery_grace_period_initial_warning    | discovery grace period initial warning    | 16    | convert_discovery_grace_period_initial_warning    | false     |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | discovery_grace_period_final_warning      | discovery grace period final warning      | 17    | convert_discovery_grace_period_final_warning      | false     |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | thread_created                            | thread created                            | 18    | convert_thread_created                            | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | inline_reply                              | inline reply                              | 19    | MESSAGE_DEFAULT_CONVERTER                         | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | slash_command                             | slash command                             | 20    | MESSAGE_DEFAULT_CONVERTER                         | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | thread_started                            | thread started                            | 21    | MESSAGE_DEFAULT_CONVERTER                         | false     |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | invite_reminder                           | invite reminder                           | 22    | convert_invite_reminder                           | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | context_command                           | context command                           | 23    | MESSAGE_DEFAULT_CONVERTER                         | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | auto_moderation_action                    | auto moderation_action                    | 24    | MESSAGE_DEFAULT_CONVERTER                         | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | role_subscription_purchase                | role subscription purchase                | 25    | MESSAGE_DEFAULT_CONVERTER                         | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | interaction_premium_upsell                | interaction premium upsell                | 26    | MESSAGE_DEFAULT_CONVERTER                         | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ('converter', 'deletable',)
    
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
        self.converter = MESSAGE_DEFAULT_CONVERTER
        self.deletable = True
        
        return self
    
    
    def __init__(self, value, name, converter, deletable):
        """
        Creates an ``MessageType`` and stores it at the class's `.INSTANCES` class attribute as well.
        
        Parameters
        ----------
        value : `int`
            The Discord side identifier value of the message type.
        name : `str`
            The default name of the message type.
        converter : `FunctionType`
            The converter function of the message type.
        deletable : `bool`
            Whether the message with this type can be deleted.
        """
        self.value = value
        self.name = name
        self.converter = converter
        self.deletable = deletable
        
        self.INSTANCES[value] = self
    
    
    def __repr__(self):
        """Returns the representation of the message type."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' name=')
        repr_parts.append(repr(self.name))
        
        repr_parts.append(', value=')
        repr_parts.append(repr(self.value))
        
        repr_parts.append(' converter=')
        repr_parts.append(repr(self.converter))
        
        repr_parts.append(', deletable=')
        repr_parts.append(repr(self.deletable))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    # predefined
    default = P(0, 'default', MESSAGE_DEFAULT_CONVERTER, True)
    add_user = P(1, 'add user', convert_add_user, False)
    remove_user = P(2, 'remove user', convert_remove_user, False)
    call = P(3, 'call', convert_call, False)
    channel_name_change = P(4, 'channel name change', convert_channel_name_change, False)
    channel_icon_change = P(5, 'channel icon change', convert_channel_icon_change, False)
    new_pin = P(6, 'new pin', convert_new_pin, True)
    welcome = P(7, 'welcome', convert_welcome, True)
    guild_boost = P(8, 'guild boost', convert_guild_boost, True)
    guild_boost_tier_1 = P(9, 'guild boost tier 1', convert_guild_boost_tier_1, True)
    guild_boost_tier_2 = P(10, 'guild boost tier 2', convert_guild_boost_tier_2, True)
    guild_boost_tier_3 = P(11, 'guild boost tier 3', convert_guild_boost_tier_3, True)
    new_follower_channel = P(12, 'new follower channel', convert_new_follower_channel, True)
    stream = P(13, 'stream', convert_stream, False)
    discovery_disqualified = P(14, 'discovery disqualified', convert_discovery_disqualified, False)
    discovery_requalified = P(15, 'discovery requalified', convert_discovery_requalified, False)
    discovery_grace_period_initial_warning = P(
        16, 'discovery grace period initial warning', convert_discovery_grace_period_initial_warning, False
    )
    discovery_grace_period_final_warning = P(
        17, 'discovery grace period final warning', convert_discovery_grace_period_final_warning, False
    )
    thread_created = P(18, 'thread created', convert_thread_created, True)
    inline_reply = P(19, 'inline reply', MESSAGE_DEFAULT_CONVERTER, True)
    slash_command = P(20, 'slash command', MESSAGE_DEFAULT_CONVERTER, True)
    thread_started = P(21, 'thread started', MESSAGE_DEFAULT_CONVERTER, False)
    invite_reminder = P(22, 'invite reminder', convert_invite_reminder, True)
    context_command = P(23, 'context command', MESSAGE_DEFAULT_CONVERTER, True)
    auto_moderation_action = P(24, 'auto moderation action', MESSAGE_DEFAULT_CONVERTER, True)
    role_subscription_purchase = P (25, 'role subscription purchase', MESSAGE_DEFAULT_CONVERTER, True)
    interaction_premium_upsell = P(26, 'interaction premium upsell', MESSAGE_DEFAULT_CONVERTER, True)
    
        
    @class_property
    def new_guild_sub(cls):
        warnings.warn(
            (
                f'`{cls.__name__}.new_guild_sub` is deprecated and will be removed in 2022 Nov.'
                f'Please use `.new_guild_subscription` instead.'
            ),
            FutureWarning,
            stacklevel = 3,
        )

    @class_property
    def new_guild_sub_t1(cls):
        warnings.warn(
            (
                f'`{cls.__name__}.new_guild_sub_t1` is deprecated and will be removed in 2022 Nov.'
                f'Please use `.new_guild_subscription_tier_1` instead.'
            ),
            FutureWarning,
            stacklevel = 3,
        )

    @class_property
    def new_guild_sub_t2(cls):
        warnings.warn(
            (
                f'`{cls.__name__}.new_guild_sub_t2` is deprecated and will be removed in 2022 Nov.'
                f'Please use `.new_guild_subscription_tier_2` instead.'
            ),
            FutureWarning,
            stacklevel = 3,
        )
    
    @class_property
    def new_guild_sub_t3(cls):
        warnings.warn(
            (
                f'`{cls.__name__}.new_guild_sub_t3` is deprecated and will be removed in 2022 Nov.'
                f'Please use `.new_guild_subscription_tier_3` instead.'
            ),
            FutureWarning,
            stacklevel = 3,
        )
    
    @property
    def convert(self):
        warnings.warn(
            (
                f'`{self.___class__.__name__}.convert` is deprecated and will be removed in 2022 Nov.'
                f'Please use `.converter` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        return self.converter

    @class_property
    def new_guild_subscription(cls):
        warnings.warn(
            (
                f'`{cls.__name__}.new_guild_subscription` is deprecated and will be removed in 2022 Dec.'
                f'Please use `.guild_boost` instead.'
            ),
            FutureWarning,
            stacklevel = 3,
        )

    @class_property
    def new_guild_subscription_tier_1(cls):
        warnings.warn(
            (
                f'`{cls.__name__}.new_guild_subscription_tier_1` is deprecated and will be removed in 2022 Dec.'
                f'Please use `.guild_boost_tier_1` instead.'
            ),
            FutureWarning,
            stacklevel = 3,
        )

    @class_property
    def new_guild_subscription_tier_2(cls):
        warnings.warn(
            (
                f'`{cls.__name__}.new_guild_subscription_tier_2` is deprecated and will be removed in 2022 Dec.'
                f'Please use `.guild_boost_tier_2` instead.'
            ),
            FutureWarning,
            stacklevel = 3,
        )
    
    @class_property
    def new_guild_subscription_tier_3(cls):
        warnings.warn(
            (
                f'`{cls.__name__}.new_guild_subscription_tier_3` is deprecated and will be removed in 2022 Dec.'
                f'Please use `.guild_boost_tier_3` instead.'
            ),
            FutureWarning,
            stacklevel = 3,
        )


del convert_add_user
del convert_remove_user
del convert_call
del convert_channel_name_change
del convert_channel_icon_change
del convert_new_pin
del convert_welcome
del convert_guild_boost
del convert_guild_boost_tier_1
del convert_guild_boost_tier_2
del convert_guild_boost_tier_3
del convert_new_follower_channel
del convert_stream
del convert_discovery_disqualified
del convert_discovery_requalified
del convert_discovery_grace_period_initial_warning
del convert_discovery_grace_period_final_warning
del convert_thread_created
del convert_invite_reminder

GENERIC_MESSAGE_TYPES = frozenset((
    MessageType.default,
    MessageType.inline_reply,
    MessageType.slash_command,
    MessageType.thread_started,
    MessageType.context_command,
))
