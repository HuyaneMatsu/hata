__all__ = ('AuditLogEntryType', 'AuditLogEntryTargetType')

from warnings import warn

from scarletio import class_property, copy_docs, export

from ...bases import Preinstance as P, PreinstancedBase

from ..audit_log_entry_change_conversions.application_command import (
    APPLICATION_COMMAND_CONVERSIONS as CHANGE_APPLICATION_COMMAND_CONVERSIONS
)
from ..audit_log_entry_change_conversions.auto_moderation_rule import (
    AUTO_MODERATION_RULE_CONVERSIONS as CHANGE_AUTO_MODERATION_RULE_CONVERSIONS
)
from ..audit_log_entry_change_conversions.channel import CHANNEL_CONVERSIONS as CHANGE_CHANNEL_CONVERSIONS
from ..audit_log_entry_change_conversions.channel_permission_overwrite import (
    CHANNEL_PERMISSION_OVERWRITE_CONVERSIONS as CHANGE_CHANNEL_PERMISSION_OVERWRITE_CONVERSIONS
)
from ..audit_log_entry_change_conversions.emoji import EMOJI_CONVERSIONS as CHANGE_EMOJI_CONVERSIONS
from ..audit_log_entry_change_conversions.guild import GUILD_CONVERSIONS as CHANGE_GUILD_CONVERSIONS
from ..audit_log_entry_change_conversions.integration import INTEGRATION_CONVERSIONS as CHANGE_INTEGRATION_CONVERSIONS
from ..audit_log_entry_change_conversions.invite import INVITE_CONVERSIONS as CHANGE_INVITE_CONVERSIONS
from ..audit_log_entry_change_conversions.onboarding_prompt import (
    ONBOARDING_PROMPT_CONVERSIONS as CHANGE_ONBOARDING_PROMPT_CONVERSIONS
)
from ..audit_log_entry_change_conversions.onboarding_screen import (
    ONBOARDING_SCREEN_CONVERSIONS as CHANGE_ONBOARDING_SCREEN_CONVERSIONS
)
from ..audit_log_entry_change_conversions.role import ROLE_CONVERSIONS as CHANGE_ROLE_CONVERSIONS
from ..audit_log_entry_change_conversions.scheduled_event import (
    SCHEDULED_EVENT_CONVERSIONS as CHANGE_SCHEDULED_EVENT_CONVERSIONS
)
from ..audit_log_entry_change_conversions.scheduled_event_occasion_overwrite import (
    SCHEDULED_EVENT_OCCASION_OVERWRITE_CONVERSIONS as CHANGE_SCHEDULED_EVENT_OCCASION_OVERWRITE_CONVERSIONS
)
from ..audit_log_entry_change_conversions.soundboard_sound import (
    SOUNDBOARD_SOUND_CONVERSIONS as CHANGE_SOUNDBOARD_SOUND_CONVERSIONS
)
from ..audit_log_entry_change_conversions.stage import STAGE_CONVERSIONS as CHANGE_STAGE_CONVERSIONS
from ..audit_log_entry_change_conversions.sticker import STICKER_CONVERSIONS as CHANGE_STICKER_CONVERSIONS
from ..audit_log_entry_change_conversions.user import USER_CONVERSIONS as CHANGE_USER_CONVERSIONS
from ..audit_log_entry_change_conversions.webhook import WEBHOOK_CONVERSIONS as CHANGE_WEBHOOK_CONVERSIONS
from ..audit_log_entry_detail_conversions.application_command import (
    APPLICATION_COMMAND_CONVERSIONS as DETAIL_APPLICATION_COMMAND_CONVERSIONS
)
from ..audit_log_entry_detail_conversions.auto_moderation_action_execution import (
    AUTO_MODERATION_ACTION_EXECUTION_CONVERSIONS as DETAIL_AUTO_MODERATION_ACTION_EXECUTION_CONVERSIONS
)
from ..audit_log_entry_detail_conversions.channel import CHANNEL_CONVERSIONS as DETAIL_CHANNEL_CONVERSIONS
from ..audit_log_entry_detail_conversions.channel_permission_overwrite import (
    CHANNEL_PERMISSION_OVERWRITE_CONVERSIONS as DETAIL_CHANNEL_PERMISSION_OVERWRITE_CONVERSIONS
)
from ..audit_log_entry_detail_conversions.guild import GUILD_CONVERSIONS as DETAIL_GUILD_CONVERSIONS
from ..audit_log_entry_detail_conversions.message import MESSAGE_CONVERSIONS as DETAIL_MESSAGE_CONVERSIONS
from ..audit_log_entry_detail_conversions.scheduled_event_occasion_overwrite import (
    SCHEDULED_EVENT_OCCASION_OVERWRITE_CONVERSIONS as DETAIL_SCHEDULED_EVENT_OCCASION_OVERWRITE_CONVERSIONS
)
from ..audit_log_entry_detail_conversions.stage import STAGE_CONVERSIONS as DETAIL_STAGE_CONVERSIONS
from ..audit_log_entry_detail_conversions.user import USER_CONVERSIONS as DETAIL_USER_CONVERSIONS

