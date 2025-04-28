__all__ = ('MessageType', )

from scarletio import copy_docs, include

from ...activity import ActivityType
from ...bases import Preinstance as P, PreinstancedBase
from ...embed import EmbedType
from ...emoji.emoji.utils import _create_partial_emoji_from_fields
from ...utils import DATETIME_FORMAT_CODE, elapsed_time, sanitize_mentions, timestamp_to_datetime


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
    return f'{self.author.name_at(self.guild_id)!s} pinned a message to this channel. See all pinned messages.'


JOIN_MESSAGE_FORMATTERS = (
    (lambda name : f'{name} joined the party.'),
    (lambda name : f'{name} is here.'),
    (lambda name : f'Welcome, {name}. We hope you brought pizza.'),
    (lambda name : f'A wild {name} appeared.'),
    (lambda name : f'Swoooosh. {name} just landed.'),
    (lambda name : f'{name} just slid into the server.'),
    (lambda name : f'Big {name} showed up!'),
    (lambda name : f'Welcome {name}. Say hi!'),
    (lambda name : f'{name} hopped into the server.'),
    (lambda name : f'Everyone welcome {name}!'),
    (lambda name : f'Glad you\'re here, {name}.'),
    (lambda name : f'Good to see you, {name}.'),
    (lambda name : f'Yay you made it, {name}!'),
)

# TODO: this system changed, just pulled out the new texts from the js client source, but the calculation is bad
def convert_welcome(self):
    seed = self.id // 4194304 + 1420070400000
    formatter = JOIN_MESSAGE_FORMATTERS[seed % len(JOIN_MESSAGE_FORMATTERS)]
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
        if activity.type is ActivityType.stream:
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
    thread = self.thread
    if thread is None:
        thread_name = self.content
        if thread_name is None:
            thread_name = 'unknown'
    else:
        thread_name = thread.name
    
    return f'{self.author.name_at(self.guild_id)!s} started a thread: {thread_name!s}. See all threads.'


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
    
    if content_parts:
        return ''.join(content_parts)


def convert_role_subscription_purchase(self):
    role_subscription = self.role_subscription
    if (role_subscription is None):
        return None
    
    user_name = self.author.name_at(self.guild_id)
    tier_name = role_subscription.tier_name
    total_months = role_subscription.total_months
    renewal = role_subscription.renewal
    
    guild = self.guild
    if guild is None:
        guild_name = 'unknown'
    else:
        guild_name = guild.name
    
    case = (renewal << 1) | total_months > 0
    
    content_parts = [
        user_name,
        ' ',
        ("renewed" if renewal else "joined"),
        ' **',
        tier_name,
        '** ',
        ('and has been a subscriber of', 'in their', 'and has been a subscriber of', 'as a subscriber of')[case],
        ' ',
        guild_name,
        (' for ', ' subscription', ' for ', '')[case],
    ]
    
    if total_months > 0:
        content_parts.append(str(total_months))
        content_parts.append(' month')
        if total_months != 1:
            content_parts.append('s')
    
    content_parts.append('!')
    return ''.join(content_parts)


def convert_invite_reminder(self):
    return (
        'Wondering who to invite?\n'
        'Start by inviting anyone who can help you build the server!'
    )


def convert_stage_start(self):
    return f'{self.author.name_at(self.guild_id)!s} started {self.content!s}.'


def convert_stage_end(self):
    return f'{self.author.name_at(self.guild_id)!s} ended {self.content!s}.'


def convert_stage_topic_change(self):
    return f'{self.author.name_at(self.guild_id)!s} changed the Stage topic: {self.content!s}'


def convert_stage_speaker(self):
    return f'{self.author.name_at(self.guild_id)!s} is now a speaker'


def convert_application_guild_subscription(self):
    application = self.application
    if application is None:
        application_name = 'unknown'
    else:
        application_name = application.name
    
    return f'{self.author.name_at(self.guild_id)} upgraded {application_name!s} to premium for this server! \uD83C\uDF89'


def convert_private_channel_integration_add(self):
    application = self.application
    if application is None:
        application_name = 'unknown'
    else:
        application_name = application.name
    
    return f'{self.author.name!s} added the {application_name!s} app. See our help center for more info.'


