__all__ = ('AuditLogEvent', 'AuditLogTargetType')

from scarletio import copy_docs, export

from ...bases import Preinstance as P, PreinstancedBase

from .change_converters.all_ import MERGED_CONVERTERS
from .change_converters.application_command import APPLICATION_COMMAND_CONVERTERS
from .change_converters.auto_moderation_rule import AUTO_MODERATION_RULE_CONVERTERS
from .change_converters.channel import CHANNEL_CONVERTERS
from .change_converters.channel_permission_overwrite import CHANNEL_PERMISSION_OVERWRITE_CONVERTERS
from .change_converters.emoji import EMOJI_CONVERTERS
from .change_converters.guild import GUILD_CONVERTERS
from .change_converters.integration import INTEGRATION_CONVERTERS
from .change_converters.invite import INVITE_CONVERTERS
from .change_converters.role import ROLE_CONVERTERS
from .change_converters.scheduled_event import SCHEDULED_EVENT_CONVERTERS
from .change_converters.stage import STAGE_CONVERTERS
from .change_converters.sticker import STICKER_CONVERTERS
from .change_converters.user import USER_CONVERTERS
from .change_converters.webhook import WEBHOOK_CONVERTERS
from .target_converters import (
    target_converter_application_command, target_converter_auto_moderation_rule, target_converter_channel,
    target_converter_emoji, target_converter_guild, target_converter_integration, target_converter_invite,
    target_converter_none, target_converter_role, target_converter_scheduled_event, target_converter_stage,
    target_converter_sticker, target_converter_thread, target_converter_user, target_converter_webhook
)