from .target_converters import (
    target_converter_application_command, target_converter_auto_moderation_rule, target_converter_channel,
    target_converter_emoji, target_converter_guild, target_converter_integration, target_converter_invite,
    target_converter_role, target_converter_scheduled_event, target_converter_soundboard_sound, target_converter_stage,
    target_converter_sticker, target_converter_user, target_converter_webhook
)


class AuditLogEntryTargetType(PreinstancedBase, value_type = int):
    """
    Represents the target type of an ``AuditLogEntry``.
    
    Attributes
    ----------
    change_conversions : `None | AuditLogEntryDetailConversionGroup`
        Change conversions.
    
    detail_conversions : `None | AuditLogEntryDetailConversionGroup`
        Detail conversions.
    
    name : `str`
        The name of audit log target type.
    
    target_converter : `None | FunctionType | MethodType`
        Audit log target converter.
    
    value : `int`
        The identifier value of the audit log target type. Only used for hashing.
    
    Type Attributes
    ---------------
    Every predefined audit log target type can be accessed as type attribute as well:
    
    +---------------------------------------+---------------------------------------+-------+
    | Type attribute name                   | name                                  | value |
    +=======================================+=======================================+=======+
    | none                                  | none                                  | 0     |
    +---------------------------------------+---------------------------------------+-------+
    | guild                                 | guild                                 | 1     |
    +---------------------------------------+---------------------------------------+-------+
    | channel                               | channel                               | 2     |
    +---------------------------------------+---------------------------------------+-------+
    | channel_permission_overwrite          | channel permission overwrite          | 3     |
    +---------------------------------------+---------------------------------------+-------+
    | user                                  | user                                  | 4     |
    +---------------------------------------+---------------------------------------+-------+
    | role                                  | role                                  | 5     |
    +---------------------------------------+---------------------------------------+-------+
    | invite                                | invite                                | 6     |
    +---------------------------------------+---------------------------------------+-------+
    | webhook                               | webhook                               | 7     |
    +---------------------------------------+---------------------------------------+-------+
    | emoji                                 | emoji                                 | 8     |
    +---------------------------------------+---------------------------------------+-------+
    | integration                           | integration                           | 9     |
    +---------------------------------------+---------------------------------------+-------+
    | stage                                 | stage                                 | 10    |
    +---------------------------------------+---------------------------------------+-------+
    | scheduled_event                       | scheduled event                       | 11    |
    +---------------------------------------+---------------------------------------+-------+
    | sticker                               | sticker                               | 12    |
    +---------------------------------------+---------------------------------------+-------+
    | application_command                   | application command                   | 13    |
    +---------------------------------------+---------------------------------------+-------+
    | auto_moderation_rule                  | auto moderation rule                  | 14    |
    +---------------------------------------+---------------------------------------+-------+
    | auto_moderation_action_execution      | auto moderation action execution      | 15    |
    +---------------------------------------+---------------------------------------+-------+
    | onboarding_screen                     | onboarding screen                     | 16    |
    +---------------------------------------+---------------------------------------+-------+
    | onboarding_prompt                     | onboarding prompt                     | 17    |
    +---------------------------------------+---------------------------------------+-------+
    | message                               | message                               | 18    |
    +---------------------------------------+---------------------------------------+-------+
    | soundboard_sound                      | soundboard sound                      | 19    |
    +---------------------------------------+---------------------------------------+-------+
    | scheduled_event_occasion_overwrite    | scheduled event occasion overwrite    | 20    |
    +---------------------------------------+---------------------------------------+-------+
    """
    __slots__ = ('change_conversions', 'detail_conversions', 'target_converter')
    
    def __new__(cls, value, name = None, target_converter = None, change_conversions = None, detail_conversions = None):
        """
        Creates a new audit log target type.
        
        Parameters
        ----------
        value : `int`
            The identifier value of the audit log target type.
        
        name : `None | str` = `None`, Optional
            The name of the audit log target type.
        
        target_converter : `None | FunctionType | MethodType` = `None`, Optional
            Audit log target converter.
        
        change_conversions :  `None | AuditLogEntryChangeConversionGroup` = `None`, Optional
            Change conversions.
        
        detail_conversions : `None | AuditLogEntryDetailConversionGroup` = `None`, Optional
            Detail conversions.
        """
        self = PreinstancedBase.__new__(cls, value, name)
        self.target_converter = target_converter
        self.change_conversions = change_conversions
        self.detail_conversions = detail_conversions
        return self
    

    # predefined
    none = P(
        0,
        'none',
        None,
        None,
        None,
    )
    guild = P(
        1,
        'guild',
        target_converter_guild,
        CHANGE_GUILD_CONVERSIONS,
        DETAIL_GUILD_CONVERSIONS,
    )
    channel = P(
        2,
        'channel',
        target_converter_channel,
        CHANGE_CHANNEL_CONVERSIONS,
        DETAIL_CHANNEL_CONVERSIONS,
    )
    channel_permission_overwrite = P(
        3,
        'channel permission overwrite',
        target_converter_channel,
        CHANGE_CHANNEL_PERMISSION_OVERWRITE_CONVERSIONS,
        DETAIL_CHANNEL_PERMISSION_OVERWRITE_CONVERSIONS,
    )
    user = P(
        4,
        'user',
        target_converter_user,
        CHANGE_USER_CONVERSIONS,
        DETAIL_USER_CONVERSIONS,
    )
    role = P(
        5,
        'role',
        target_converter_role,
        CHANGE_ROLE_CONVERSIONS,
        None,
    )
    invite = P(
        6,
        'invite',
        target_converter_invite,
        CHANGE_INVITE_CONVERSIONS,
        None,
    )
    webhook = P(
        7,
        'webhook',
        target_converter_webhook,
        CHANGE_WEBHOOK_CONVERSIONS,
        None,
    )
    emoji = P(
        8,
        'emoji',
        target_converter_emoji,
        CHANGE_EMOJI_CONVERSIONS,
        None,
    )
    integration = P(
        9,
        'integration',
        target_converter_integration,
        CHANGE_INTEGRATION_CONVERSIONS,
        None,
    )
    stage = P(
        10,
        'stage',
        target_converter_stage,
        CHANGE_STAGE_CONVERSIONS,
        DETAIL_STAGE_CONVERSIONS,
    )
    scheduled_event = P(
        11,
        'scheduled event',
        target_converter_scheduled_event,
        CHANGE_SCHEDULED_EVENT_CONVERSIONS,
        None,
    )
    sticker = P(
        12,
        'sticker',
        target_converter_sticker,
        CHANGE_STICKER_CONVERSIONS,
        None,
    )
    application_command = P(
        13,
        'application command',
        target_converter_application_command,
        CHANGE_APPLICATION_COMMAND_CONVERSIONS,
        DETAIL_APPLICATION_COMMAND_CONVERSIONS,
    )
    auto_moderation_rule = P(
        14,
        'auto moderation rule',
        target_converter_auto_moderation_rule,
        CHANGE_AUTO_MODERATION_RULE_CONVERSIONS,
        None,
    )
    auto_moderation_action_execution = P(
        15,
        'auto moderation action execution',
        None,
        CHANGE_USER_CONVERSIONS,
        DETAIL_AUTO_MODERATION_ACTION_EXECUTION_CONVERSIONS,
    )
    onboarding_screen = P(
        16,
        'onboarding screen',
        None,
        CHANGE_ONBOARDING_SCREEN_CONVERSIONS,
        None,
    )
    onboarding_prompt = P(
        17,
        'onboarding prompt',
        None,
        CHANGE_ONBOARDING_PROMPT_CONVERSIONS,
        None,
    )
    message = P(
        18,
        'message',
        None,
        None,
        DETAIL_MESSAGE_CONVERSIONS,
    )
    soundboard_sound = P(
        19,
        'soundboard sound',
        target_converter_soundboard_sound,
        CHANGE_SOUNDBOARD_SOUND_CONVERSIONS,
        None,
    )
    scheduled_event_occasion_overwrite = P(
        20,
        'scheduled event occasion overwrite',
        target_converter_scheduled_event,
        CHANGE_SCHEDULED_EVENT_OCCASION_OVERWRITE_CONVERSIONS,
        DETAIL_SCHEDULED_EVENT_OCCASION_OVERWRITE_CONVERSIONS,
    )