def convert_private_channel_integration_remove(self):
    application = self.application
    if application is None:
        application_name = 'unknown'
    else:
        application_name = application.name
    
    return f'{self.author.name!s} removed the {application_name} app. See our help center for more info.'


def convert_guild_incidents_enable(self):
    content_parts = [self.author.name_at(self.guild_id), ' enabled security actions for ']
    
    guild = self.guild
    if guild is None:
        guild_name = 'unknown'
    else:
        guild_name = guild.name
    content_parts.append(guild_name)
    
    content = self.content
    if content is not None:
        content_parts.append(' until ')
        content_parts.append(format(timestamp_to_datetime(content), DATETIME_FORMAT_CODE))
    
    content_parts.append('.')
    return ''.join(content_parts)


def convert_guild_incidents_disable(self):
    guild = self.guild
    if guild is None:
        guild_name = 'unknown'
    else:
        guild_name = guild.name
        
    return f'{self.author.name_at(self.guild_id)!s} disabled security actions for {guild_name!s}.'


def convert_purchase_notification(self):
    return f'Thank you,\n {self.author.name_at(self.guild_id)!s}'


def convert_poll_result(self):
    embed = self.embed
    if embed is None or embed.type is not EmbedType.poll_result:
        return None
    
    content_parts = []
    should_add_next = ''
    
    description = embed.description
    if description is not None:
        content_parts.append(description)
        should_add_next = '\n'
    
    
    for field in embed.iter_fields():
        if field.name == 'poll_question_text':
            content_parts.append(should_add_next)
            content_parts.append('The poll ')
            content_parts.append(field.value)
            content_parts.append(' has closed.')
            should_add_next = '\n'
            break
    
    for field in embed.iter_fields():
        if field.name == 'victor_answer_text':
            answer_text = field.value
            break
    else:
        answer_text = None
    
    for field in embed.iter_fields():
        if field.name == 'victor_answer_emoji_id':
            answer_emoji_id = field.value
            break
    else:
        answer_emoji_id = None
    
    for field in embed.iter_fields():
        if field.name == 'victor_answer_emoji_name':
            answer_emoji_name = field.value
            break
    else:
        answer_emoji_name = ''
    
    for field in embed.iter_fields():
        if field.name == 'victor_answer_emoji_animated':
            answer_emoji_animated = field.value == 'true'
            break
    else:
        answer_emoji_animated = False
    
    if answer_emoji_id or answer_emoji_name:
        emoji = _create_partial_emoji_from_fields(answer_emoji_name, answer_emoji_id, answer_emoji_animated)
    else:
        emoji = None
    
    text_flag = ((answer_text is not None) << 1) | (emoji is not None)
    if text_flag:
        content_parts.append(should_add_next)
        should_add_next = '\n'
        
        if text_flag & 0b01:
            content_parts.append(emoji.as_emoji)
        
        if text_flag == 0b11:
            content_parts.append(' ')
        
        if text_flag & 0b10:
            content_parts.append(answer_text)
    
    
    for field in embed.iter_fields():
        if field.name == 'victor_answer_votes':
            try:
                winning_answer_votes = int(field.value)
            except ValueError:
                winning_answer_votes = -1
            break
    else:
        winning_answer_votes = -1
    
    total_votes = -1
    
    for field in embed.iter_fields():
        if field.name == 'total_votes':
            try:
                total_votes = int(field.value)
            except ValueError:
                pass
            break
    
    if (winning_answer_votes != -1) and (total_votes != -1):
        content_parts.append(should_add_next)
        
        if (winning_answer_votes == 0) and (total_votes == 0):
            content_parts.append('There was no winner')
        
        else:
            content_parts.append('Winning answer • ')
            content_parts.append(format(winning_answer_votes * 100 / total_votes, '.0f'))
            content_parts.append('%')
    
    
    if content_parts:
        return ''.join(content_parts)


