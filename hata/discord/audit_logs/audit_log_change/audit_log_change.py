__all__ = ('AuditLogChange', )

from scarletio import RichAttributeErrorBaseType

from ..conversion_helpers.helpers import _hash_change_value

from .fields import validate_attribute_name
from .flags import FLAG_HAS_AFTER, FLAG_HAS_BEFORE


class AuditLogChange(RichAttributeErrorBaseType):
    """
    A change of an ``AuditLogEntry``.
    
    Attributes
    ----------
    after : `object`
        The changed attribute's new value. Defaults to `None`.
    attribute_name : `str`
        The name of the changed attribute.
    before : `object`
        The changed attribute's original value. Defaults to `None`.
    flags : `int`
        Bitwise flags containing additional details.
    
    Notes
    -----
    The value of `before` and `after` depending on the value of `attribute_name`. These are:
    
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | Attribute name                        | before / after                                                                        |
    +=======================================+=======================================================================================+
    | actions                               | `None`, `tuple` of ``AutoModerationAction``                                           |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | afk_channel_id                        | `None`, `int`                                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | afk_timeout                           | `None`, `bool`                                                                        |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | allow                                 | `None`, ``Permission``                                                                |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | application_command_id                | `None`, `int`                                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | application_id                        | `None`, `int`                                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | applied_tag_ids                       | `None`, `tuple` of `int`                                                              |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | archived                              | `None`, `bool`                                                                        |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | auto_archive_duration                 | `None`, `int`                                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | available                             | `None`, `bool`                                                                        |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | available_tags                        | `None`, `tuple` of ``ForumTag``                                                       |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | avatar                                | `None`, ``Icon``                                                                      |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | banner                                | `None`, ``Icon``                                                                      |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | bitrate                               | `None`, `int`                                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | boost_progress_bar_enabled            | `None`, `bool`                                                                        |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | bypasses_verification                 | `None`, `bool`                                                                        |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | channel_id                            | `None`, `int`                                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | code                                  | `None`, `str`                                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | color                                 | `None`, ``Color``                                                                     |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | communication_disabled_until          | `None`, `DateTime`                                                                    |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | creator_id                            | `None`, `int`                                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | default_channel_ids                   | `None`, `tuple` of `int`                                                              |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | days                                  | `None`, `int`                                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | deaf                                  | `None`, `bool`                                                                        |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | description                           | `None`, `str`                                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | default_message_notification          | `None`, ``MessageNotificationLevel``                                                  |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | default_forum_layout                  | `None`, ``ForumLayout``                                                               |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | default_message_notification_level    | `None`, ``MessageNotificationLevel``                                                  |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | default_sort_order                    | `None`, ``SortOrder``                                                                 |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | default_thread_auto_archive_after     | `None`, `int`                                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | default_thread_reaction_emoji         | `None`, ``Emoji``                                                                     |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | default_thread_slowmode               | `None`, `int`                                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | deny                                  | `None`, ``Permission``                                                                |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | discovery_splash                      | `None`, ``Icon``                                                                      |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | emoji                                 | `None`, ``Emoji``                                                                     |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | emojis_enabled                        | `None`, `bool`                                                                        |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | enabled                               | `None`, `bool`                                                                        |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | end                                   | `None`, `DateTime`                                                                    |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | entity_id                             | `None`, `int`                                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | entity_metadata                       | `None`, ``ScheduledEventEntityMetadataBase``                                          |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | entity_type                           | `None`, ``ScheduledEventEntityType``                                                  |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | event_type                            | `None`, ``AutoModerationEventType``                                                   |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | excluded_channel_ids                  | `None`, `tuple` of `int`                                                              |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | excluded_keywords                     | `None`, `tuple` of `str`                                                              |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | excluded_role_ids                     | `None`, `tuple` of `int`                                                              |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | expire_behavior                       | `None`, ``IntegrationExpireBehavior``                                                 |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | expire_grace_period                   | `None`, `int`                                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | explicit_content_filter_level         | `None`, ``ExplicitContentFilterLevel``                                                |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | flags                                 | `None`, ``ChannelFlag``, ``RoleFlag``, ``InviteFlag``, ``GuildProfileFlag``           |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | format                                | `None`, ``StickerFormat``                                                             |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | guild_id                              | `None`, `int`                                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | hub_type                              | `None`, ``HubType``                                                                   |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | icon                                  | `None`, ``Icon``                                                                      |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | id                                    | `None`, `int`                                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | image                                 | `None`, ``Icon``                                                                      |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | in_onboarding                         | `None`, `bool`                                                                        |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | invitable                             | `None`, `bool`                                                                        |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | invite_splash                         | `None`, ``Icon``                                                                      |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | inviter_id                            | `None`, `int`                                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | keywords                              | `None`, `tuple` of `str`                                                              |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | locale                                | `None`, ``Locale``                                                                    |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | max_age                               | `None`, `int`                                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | max_stage_channel_video_users         | `None`, `int`                                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | max_uses                              | `None`, `int`                                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | max_voice_channel_video_users         | `None`, `bool`                                                                        |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | mention_limit                         | `None`, `bool`                                                                        |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | mentionable                           | `None`, `bool`                                                                        |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | mfa_level                             | `None`, ``MfaLevel``                                                                  |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | mute                                  | `None`, `bool`                                                                        |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | name                                  | `None`, `str`                                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | nick                                  | `None`, `str`                                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | nsfw                                  | `None`, `bool`                                                                        |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | nsfw_level                            | `None`, ``NsfwLevel``                                                                 |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | options                               | `None`, `tuple` of ``OnboardingPromptOption``                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | owner_id                              | `None`, `int`                                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | parent_id                             | `None`, `int`                                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | pending                               | `None`, `bool`                                                                        |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | permission_overwrites                 | `None`, `dict` of (`int`, ``PermissionOverwrite``) items                              |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | permissions                           | `None`, ``Permission``                                                                |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | privacy_level                         | `None`, ``PrivacyLevel``                                                              |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | prompts                               | `None`, `tuple` of ``OnboardingPrompt``                                               |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | position                              | `None`, `int`                                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | public_updates_channel_id             | `None`, `int`                                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | raid_protection                       | `None`, `bool`                                                                        |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | regex_patterns                        | `None`, `tuple` of `str`                                                              |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | region                                | `None`, ``VoiceRegion``                                                               |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | required                              | `None`, `bool`                                                                        |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | role_ids                              | `None`, `tuple` of `int`                                                              |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | roles                                 | `None`, `tuple` of ``AuditLogRole``                                                   |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | rules_channel_id                      | `None`, `int`                                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | safety_alerts_channel_id              | `None`, `int`                                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | separated                             | `None`, `bool`                                                                        |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | single_select                         | `None`, `bool`                                                                        |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | slowmode                              | `None`, `int`                                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | sku_ids                               | `None`, `tuple` of `int`                                                              |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | start                                 | `None`, `DateTime`                                                                    |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | system_channel_flags                  | `None`, ``SystemChannelFlag``                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | system_channel_id                     | `None`, `int`                                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | tags                                  | `None`, `frozenset` of `str`                                                          |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | target_id                             | `None`, `int`                                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | target_type                           | `None`, ``PermissionOverwriteTargetType``                                             |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | temporary                             | `None`, `bool`                                                                        |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | timed_out_until                       | `None`, `DateTime`                                                                    |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | topic                                 | `None`, `str`                                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | trigger_metadata                      | `None`, ``AutoModerationRuleTriggerMetadataBase``                                     |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | trigger_type                          | `None`, ``AutoModerationRuleTriggerType``                                             |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | type                                  | `None`, ``ChannelType```, ``OnboardingPromptType``, ``WebhookType``, ``StickerType``, |
    |                                       | ``IntegrationType``                                                                   |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | unicode_emoji                         | `None`, ``Emoji``                                                                     |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | user_id                               | `None`, `int`                                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | user_limit                            | `None`, `int`                                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | uses                                  | `None`, `int`                                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | vanity_code                           | `None`, `str`                                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | verification_level                    | `None`, ``VerificationLevel``                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | widget_channel_id                     | `None`, `int`                                                                         |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    | widget_enabled                        | `None`, `bool`                                                                        |
    +---------------------------------------+---------------------------------------------------------------------------------------+
    """
    __slots__ = ('after', 'attribute_name', 'before', 'flags')
    
    def __new__(cls, attribute_name, *, before = ..., after = ...):
        """
        Creates a new audit log change instance.
        
        Parameters
        ----------
        attribute_name : `str`
            The name of the changed attribute.
        after : `object`
            The changed attribute's new value.
        before : `object`, Optional (Keyword only)
            The changed attribute's original value.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        attribute_name = validate_attribute_name(attribute_name)
        flags = 0
        
        # after
        if after is ...:
            after = None
        else:
            flags |= FLAG_HAS_AFTER
        
        # before
        if before is ...:
            before = None
        else:
            flags |= FLAG_HAS_BEFORE
        
        # Construct
        self = object.__new__(cls)
        self.after = after
        self.attribute_name = attribute_name
        self.before = before
        self.flags = flags
        return self
    
    
    @classmethod
    def create_clean(cls, attribute_name):
        """
        Creates a new clean audit log instance.
        Not like ``.__new__`` this skips validations and only accepts `attribute_name`. For internal use only.
        

        Parameters
        ----------
        attribute_name : `str`
            The name of the changed attribute.
        
        Returns
        -------
        self : `instance<cls>`
        """
        # Construct
        self = object.__new__(cls)
        self.after = None
        self.attribute_name = attribute_name
        self.before = None
        self.flags = 0
        return self
    
    
    @classmethod
    def from_fields(cls, attribute_name, flags, before, after):
        """
        Creates a new audit log change instance.
        Not like ``.__new__`` this has no validations. For internal use only.
        
        Parameters
        ----------
        attribute_name : `str`
            The name of the changed attribute.
        after : `object`
            The changed attribute's new value.
        before : `object`
            The changed attribute's original value.
        flags : `int`
            Bitwise flags containing additional details.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.after = after
        self.attribute_name = attribute_name
        self.before = before
        self.flags = flags
        return self
    
    
    def __repr__(self):
        """Returns the representation of the audit log change."""
        repr_parts = ['<', self.__class__.__name__]
        
        # attribute_name
        repr_parts.append(' attribute_name = ')
        repr_parts.append(repr(self.attribute_name))
        
        flags = self.flags
        if flags & FLAG_HAS_BEFORE:
            repr_parts.append(', before = ')
            repr_parts.append(repr(self.before))
        
        if flags & FLAG_HAS_AFTER:
            repr_parts.append(', after = ')
            repr_parts.append(repr(self.after))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two audit log changes are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # attribute_name
        if self.attribute_name != other.attribute_name:
            return False
        
        # flags
        if self.flags != other.flags:
            return False
        
        # before
        if self.before != other.before:
            return False
        
        # after
        if self.after != other.after:
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the hash value of the audit log change."""
        hash_value = 0
        
        # attribute_name
        hash_value ^= hash(self.attribute_name)
        
        # flags
        hash_value ^= hash(self.flags)
        
        # before
        hash_value ^= _hash_change_value(self.before)
        
        # after
        hash_value ^= _hash_change_value(self.after)
        
        return hash_value
    
    
    def has_before(self):
        """
        Returns whether the change has `before` value.
        
        Returns
        -------
        has_before : `bool`
        """
        return True if self.flags & FLAG_HAS_BEFORE else False
    
    
    def has_after(self):
        """
        Returns whether the change has `after` value.
        
        Returns
        -------
        has_after : `bool`
        """
        return True if self.flags & FLAG_HAS_AFTER else False