class AuditLogTargetType(PreinstancedBase):
    """
    Represents the target type of an ``AuditLogEntry``.
    
    Attributes
    ----------
    name : `str`
        The name of audit log target type.
    value : `int`
        The identifier value of the audit log target type. Only used for hashing.
    target_converter : ``FunctionType``
        Audit log target converter.
    change_converters : `dict` of (`str`, `FunctionType`) items
        Audit change key change_converters.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``AuditLogTargetType``) items
        Stores the predefined ``AuditLogTargetType``-s. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The audit log target types' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the audit log target types.
    
    Every predefined audit log target type can be accessed as class attribute as well:
    
    +-------------------------------+-------------------------------+-------+-------------------------------------------+
    | Class attribute name          | name                          | value | key converters                            |
    +================================+==============================+=======+===========================================+
    | all                           | all                           | -1    | MERGED_CONVERTERS                         |
    +-------------------------------+-------------------------------+-------+-------------------------------------------+
    | none                          | none                          | 0     | N/A                                       |
    +-------------------------------+-------------------------------+-------+-------------------------------------------+
    | guild                         | guild                         | 1     | GUILD_CONVERTERS                          |
    +-------------------------------+-------------------------------+-------+-------------------------------------------+
    | channel                       | channel                       | 2     | CHANNEL_CONVERTERS                        |
    +-------------------------------+-------------------------------+-------+-------------------------------------------+
    | channel_permission_overwrite  | channel permission overwrite  | 3     | CHANNEL_PERMISSION_OVERWRITE_CONVERTERS   |
    +-------------------------------+-------------------------------+-------+-------------------------------------------+
    | user                          | user                          | 4     | USER_CONVERTERS                           |
    +-------------------------------+-------------------------------+-------+-------------------------------------------+
    | role                          | role                          | 5     | ROLE_CONVERTERS                           |
    +-------------------------------+-------------------------------+-------+-------------------------------------------+
    | invite                        | invite                        | 6     | INVITE_CONVERTERS                         |
    +-------------------------------+-------------------------------+-------+-------------------------------------------+
    | webhook                       | webhook                       | 7     | WEBHOOK_CONVERTERS                        |
    +-------------------------------+-------------------------------+-------+-------------------------------------------+
    | emoji                         | emoji                         | 8     | EMOJI_CONVERTERS                          |
    +-------------------------------+-------------------------------+-------+-------------------------------------------+
    | integration                   | integration                   | 9     | INTEGRATION_CONVERTERS                    |
    +-------------------------------+-------------------------------+-------+-------------------------------------------+
    | stage                         | stage                         | 10    | STAGE_CONVERTERS                          |
    +-------------------------------+-------------------------------+-------+-------------------------------------------+
    | scheduled_event               | scheduled event               | 11    | SCHEDULED_EVENT_CONVERTERS                |
    +-------------------------------+-------------------------------+-------+-------------------------------------------+
    | sticker                       | sticker                       | 12    | STICKER_CONVERTERS                        |
    +-------------------------------+-------------------------------+-------+-------------------------------------------+
    | application_command           | application command           | 13    | APPLICATION_COMMAND_CONVERTERS            |
    +-------------------------------+-------------------------------+-------+-------------------------------------------+
    | thread                        | thread                        | 14    | CHANNEL_CONVERTERS                        |
    +-------------------------------+-------------------------------+-------+-------------------------------------------+
    | auto_moderation_rule          | auto moderation rule          | 15    | AUTO_MODERATION_RULE_CONVERTERS           |
    +-------------------------------+-------------------------------+-------+-------------------------------------------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ('target_converter', 'change_converters', )
    
    # predefined
    all = P(-1, 'all', target_converter_none, MERGED_CONVERTERS)
    none = P(0, 'none', target_converter_none, {})
    guild = P(1, 'guild', target_converter_guild, GUILD_CONVERTERS)
    channel = P(2, 'channel', target_converter_channel, CHANNEL_CONVERTERS)
    channel_permission_overwrite = P(
        3, 'channel permission overwrite', target_converter_channel, CHANNEL_PERMISSION_OVERWRITE_CONVERTERS,
    )
    user = P(4, 'user', target_converter_user, USER_CONVERTERS)
    role = P(5, 'role', target_converter_role, ROLE_CONVERTERS)
    invite = P(6, 'invite', target_converter_invite, INVITE_CONVERTERS)
    webhook = P(7, 'webhook', target_converter_webhook, WEBHOOK_CONVERTERS)
    emoji = P(8, 'emoji', target_converter_emoji, EMOJI_CONVERTERS)
    integration = P(9, 'integration', target_converter_integration, INTEGRATION_CONVERTERS)
    stage = P(10, 'stage', target_converter_stage, STAGE_CONVERTERS)
    scheduled_event = P(11, 'scheduled event', target_converter_scheduled_event, SCHEDULED_EVENT_CONVERTERS)
    sticker = P(12, 'sticker', target_converter_sticker, STICKER_CONVERTERS)
    application_command = P(
        13, 'application command', target_converter_application_command, APPLICATION_COMMAND_CONVERTERS,
    )
    thread = P(14, 'thread', target_converter_thread, CHANNEL_CONVERTERS)
    auto_moderation_rule = P(
        15, 'auto moderation rule', target_converter_auto_moderation_rule, AUTO_MODERATION_RULE_CONVERTERS
    )
    
    
    @copy_docs(PreinstancedBase.__repr__)
    def __repr__(self):
        return f'<{self.__class__.__name__} name={self.name!r}>'
    
    
    def __init__(self, value, name, target_converter, change_converters):
        """
        Creates a new audit log target type and stores it at the class's `.INSTANCES` class attribute.
        
        Parameters
        ----------
        value : `int`
            The identifier value of the audit log target type.
        name : `str`
            The name of the audit log target type.
        target_converter : ``FunctionType``
            Audit log target converter.
        change_converters : `dict` of (`str`, `FunctionType`) items
            Audit change key change_converters.
        """
        self.target_converter = target_converter
        self.change_converters = change_converters
        PreinstancedBase.__init__(self, value, name)
    
    
    @classmethod
    def _from_value(cls, value):
        """
        Creates a new audit log target type object from the given value.
        
        Parameters
        ----------
        value : ``.VALUE_TYPE``
            The value what has no representation yet.
        
        Returns
        -------
        self : ``Status``
            The created audit log target type.
        """
        self = super(AuditLogTargetType, cls)._from_value(value)
        self.change_converters = {}
        self.target_converter = target_converter_none
        return self


@export
class AuditLogEvent(PreinstancedBase):
    """
    Represents the event type of an ``AuditLogEntry``.
    
    Attributes
    ----------
    name : `str`
        The name of audit log event.
    value : `int`
        The Discord side identifier value of the audit log event.
    target_type : ``AuditLogTargetType``
        The audit log's target's type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``AuditLogEvent``) items
        Stores the predefined ``AuditLogEvent``-s. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The audit log events' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the audit log events.
    
    Every predefined audit log event can be accessed as class attribute as well:
    
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | Class attribute name                  | name                                  | value | target type                   |
    +=======================================+=======================================+=======+===============================+
    | guild_update                          | guild update                          |  1    | guild                         |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | channel_create                        | channel create                        | 10    | channel                       |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | channel_update                        | channel update                        | 11    | channel                       |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | channel_delete                        | channel delete                        | 12    | channel                       |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | channel_permission_overwrite_create   | channel permission overwrite create   | 13    | channel_permission_overwrite  |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | channel_permission_overwrite_update   | channel permission overwrite update   | 14    | channel_permission_overwrite  |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | channel_permission_overwrite_delete   | channel permission overwrite delete   | 15    | channel_permission_overwrite  |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | member_kick                           | member kick                           | 20    | user                          |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | member_prune                          | member prune                          | 21    | guild                         |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | member_ban_add                        | member ban add                        | 22    | user                          |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | member_ban_remove                     | member ban remove                     | 23    | user                          |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | member_update                         | member update                         | 24    | user                          |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | member_role_update                    | member role update                    | 25    | user                          |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | member_move                           | member move                           | 26    | user                          |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | member_disconnect                     | member disconnect                     | 27    | user                          |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | bot_add                               | bot add                               | 28    | user                          |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | role_create                           | role create                           | 30    | role                          |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | role_update                           | role update                           | 31    | role                          |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | role_delete                           | role delete                           | 32    | role                          |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | invite_create                         | invite create                         | 40    | invite                        |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | invite_update                         | invite update                         | 41    | invite                        |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | invite_delete                         | invite delete                         | 42    | invite                        |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | webhook_create                        | webhook create                        | 50    | webhook                       |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | webhook_update                        | webhook update                        | 51    | webhook                       |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | webhook_delete                        | webhook delete                        | 52    | webhook                       |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | emoji_create                          | emoji create                          | 60    | emoji                         |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | emoji_update                          | emoji update                          | 61    | emoji                         |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | emoji_delete                          | emoji delete                          | 62    | emoji                         |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | message_delete                        | message delete                        | 72    | none                          |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | message_bulk_delete                   | message bulk delete                   | 73    | none                          |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | message_pin                           | message pin                           | 74    | none                          |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | message_unpin                         | message unpin                         | 75    | none                          |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | integration_create                    | integration create                    | 80    | integration                   |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | integration_update                    | integration update                    | 81    | integration                   |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | integration_delete                    | integration delete                    | 82    | integration                   |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | stage_create                          | stage create                          | 83    | stage                         |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | stage_update                          | stage update                          | 84    | stage                         |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | stage_delete                          | stage delete                          | 85    | stage                         |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | sticker_create                        | sticker create                        | 90    | sticker                       |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | sticker_update                        | sticker update                        | 91    | sticker                       |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | sticker_delete                        | sticker delete                        | 92    | sticker                       |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | scheduled_event_create                | scheduled event create                | 100   | scheduled_event               |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | scheduled_event_update                | scheduled event update                | 101   | scheduled_event               |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | scheduled_event_delete                | scheduled event delete                | 102   | scheduled_event               |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | thread_create                         | thread create                         | 110   | thread                        |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | thread_update                         | thread update                         | 111   | thread                        |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | thread_delete                         | thread delete                         | 112   | thread                        |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | application_command_permission_update | application command permission update | 121   | application_command           |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | auto_moderation_rule_create           | auto moderation rule create           | 140   | auto_moderation_rule          |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | auto_moderation_rule_edit             | auto moderation rule edit             | 141   | auto_moderation_rule          |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | auto_moderation_rule_delete           | auto moderation rule delete           | 142   | auto_moderation_rule          |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | auto_moderation_block_message         | auto moderation block message         | 143   | none                          |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | auto_moderation_alert_message         | auto moderation alert message         | 144   | none                          |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | auto_moderation_user_timeout          | auto moderation user timeout          | 145   | none                          |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | creator_monetization_request_created  | creator_monetization_request_created  | 150   | none                          |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | creator_monetization_terms_accepted   | creator_monetization_terms_accepted   | 151   | none                          |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | role_prompt_create                    | role_prompt_create                    | 160   | none                          |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | role_prompt_edit                      | role_prompt_edit                      | 161   | none                          |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | role_prompt_delete                    | role_prompt_delete                    | 162   | none                          |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | guild_home_feature_item               | guild_home_feature_item               | 171   | none                          |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    | guild_home_remove_item                | guild_home_remove_item                | 172   | none                          |
    +---------------------------------------+---------------------------------------+-------+-------------------------------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ('target_type',)
    
    # predefined
    guild_update = P(1, 'guild update', AuditLogTargetType.guild)
    
    channel_create = P(10, 'channel create', AuditLogTargetType.channel)
    channel_update = P(11, 'channel update', AuditLogTargetType.channel)
    channel_delete = P(12, 'channel delete', AuditLogTargetType.channel)
    
    channel_permission_overwrite_create = P(
        13,
        'channel permission overwrite create',
        AuditLogTargetType.channel_permission_overwrite,
    )
    channel_permission_overwrite_update = P(
        14,
        'channel permission overwrite update',
        AuditLogTargetType.channel_permission_overwrite,
    )
    channel_permission_overwrite_delete = P(
        15,
        'channel permission overwrite delete',
        AuditLogTargetType.channel_permission_overwrite,
    )
    
    member_kick = P(20, 'member kick', AuditLogTargetType.user)
    member_prune = P(21, 'member prune', AuditLogTargetType.guild)
    member_ban_add = P(22, 'member ban add', AuditLogTargetType.user)
    member_ban_remove = P(23, 'member ban remove', AuditLogTargetType.user)
    member_update = P(24, 'member update', AuditLogTargetType.user)
    member_role_update = P(25, 'member role update', AuditLogTargetType.user)
    member_move = P(26, 'member move', AuditLogTargetType.user)
    member_disconnect = P(27, 'member disconnect', AuditLogTargetType.user)
    bot_add = P(28, 'member role update', AuditLogTargetType.user)
    
    role_create = P(30, 'role create', AuditLogTargetType.role)
    role_update = P(31, 'role update', AuditLogTargetType.role)
    role_delete = P(32, 'role delete', AuditLogTargetType.role)
    
    invite_create = P(40, 'invite create', AuditLogTargetType.invite)
    invite_update = P(41, 'invite update', AuditLogTargetType.invite)
    invite_delete = P(42, 'invite delete', AuditLogTargetType.invite)
    
    webhook_create = P(50, 'webhook create', AuditLogTargetType.webhook)
    webhook_update = P(51, 'webhook update', AuditLogTargetType.webhook)
    webhook_delete = P(52, 'webhook delete', AuditLogTargetType.webhook)
    
    emoji_create = P(60, 'emoji create', AuditLogTargetType.emoji)
    emoji_update = P(61, 'emoji update', AuditLogTargetType.emoji)
    emoji_delete = P(62, 'emoji delete', AuditLogTargetType.emoji)
    
    message_delete = P(72, 'message delete', AuditLogTargetType.none)
    message_bulk_delete = P(73, 'message bulk delete', AuditLogTargetType.none)
    message_pin = P(74, 'message pin', AuditLogTargetType.none)
    message_unpin = P(75, 'message unpin', AuditLogTargetType.none)
    
    integration_create = P(80, 'integration create', AuditLogTargetType.integration)
    integration_update = P(81, 'integration update', AuditLogTargetType.integration)
    integration_delete = P(82, 'integration delete', AuditLogTargetType.integration)
    
    stage_create = P(83, 'stage create', AuditLogTargetType.stage)
    stage_update = P(84, 'stage update', AuditLogTargetType.stage)
    stage_delete = P(85, 'stage delete', AuditLogTargetType.stage)
    
    sticker_create = P(90, 'sticker create', AuditLogTargetType.sticker)
    sticker_update = P(91, 'sticker update', AuditLogTargetType.sticker)
    sticker_delete = P(92, 'sticker delete', AuditLogTargetType.sticker)
    
    scheduled_event_create = P(100, 'scheduled event create', AuditLogTargetType.scheduled_event)
    scheduled_event_update = P(101, 'scheduled event update', AuditLogTargetType.scheduled_event)
    scheduled_event_delete = P(102, 'scheduled event delete', AuditLogTargetType.scheduled_event)
    
    thread_create = P(110, 'thread create', AuditLogTargetType.thread)
    thread_update = P(111, 'thread update', AuditLogTargetType.thread)
    thread_delete = P(112, 'thread delete', AuditLogTargetType.thread)
    
    application_command_permission_update = P(
        121,
        'application command permission update',
        AuditLogTargetType.application_command,
    )
    
    auto_moderation_rule_create = P(140, 'auto moderation rule create', AuditLogTargetType.auto_moderation_rule)
    auto_moderation_rule_edit = P(141, 'auto moderation rule edit', AuditLogTargetType.auto_moderation_rule)
    auto_moderation_rule_delete = P(142, 'auto moderation rule delete', AuditLogTargetType.auto_moderation_rule)
    auto_moderation_block_message = P(143, 'auto moderation block message', AuditLogTargetType.none)
    auto_moderation_alert_message = P(143, 'auto moderation alert message', AuditLogTargetType.none)
    auto_moderation_user_timeout = P(143, 'auto moderation user timeout', AuditLogTargetType.none)
    
    creator_monetization_request_created = P(150, 'creator monetization request created', AuditLogTargetType.none)
    creator_monetization_terms_accepted = P(151, 'creator monetization terms accepted', AuditLogTargetType.none)
    
    role_prompt_create =  P(160,'role prompt create', AuditLogTargetType.none)
    role_prompt_edit =  P(161, 'role prompt edit', AuditLogTargetType.none)
    role_prompt_delete = P(162, 'role prompt delete', AuditLogTargetType.none)
    
    guild_home_feature_item = P(171, 'guild_home_feature_item', AuditLogTargetType.none)
    guild_home_remove_item = P(172, 'guild_home_remove_item', AuditLogTargetType.none)
    
    
    def __init__(self, value, name, target_type):
        """
        Creates a new audit log event and stores it at the class's `.INSTANCES` class attribute.
        
        Parameters
        ----------
        value : `int`
            The identifier value of the audit log event.
        name : `str`
            The audit log event's name.
        target_type : ``AuditLogTargetType`
            The audit log's target type.
        """
        self.target_type = target_type
        PreinstancedBase.__init__(self, value, name)
    
    
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
        self : ``AuditLogEvent``
            The created audit log event.
        """
        self = super(AuditLogEvent, cls)._from_value(value)
        self.target_type = AuditLogTargetType.all
        return self
    
    
    @copy_docs(PreinstancedBase.__repr__)
    def __repr__(self):
        return (
            f'<{self.__class__.__name__} '
            f'name={self.name!r}, '
            f'value={self.value!r}, '
            f'target_type={self.target_type.name!r}'
            '>'
        )