class MessageType(PreinstancedBase, value_type = int):
    """
    Represents a ``Message``'s type.
    
    Attributes
    ----------
    converter : `FunctionType`
        The converter function of the message type, what tries to convert the message's content to it's Discord side
        representation.
    
    deletable : `bool`
        Whether the message with this type can be deleted.
    
    name : `str`
        The default name of the message type.
    
    value : `int`
        The Discord side identifier value of the message type.
    
    Type Attributes
    ---------------
    Every predefined message type can be accessed as type attribute as well:
    
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | Type attribute name                       | Name                                      | Value | Converter                                         | Deletable |
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
    | role_subscription_purchase                | role subscription purchase                | 25    | convert_role_subscription_purchase                | true      |
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
    | application_guild_subscription            | application guild subscription            | 32    | convert_application_guild_subscription            | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | private_channel_integration_add           | private channel integration add           | 33    | convert_private_channel_integration_add           | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | private_channel_integration_remove        | private channel integration remove        | 34    | convert_private_channel_integration_remove        | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | premium_referral                          | premium referral                          | 35    | MESSAGE_DEFAULT_CONVERTER                         | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | guild_incidents_enable                    | guild incidents enable                    | 36    | convert_guild_incidents_enable                    | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | guild_incidents_disable                   | guild incidents disable                   | 37    | convert_guild_incidents_disable                   | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | guild_incidents_report_raid               | guild incidents report raid               | 38    | MESSAGE_DEFAULT_CONVERTER                         | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | guild_incidents_report_false_alarm        | guild incidents report false alarm        | 39    | MESSAGE_DEFAULT_CONVERTER                         | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | guild_channel_revive                      | guild channel revive                      | 40    | MESSAGE_DEFAULT_CONVERTER                         | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | custom_gift                               | custom gift                               | 41    | MESSAGE_DEFAULT_CONVERTER                         | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | guild_gaming_stats                        | guild gaming stats                        | 42    | MESSAGE_DEFAULT_CONVERTER                         | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | poll                                      | poll                                      | 43    | MESSAGE_DEFAULT_CONVERTER                         | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | purchase_notification                     | purchase notification                     | 44    | MESSAGE_DEFAULT_CONVERTER                         | false     |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | voice_hangout_invite                      | voice hangout invite                      | 45    | MESSAGE_DEFAULT_CONVERTER                         | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | poll_result                               | poll result                               | 46    | convert_poll_result                               | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | changelog                                 | changelog                                 | 47    | MESSAGE_DEFAULT_CONVERTER                         | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | nitro_notification                        | nitro notification                        | 48    | MESSAGE_DEFAULT_CONVERTER                         | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | channel_linked_to_lobby                   | channel linked to lobby                   | 49    | MESSAGE_DEFAULT_CONVERTER                         | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | gifting_prompt                            | gifting prompt                            | 50    | MESSAGE_DEFAULT_CONVERTER                         | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | in_activity_message                       | in activity message                       | 51    | MESSAGE_DEFAULT_CONVERTER                         | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | guild_join_request_accept                 | guild join request accept                 | 52    | MESSAGE_DEFAULT_CONVERTER                         | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | guild_join_request_reject                 | guild join request reject                 | 53    | MESSAGE_DEFAULT_CONVERTER                         | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | guild_join_request_withdraw               | guild join request withdraw               | 54    | MESSAGE_DEFAULT_CONVERTER                         | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | streaming_quality_upgraded                | streaming quality upgraded                | 55    | MESSAGE_DEFAULT_CONVERTER                         | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | channel_wallpaper_set                     | channel wallpaper set                     | 56    | MESSAGE_DEFAULT_CONVERTER                         | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    | channel_wallpaper_removed                  | channel wallpaper removed                | 57    | MESSAGE_DEFAULT_CONVERTER                         | true      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------------------+-----------+
    """
    __slots__ = ('converter', 'deletable',)
    
    def __new__(cls, value, name = None, converter = None, deletable = True):
        """
        Creates a new message type.
        
        Parameters
        ----------
        value : `int`
            The Discord side identifier value of the message type.
        
        name : `None | str` = `None`, Optional
            The default name of the message type.
        
        converter : `None | FunctionType` = `None`, Optional
            The converter function of the message type.
        
        deletable : `bool` = `True`, Optional
            Whether the message with this type can be deleted.
        """
        if converter is None:
            converter = MESSAGE_DEFAULT_CONVERTER
        
        self = PreinstancedBase.__new__(cls, value, name)
        self.converter = converter
        self.deletable = deletable
        return self
    
    
    @copy_docs(PreinstancedBase._put_repr_parts_into)
    def _put_repr_parts_into(self, repr_parts):
        # converter
        repr_parts.append(', converter = ')
        repr_parts.append(repr(self.converter))
        
        # deletable
        repr_parts.append(', deletable = ')
        repr_parts.append(repr(self.deletable))
    
    
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
    role_subscription_purchase = P (25, 'role subscription purchase', convert_role_subscription_purchase, True)
    interaction_premium_upsell = P(26, 'interaction premium upsell', MESSAGE_DEFAULT_CONVERTER, True)
    stage_start = P(27, 'stage start', convert_stage_start, True)
    stage_end = P(28, 'stage end', convert_stage_end, True)
    stage_speaker = P(29, 'stage speaker', convert_stage_speaker, True)
    stage_request_to_speak = P(30, 'stage request to speak', MESSAGE_DEFAULT_CONVERTER, True)
    stage_topic_change = P(31, 'stage topic change', convert_stage_topic_change, True)
    application_guild_subscription = P(
        32, 'application guild subscription', convert_application_guild_subscription, True
    )
    private_channel_integration_add = P(
        33, 'private channel integration add', convert_private_channel_integration_add, True
    )
    private_channel_integration_remove = P(
        34, 'private channel integration remove', convert_private_channel_integration_remove, True
    )
    premium_referral = P(35, 'premium referral', MESSAGE_DEFAULT_CONVERTER, True)
    guild_incidents_enable = P(36, 'guild incidents enable', convert_guild_incidents_enable, False)
    guild_incidents_disable = P(37, 'guild incidents disable', convert_guild_incidents_disable, False)
    guild_incidents_report_raid = P(38, 'guild incidents report raid', MESSAGE_DEFAULT_CONVERTER, False)
    guild_incidents_report_false_alarm = P(39, 'guild incidents report false alarm', MESSAGE_DEFAULT_CONVERTER, False)
    guild_channel_revive = P(40, 'guild channel revive', MESSAGE_DEFAULT_CONVERTER, True)
    custom_gift = P(41, 'custom gif', MESSAGE_DEFAULT_CONVERTER, True)
    guild_gaming_stats = P(42, 'guild gaming stats', MESSAGE_DEFAULT_CONVERTER, True)
    poll = P(43, 'poll', MESSAGE_DEFAULT_CONVERTER, True)
    purchase_notification = P(44, 'purchase notification', convert_purchase_notification, False)
    voice_hangout_invite = P(45, 'voice hangout invite', MESSAGE_DEFAULT_CONVERTER, True)
    poll_result = P(46, 'poll result', convert_poll_result, True)
    changelog = P(47, 'changelog', MESSAGE_DEFAULT_CONVERTER, True)
    nitro_notification = P(48, 'nitro notification', MESSAGE_DEFAULT_CONVERTER, True)
    channel_linked_to_lobby = P(49, 'channel linked to lobby', MESSAGE_DEFAULT_CONVERTER, True)
    gifting_prompt = P(50, 'gifting prompt', MESSAGE_DEFAULT_CONVERTER, True)
    in_activity_message = P(51, 'in activity message', MESSAGE_DEFAULT_CONVERTER, True)
    guild_join_request_accept = P(52, 'guild join request accept', MESSAGE_DEFAULT_CONVERTER, True)
    guild_join_request_reject = P(53, 'guild join request reject', MESSAGE_DEFAULT_CONVERTER, True)
    guild_join_request_withdraw = P(54, 'guild join request withdraw', MESSAGE_DEFAULT_CONVERTER, True)
    streaming_quality_upgraded = P(55, 'streaming quality upgraded', MESSAGE_DEFAULT_CONVERTER, True)
    channel_wallpaper_set = P(56, 'channel wallpaper set', MESSAGE_DEFAULT_CONVERTER, True)
    channel_wallpaper_removed = P(57, 'channel wallpaper removed', MESSAGE_DEFAULT_CONVERTER, True)


GENERIC_MESSAGE_TYPES = frozenset((
    MessageType.default,
    MessageType.inline_reply,
    MessageType.slash_command,
    MessageType.thread_started,
    MessageType.context_command,
    MessageType.changelog,
    MessageType.in_activity_message,
))