@export
class AuditLogEntryType(PreinstancedBase, value_type = int):
    """
    Represents the event type of an ``AuditLogEntry``.
    
    Attributes
    ----------
    name : `str`
        The name of audit log event.
    
    target_type : ``AuditLogEntryTargetType``
        The audit log's target's type.
    
    value : `int`
        The Discord side identifier value of the audit log event.
    
    Type Attributes
    ---------------
    Every predefined audit log event can be accessed as type attribute as well:
    
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | Type attribute name                       | Name                                      | Value | Target type                           |
    +===========================================+===========================================+=======+=======================================+
    | none                                      | none                                      |  0    | none                                  |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | guild_update                              | guild update                              |  1    | guild                                 |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | channel_create                            | channel create                            | 10    | channel                               |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | channel_update                            | channel update                            | 11    | channel                               |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | channel_delete                            | channel delete                            | 12    | channel                               |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | channel_permission_overwrite_create       | channel permission overwrite create       | 13    | channel_permission_overwrite          |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | channel_permission_overwrite_update       | channel permission overwrite update       | 14    | channel_permission_overwrite          |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | channel_permission_overwrite_delete       | channel permission overwrite delete       | 15    | channel_permission_overwrite          |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | user_kick                                 | user kick                                 | 20    | user                                  |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | user_prune                                | user prune                                | 21    | guild                                 |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | user_ban_add                              | user ban add                              | 22    | user                                  |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | user_ban_remove                           | user ban remove                           | 23    | user                                  |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | user_update                               | user update                               | 24    | user                                  |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | user_role_update                          | user role update                          | 25    | user                                  |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | user_move                                 | user move                                 | 26    | user                                  |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | user_disconnect                           | user disconnect                           | 27    | user                                  |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | bot_add                                   | bot add                                   | 28    | user                                  |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | role_create                               | role create                               | 30    | role                                  |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | role_update                               | role update                               | 31    | role                                  |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | role_delete                               | role delete                               | 32    | role                                  |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | invite_create                             | invite create                             | 40    | invite                                |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | invite_update                             | invite update                             | 41    | invite                                |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | invite_delete                             | invite delete                             | 42    | invite                                |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | webhook_create                            | webhook create                            | 50    | webhook                               |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | webhook_update                            | webhook update                            | 51    | webhook                               |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | webhook_delete                            | webhook delete                            | 52    | webhook                               |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | emoji_create                              | emoji create                              | 60    | emoji                                 |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | emoji_update                              | emoji update                              | 61    | emoji                                 |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | emoji_delete                              | emoji delete                              | 62    | emoji                                 |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | message_delete                            | message delete                            | 72    | message                               |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | message_bulk_delete                       | message bulk delete                       | 73    | message                               |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | message_pin                               | message pin                               | 74    | message                               |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | message_unpin                             | message unpin                             | 75    | message                               |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | integration_create                        | integration create                        | 80    | integration                           |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | integration_update                        | integration update                        | 81    | integration                           |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | integration_delete                        | integration delete                        | 82    | integration                           |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | stage_create                              | stage create                              | 83    | stage                                 |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | stage_update                              | stage update                              | 84    | stage                                 |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | stage_delete                              | stage delete                              | 85    | stage                                 |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | sticker_create                            | sticker create                            | 90    | sticker                               |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | sticker_update                            | sticker update                            | 91    | sticker                               |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | sticker_delete                            | sticker delete                            | 92    | sticker                               |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | scheduled_event_create                    | scheduled event create                    | 100   | scheduled_event                       |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | scheduled_event_update                    | scheduled event update                    | 101   | scheduled_event                       |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | scheduled_event_delete                    | scheduled event delete                    | 102   | scheduled_event                       |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | thread_create                             | thread create                             | 110   | channel                               |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | thread_update                             | thread update                             | 111   | channel                               |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | thread_delete                             | thread delete                             | 112   | channel                               |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | application_command_permission_update     | application command permission update     | 121   | application_command                   |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | soundboard_sound_create                   | soundboard sound create                   | 130   | soundboard_sound                      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | soundboard_sound_update                   | soundboard sound update                   | 131   | soundboard_sound                      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | soundboard_sound_delete                   | soundboard sound delete                   | 132   | soundboard_sound                      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | auto_moderation_rule_create               | auto moderation rule create               | 140   | auto_moderation_rule                  |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | auto_moderation_rule_update               | auto moderation rule update               | 141   | auto_moderation_rule                  |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | auto_moderation_rule_delete               | auto moderation rule delete               | 142   | auto_moderation_rule                  |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | auto_moderation_block_message             | auto moderation block message             | 143   | auto_moderation_action_execution      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | auto_moderation_alert_message             | auto moderation alert message             | 144   | auto_moderation_action_execution      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | auto_moderation_user_timeout              | auto moderation user timeout              | 145   | auto_moderation_action_execution      |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | creator_monetization_request_created      | creator_monetization_request_created      | 150   | none                                  |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | creator_monetization_terms_accepted       | creator_monetization_terms_accepted       | 151   | none                                  |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | role_prompt_create                        | role_prompt_create                        | 160   | none                                  |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | role_prompt_update                        | role_prompt_update                        | 161   | none                                  |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | role_prompt_delete                        | role_prompt_delete                        | 162   | none                                  |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | onboarding_prompt_create                  | onboarding prompt create                  | 163   | onboarding_prompt                     |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | onboarding_prompt_update                  | onboarding prompt update                  | 164   | onboarding_prompt                     |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | onboarding_prompt_delete                  | onboarding prompt delete                  | 165   | onboarding_prompt                     |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | onboarding_screen_create                  | onboarding screen create                  | 166   | onboarding_screen                     |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | onboarding_screen_update                  | onboarding screen update                  | 167   | onboarding_screen                     |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | home_feature_item                         | home feature item                         | 171   | none                                  |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | home_remove_item                          | home remove item                          | 172   | none                                  |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | home_screen_create                        | home screen create                        | 190   | none                                  |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | home_screen_update                        | home screen update                        | 191   | none                                  |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | channel_status_update                     | channel status update                     | 192   | channel                               |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | channel_status_delete                     | channel status delete                     | 193   | channel                               |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | clyde_ai_update                           | clyde ai update                           | 194   | none                                  |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | scheduled_event_occasion_overwrite_create | scheduled event occasion overwrite create | 200   | scheduled_event_occasion_overwrite    |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | scheduled_event_occasion_overwrite_update | scheduled event occasion overwrite update | 201   | scheduled_event_occasion_overwrite    |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | scheduled_event_occasion_overwrite_delete | scheduled event occasion overwrite delete | 202   | scheduled_event_occasion_overwrite    |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | user_verification_update                  | user verification update                  | 210   | none                                  |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    | guild_overview_update                     | guild overview update                     | 211   | guild                                 |
    +-------------------------------------------+-------------------------------------------+-------+---------------------------------------+
    """
    __slots__ = ('target_type',)
    
    def __new__(cls, value, name = None, target_type = None):
        """
        Creates a new audit log event.
        
        Parameters
        ----------
        value : `int`
            The identifier value of the audit log event.
        
        name : `None | str` = `None`, Optional
            The audit log event's name.
        
        target_type : `None | AuditLogEntryTargetType` = `None`, Optional
            The audit log's target type.
        """
        if target_type is None:
            target_type = AuditLogEntryTargetType.none
        
        self = PreinstancedBase.__new__(cls, value, name)
        self.target_type = target_type
        return self
    
    
    @classmethod
    def _from_value(cls, value):
        """
        Creates a new audit log event object from the given value.
        
        Parameters
        ----------
        value : ``.VALUE_TYPE``
            The value what has no representation yet.
        
        Returns
        -------
        self : ``AuditLogEntryType``
            The created audit log event.
        """
        self = super(AuditLogEntryType, cls)._from_value(value)
        self.target_type = AuditLogEntryTargetType.none
        return self
    
    
    @copy_docs(PreinstancedBase._put_repr_parts_into)
    def _put_repr_parts_into(self, repr_parts):
        repr_parts.append(', target_type = ')
        repr_parts.append(self.target_type.name)
    
    
    # predefined
    none = P(0, 'none', AuditLogEntryTargetType.none)
    
    guild_update = P(1, 'guild update', AuditLogEntryTargetType.guild)
    
    channel_create = P(10, 'channel create', AuditLogEntryTargetType.channel)
    channel_update = P(11, 'channel update', AuditLogEntryTargetType.channel)
    channel_delete = P(12, 'channel delete', AuditLogEntryTargetType.channel)
    
    channel_permission_overwrite_create = P(
        13,
        'channel permission overwrite create',
        AuditLogEntryTargetType.channel_permission_overwrite,
    )
    channel_permission_overwrite_update = P(
        14,
        'channel permission overwrite update',
        AuditLogEntryTargetType.channel_permission_overwrite,
    )
    channel_permission_overwrite_delete = P(
        15,
        'channel permission overwrite delete',
        AuditLogEntryTargetType.channel_permission_overwrite,
    )
    
    user_kick = P(20, 'user kick', AuditLogEntryTargetType.user)
    user_prune = P(21, 'user prune', AuditLogEntryTargetType.guild)
    user_ban_add = P(22, 'user ban add', AuditLogEntryTargetType.user)
    user_ban_remove = P(23, 'user ban remove', AuditLogEntryTargetType.user)
    user_update = P(24, 'user update', AuditLogEntryTargetType.user)
    user_role_update = P(25, 'user role update', AuditLogEntryTargetType.user)
    user_move = P(26, 'user move', AuditLogEntryTargetType.user)
    user_disconnect = P(27, 'user disconnect', AuditLogEntryTargetType.user)
    bot_add = P(28, 'user role update', AuditLogEntryTargetType.user)
    
    role_create = P(30, 'role create', AuditLogEntryTargetType.role)
    role_update = P(31, 'role update', AuditLogEntryTargetType.role)
    role_delete = P(32, 'role delete', AuditLogEntryTargetType.role)
    
    invite_create = P(40, 'invite create', AuditLogEntryTargetType.invite)
    invite_update = P(41, 'invite update', AuditLogEntryTargetType.invite)
    invite_delete = P(42, 'invite delete', AuditLogEntryTargetType.invite)
    
    webhook_create = P(50, 'webhook create', AuditLogEntryTargetType.webhook)
    webhook_update = P(51, 'webhook update', AuditLogEntryTargetType.webhook)
    webhook_delete = P(52, 'webhook delete', AuditLogEntryTargetType.webhook)
    
    emoji_create = P(60, 'emoji create', AuditLogEntryTargetType.emoji)
    emoji_update = P(61, 'emoji update', AuditLogEntryTargetType.emoji)
    emoji_delete = P(62, 'emoji delete', AuditLogEntryTargetType.emoji)
    
    message_delete = P(72, 'message delete', AuditLogEntryTargetType.message)
    message_bulk_delete = P(73, 'message bulk delete', AuditLogEntryTargetType.message)
    message_pin = P(74, 'message pin', AuditLogEntryTargetType.message)
    message_unpin = P(75, 'message unpin', AuditLogEntryTargetType.message)
    
    integration_create = P(80, 'integration create', AuditLogEntryTargetType.integration)
    integration_update = P(81, 'integration update', AuditLogEntryTargetType.integration)
    integration_delete = P(82, 'integration delete', AuditLogEntryTargetType.integration)
    
    stage_create = P(83, 'stage create', AuditLogEntryTargetType.stage)
    stage_update = P(84, 'stage update', AuditLogEntryTargetType.stage)
    stage_delete = P(85, 'stage delete', AuditLogEntryTargetType.stage)
    
    sticker_create = P(90, 'sticker create', AuditLogEntryTargetType.sticker)
    sticker_update = P(91, 'sticker update', AuditLogEntryTargetType.sticker)
    sticker_delete = P(92, 'sticker delete', AuditLogEntryTargetType.sticker)
    
    scheduled_event_create = P(100, 'scheduled event create', AuditLogEntryTargetType.scheduled_event)
    scheduled_event_update = P(101, 'scheduled event update', AuditLogEntryTargetType.scheduled_event)
    scheduled_event_delete = P(102, 'scheduled event delete', AuditLogEntryTargetType.scheduled_event)
    
    thread_create = P(110, 'thread create', AuditLogEntryTargetType.channel)
    thread_update = P(111, 'thread update', AuditLogEntryTargetType.channel)
    thread_delete = P(112, 'thread delete', AuditLogEntryTargetType.channel)
    
    application_command_permission_update = P(
        121,
        'application command permission update',
        AuditLogEntryTargetType.application_command,
    )
    
    soundboard_sound_create =  P(130,'soundboard sound create', AuditLogEntryTargetType.soundboard_sound)
    soundboard_sound_update =  P(131, 'soundboard sound update', AuditLogEntryTargetType.soundboard_sound)
    soundboard_sound_delete = P(132, 'soundboard sound delete', AuditLogEntryTargetType.soundboard_sound)
    
    auto_moderation_rule_create = P(140, 'auto moderation rule create', AuditLogEntryTargetType.auto_moderation_rule)
    auto_moderation_rule_update = P(141, 'auto moderation rule update', AuditLogEntryTargetType.auto_moderation_rule)
    auto_moderation_rule_delete = P(142, 'auto moderation rule delete', AuditLogEntryTargetType.auto_moderation_rule)
    auto_moderation_block_message = P(
        143, 'auto moderation block message', AuditLogEntryTargetType.auto_moderation_action_execution
    )
    auto_moderation_alert_message = P(
        144, 'auto moderation alert message', AuditLogEntryTargetType.auto_moderation_action_execution
    )
    auto_moderation_user_timeout = P(
        145, 'auto moderation user timeout', AuditLogEntryTargetType.auto_moderation_action_execution
    )
    
    creator_monetization_request_created = P(150, 'creator monetization request created', AuditLogEntryTargetType.none)
    creator_monetization_terms_accepted = P(151, 'creator monetization terms accepted', AuditLogEntryTargetType.none)
    
    # These 3 are deprecated
    role_prompt_create =  P(160,'role prompt create', AuditLogEntryTargetType.none)
    role_prompt_update =  P(161, 'role prompt update', AuditLogEntryTargetType.none)
    role_prompt_delete = P(162, 'role prompt delete', AuditLogEntryTargetType.none)
    
    onboarding_prompt_create =  P(163,'onboarding prompt create', AuditLogEntryTargetType.onboarding_prompt)
    onboarding_prompt_update =  P(164, 'onboarding prompt update', AuditLogEntryTargetType.onboarding_prompt)
    onboarding_prompt_delete = P(165, 'onboarding prompt delete', AuditLogEntryTargetType.onboarding_prompt)
    
    onboarding_screen_create =  P(166,'onboarding screen create', AuditLogEntryTargetType.onboarding_screen)
    onboarding_screen_update =  P(167, 'onboarding screen update', AuditLogEntryTargetType.onboarding_screen)
    
    home_feature_item = P(171, 'home feature item', AuditLogEntryTargetType.none)
    home_remove_item = P(172, 'home remove item', AuditLogEntryTargetType.none)
    
    home_screen_create = P(190, 'home screen create', AuditLogEntryTargetType.none)
    home_screen_update = P(191, 'home screen update', AuditLogEntryTargetType.none)
    channel_status_update = P(192, 'channel status update', AuditLogEntryTargetType.channel)
    channel_status_delete = P(193, 'channel status delete', AuditLogEntryTargetType.channel)
    clyde_ai_update = P(194, 'clyde ai update', AuditLogEntryTargetType.none)
    
    scheduled_event_occasion_overwrite_create = P(
        200,
        'scheduled event occasion overwrite create',
        AuditLogEntryTargetType.scheduled_event_occasion_overwrite,
    )
    scheduled_event_occasion_overwrite_update = P(
        201,
        'scheduled event occasion overwrite update',
        AuditLogEntryTargetType.scheduled_event_occasion_overwrite,
    )
    scheduled_event_occasion_overwrite_delete = P(
        202,
        'scheduled event occasion overwrite delete',
        AuditLogEntryTargetType.scheduled_event_occasion_overwrite,
    )
    
    user_verification_update = P(201, 'user verification update', AuditLogEntryTargetType.none)
    guild_overview_update = P(202, 'guild overview update', AuditLogEntryTargetType.guild)
    
    
    @class_property
    def scheduled_event_exception_create(cls):
        """
        Deprecated and will be removed in 2016 January. Use `scheduled_event_occasion_overwrite_create.` instead.
        """
        warn(
            (
                f'`{cls.__name__}.scheduled_event_exception_create` is deprecated and will be removed 2016 January. '
                f'Use `.scheduled_event_occasion_overwrite_create` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        return cls.scheduled_event_occasion_overwrite_create
    
    
    @class_property
    def scheduled_event_exception_update(cls):
        """
        Deprecated and will be removed in 2016 January. Use `scheduled_event_occasion_overwrite_update.` instead.
        """
        warn(
            (
                f'`{cls.__name__}.scheduled_event_exception_update` is deprecated and will be removed 2016 January. '
                f'Use `.scheduled_event_occasion_overwrite_update` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        return cls.scheduled_event_occasion_overwrite_update
    
    
    @class_property
    def scheduled_event_exception_delete(cls):
        """
        Deprecated and will be removed in 2016 January. Use `scheduled_event_occasion_overwrite_delete.` instead.
        """
        warn(
            (
                f'`{cls.__name__}.scheduled_event_exception_delete` is deprecated and will be removed 2016 January. '
                f'Use `.scheduled_event_occasion_overwrite_delete` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        return cls.scheduled_event_occasion_overwrite_delete
