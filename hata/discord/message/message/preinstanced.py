__all__ = ('MessageType', )

import warnings

from scarletio import class_property, include

from ...activity import ACTIVITY_TYPES
from ...bases import Preinstance as P, PreinstancedBase
from ...embed import EmbedType
from ...utils import elapsed_time, sanitize_mentions


Client = include('Client')


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


def convert_user_add(self):
    return f'{self.author.name} added {self.mentioned_users[0].name} to the group.'

def convert_user_remove(self):
    return f'{self.author.name} removed {self.mentioned_users[0].name} from the group.'


def convert_call(self):
    call = self.call
    if call is None or not any(isinstance(user, Client) for user in call.iter_users()):
        return f'{self.author.name} started a call.'
    
    ended_at = call.ended_at
    if ended_at is None:
        # We are using a unicode as dash and not the minus sign
        return f'{self.author.name} started a call — Join the call.'
    
    # This formatting could be more accurate.
    if elapsed_time is None:
        return f'{self.author.name} started a call.'
    
    return f'{self.author.name} started a call that lasted {elapsed_time(self.created_at, ended_at)}.'


def convert_channel_name_change(self):
    return f'{self.author.name} changed the channel name: {self.content!s}'

def convert_channel_icon_change(self):
    return f'{self.author.name} changed the channel icon.'

def convert_new_pin(self):
    return f'{self.author.name_at(self.guild_id)} pinned a message to this channel. See all pinned messages.'


JOIN_MESSAGE_FORMATTERS = (
    lambda name : f'{name} just joined the server - glhf!',
    lambda name : f'{name} just joined. Everyone, look busy!',
    lambda name : f'{name} just joined. Can I get a heal?',
    lambda name : f'{name} joined your party.',
    lambda name : f'{name} joined. You must construct additional pylons.',
    lambda name : f'Ermagherd. {name} is here.',
    lambda name : f'Welcome, {name}. Stay awhile and listen.',
    lambda name : f'Welcome, {name}. We were expecting you ( ͡° ͜ʖ ͡°)',
    lambda name : f'Welcome, {name}. We hope you brought pizza.',
    lambda name : f'Welcome {name}. Leave your weapons by the door.',
    lambda name : f'A wild {name} appeared.',
    lambda name : f'Swoooosh. {name} just landed.',
    lambda name : f'Brace yourselves. {name} just joined the server.',
    lambda name : f'{name} just joined... or did they?',
    lambda name : f'{name} just arrived. Seems OP - please nerf.',
    lambda name : f'{name} just slid into the server.',
    lambda name : f'A {name} has spawned in the server.',
    lambda name : f'Big {name} showed up!',
    lambda name : f'Where’s {name}? In the server!',
    lambda name : f'{name} hopped into the server. Kangaroo!!',
    lambda name : f'{name} just showed up. Hold my beer.',
    lambda name : f'Challenger approaching - {name} has appeared!',
    lambda name : f'It\'s a bird! It\'s a plane! Nevermind, it\'s just {name}.',
    lambda name : f'It\'s {name}! Praise the sun! [T]/',
    lambda name : f'Never gonna give {name} up. Never gonna let {name} down.',
    lambda name : f'{name} has joined the battle bus.',
    lambda name : f'Cheers, love! {name}\'s here!',
    lambda name : f'Hey! Listen! {name} has joined!',
    lambda name : f'We\'ve been expecting you {name}',
    lambda name : f'It\'s dangerous to go alone, take {name}!',
    lambda name : f'{name} has joined the server! It\'s super effective!',
    lambda name : f'Cheers, love! {name} is here!',
    lambda name : f'{name} is here, as the prophecy foretold.',
    lambda name : f'{name} has arrived. Party\'s over.',
    lambda name : f'Ready player {name}',
    lambda name : f'{name} is here to kick butt and chew bubblegum. And {name} is all out of gum.',
    lambda name : f'Hello. Is it {name} you\'re looking for?',
    lambda name : f'{name} has joined. Stay a while and listen!',
    lambda name : f'Roses are red, violets are blue, {name} joined this server with you',
)

# TODO: this system changed, just pulled out the new texts from the js client source, but the calculation is bad
def convert_welcome(self):
    formatter = JOIN_MESSAGE_FORMATTERS[int(self.created_at.timestamp()) % len(JOIN_MESSAGE_FORMATTERS)]
    user_name = self.author.name_at(self.guild_id)
    return formatter(user_name)


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
    
    user_name = user.name_at(self.guild_id)
    
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
    return f'{self.author.name_at(self.guild_id)} started a thread: {self.content!r}. See all threads.'


def convert_auto_moderation_action(self):
    embed = self.embed
    if embed is None or embed.type is not EmbedType.auto_moderation_message:
        return None
    
    content_parts = []
    should_add_next = ''
    
    description = embed.description
    if description is not None:
        content_parts.append(description)
        should_add_next = '\n'
    
    
    for field in embed.iter_fields():
        if field.name == 'keyword':
            content_parts.append(should_add_next)
            content_parts.append('Keyword: ')
            content_parts.append(field.value)
            should_add_next = ' • '
            break
    
    for field in embed.iter_fields():
        if field.name == 'rule_name':
            content_parts.append(should_add_next)
            content_parts.append('Rule: ')
            content_parts.append(field.value)
            should_add_next = ' • '
            break
    
    for field in embed.iter_fields():
        if field.name == 'timeout_duration':
            content_parts.append(should_add_next)
            content_parts.append('Time-out: ')
            content_parts.append(field.value)
            content_parts.append(' secs')
            break
    
    return ''.join(content_parts)


def convert_invite_reminder(self):
    return (
        'Wondering who to invite?\n'
        'Start by inviting anyone who can help you build the server!'
    )


def convert_stage_start(self):
    return f'{self.author.name_at(self.guild_id)} started {self.content!s}.'


def convert_stage_end(self):
    return f'{self.author.name_at(self.guild_id)} ended {self.content!s}.'


def convert_stage_topic_change(self):
    return f'{self.author.name_at(self.guild_id)} changed the Stage topic: {self.content!r}'


def convert_stage_speaker(self):
    return f'{self.author.name_at(self.guild_id)} is now a speaker'


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
    | user_add                                  | user add                                  | 1     | convert_user_add                                  | false     |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | user_remove                               | user remove                               | 2     | convert_user_remove                               | false     |
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
    | auto_moderation_action                    | auto moderation action                    | 24    | convert_auto_moderation_action                    | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | role_subscription_purchase                | role subscription purchase                | 25    | MESSAGE_DEFAULT_CONVERTER                         | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | interaction_premium_upsell                | interaction premium upsell                | 26    | MESSAGE_DEFAULT_CONVERTER                         | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | stage_start                               | stage start                               | 27    | convert_stage_start                               | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | stage_end                                 | stage end                                 | 28    | convert_stage_end                                 | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | stage_speaker                             | stage speaker                             | 29    | convert_stage_speaker                             | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | stage_request_to_speak                    | stage request to speak                    | 30    | MESSAGE_DEFAULT_CONVERTER                         | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | stage_topic_change                        | stage topic change                        | 31    | convert_stage_topic_change                        | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | application_subscription                  | application subscription                  | 32    | MESSAGE_DEFAULT_CONVERTER                         | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | private_channel_integration_add           | private channel integration add           | 33    | MESSAGE_DEFAULT_CONVERTER                         | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | private_channel_integration_remove        | private channel integration remove        | 34    | MESSAGE_DEFAULT_CONVERTER                         | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | premium_referral                          | premium referral                          | 35    | MESSAGE_DEFAULT_CONVERTER                         | true      |
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
        
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.name))
        
        repr_parts.append(', value = ')
        repr_parts.append(repr(self.value))
        
        repr_parts.append(' converter = ')
        repr_parts.append(repr(self.converter))
        
        repr_parts.append(', deletable = ')
        repr_parts.append(repr(self.deletable))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    # predefined
    default = P(0, 'default', MESSAGE_DEFAULT_CONVERTER, True)
    user_add = P(1, 'add user', convert_user_add, False)
    user_remove = P(2, 'remove user', convert_user_remove, False)
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
    auto_moderation_action = P(24, 'auto moderation action', convert_auto_moderation_action, True)
    role_subscription_purchase = P (25, 'role subscription purchase', MESSAGE_DEFAULT_CONVERTER, True)
    interaction_premium_upsell = P(26, 'interaction premium upsell', MESSAGE_DEFAULT_CONVERTER, True)
    stage_start = P(27, 'stage start', convert_stage_start, True)
    stage_end = P(28, 'stage end', convert_stage_end, True)
    stage_speaker = P(29, 'stage speaker', convert_stage_speaker, True)
    stage_request_to_speak = P(30, 'stage request to speak', MESSAGE_DEFAULT_CONVERTER, True)
    stage_topic_change = P(31, 'stage topic change', convert_stage_topic_change, True)
    application_subscription = P(32, 'application subscription', MESSAGE_DEFAULT_CONVERTER, True)
    private_channel_integration_add = P(33, 'private channel integration add', MESSAGE_DEFAULT_CONVERTER, True)
    private_channel_integration_remove = P(34, 'private channel integration remove', MESSAGE_DEFAULT_CONVERTER, True)
    premium_referral = P(34, 'premium referral', MESSAGE_DEFAULT_CONVERTER, True)


    @class_property
    def add_user(cls):
        """
        Deprecated and will be removed in 2023 November. Please use `.user_add` instead.
        """
        warnings.warn(
            (
                f'`{cls.__name__}.add_user` is deprecated and will be removed in 2023 November. '
                f'Please use `.user_add` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        return cls.user_add


    @class_property
    def remove_user(cls):
        """
        Deprecated and will be removed in 2023 November. Please use `.user_remove` instead.
        """
        warnings.warn(
            (
                f'`{cls.__name__}.remove_user` is deprecated and will be removed in 2023 November. '
                f'Please use `.user_remove` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        return cls.user_remove


del convert_user_add
del convert_user_remove
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
del convert_stage_start
del convert_stage_end
del convert_stage_topic_change
del convert_stage_speaker
del convert_auto_moderation_action

GENERIC_MESSAGE_TYPES = frozenset((
    MessageType.default,
    MessageType.inline_reply,
    MessageType.slash_command,
    MessageType.thread_started,
    MessageType.context_command,
))
