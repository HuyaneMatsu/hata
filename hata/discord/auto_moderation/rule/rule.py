__all__ = ('AutoModerationRule',)

from ...bases import DiscordEntity
from ...channel import ChannelType, create_partial_channel_from_id
from ...core import AUTO_MODERATION_RULES, GUILDS
from ...role import create_partial_role_from_id
from ...precreate_helpers import process_precreate_parameters
from ...user import ZEROUSER, create_partial_user_from_id

from ..trigger_metadata import AutoModerationRuleTriggerMetadataBase

from .fields import (
    parse_actions, parse_creator_id, parse_enabled, parse_event_type, parse_excluded_channel_ids,
    parse_excluded_role_ids, parse_guild_id, parse_id, parse_name, parse_trigger_metadata, parse_trigger_type,
    put_actions_into, put_creator_id_into, put_enabled_into, put_event_type_into, put_excluded_channel_ids_into,
    put_excluded_role_ids_into, put_guild_id_into, put_id_into, put_name_into, put_trigger_metadata_into,
    put_trigger_type_into, validate_actions, validate_creator_id, validate_enabled, validate_event_type,
    validate_excluded_channel_ids, validate_excluded_role_ids, validate_guild_id, validate_id, validate_name,
    validate_trigger_type
)
from .helpers import guess_rule_trigger_type_from_keyword_parameters
from .preinstanced import AutoModerationEventType, AutoModerationRuleTriggerType


PRECREATE_FIELDS = {
    'actions': ('actions', validate_actions),
    'creator_id': ('creator_id', validate_creator_id),
    'enabled': ('enabled', validate_enabled),
    'event_type': ('event_type', validate_event_type),
    'excluded_channel_ids': ('excluded_channel_ids', validate_excluded_channel_ids),
    'excluded_role_ids': ('excluded_role_ids', validate_excluded_role_ids),
    'guild_id': ('guild_id', validate_guild_id),
    'name': ('name', validate_name),
}


class AutoModerationRule(DiscordEntity, immortal = True):
    """
    Auto moderation feature which allows guilds to set rules that trigger based on some criteria.
    
    Attributes
    ----------
    id : `int`
        The unique identifier of the auto moderation rule. Defaults to `0`.
    
    actions : `None`, `tuple` of ``AutoModerationAction``
        Actions which will execute when the rule is triggered. Defaults to `0`.
    
    creator_id : `int`
        The user who created the rule. Defaults to `0`.
    
    enabled : `bool`
        Whether the rule is enabled.
    
    event_type : ``AutoModerationEventType``
        For which events is the rule applied.
    
    excluded_channel_ids : `None`, `tuple` of `int`
        The excluded channels' identifiers.
    
    excluded_role_ids : `None`, `tuple` of `int`
        The excluded roles' identifiers.
    
    guild_id : `int`
        The guild's identifier where the rule is. Defaults to `0`.
    
    name : `str`
        The rule's name.
    
    trigger_metadata : ``AutoModerationRuleTriggerMetadataBase``
        Trigger type specific metadata if applicable.
    
    trigger_type : ``AutoModerationRuleTriggerType``
        Characterizes the type of content which can trigger the rule.
    """
    __slots__ = (
        'actions', 'creator_id', 'enabled', 'event_type', 'excluded_channel_ids', 'excluded_role_ids', 'guild_id',
        'name', 'trigger_metadata', 'trigger_type'
    )
    
    
    def __new__(
        cls,
        name = ...,
        actions = ...,
        trigger_type=...,
        *,
        enabled = ...,
        event_type = ...,
        excluded_channel_ids = ...,
        excluded_role_ids = ...,
        **keyword_parameters,
    ):
        """
        Creates a new auto moderation rule with the given parameters.
        
        Parameters
        ----------
        name : `str`, Optional
            The rule's name.
        
        actions : `None`, ``AutoModerationAction``, `iterable` of ``AutoModerationAction``, Optional
             Actions which will execute when the rule is triggered.
        
        trigger_type : ``AutoModerationRuleTriggerType``, `int`, Optional
            Auto moderation trigger type.
        
        enabled : `bool` , Optional (Keyword only)
            Whether the rule is enabled.
        
        event_type : `None`, `int`, ``AutoModerationEventType``, Optional (Keyword only)
            For which events is the rule applied.
        
        excluded_channel_ids : `None`, `int`, ``Channel``, `iterable` of (`int`, ``Channel``), Optional (Keyword only)
            Excluded channels from the rule.
        
        excluded_role_ids : `None`, `int`, ``Role``, `iterable` of (`int`, ``Role``), Optional (Keyword only)
            Excluded roles from the rule.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters defining how the rule is triggered.
        
        Other Parameters
        ----------------
        excluded_keywords : `None`, `str`, `iterable` of `str`, Optional (Keyword only)
            Excluded keywords from preset filter.
        
        keyword_presets : `None`, `int`, ``AutoModerationKeywordPresetType``, \
                `iterable` of (`int`, ``AutoModerationKeywordPresetType``), Optional (Keyword only)
            Keyword preset defined by Discord which will be searched for in content.
            
        keywords : `None`, `str`, `iterable` of `str`, Optional (Keyword only)
            Substrings which will be searched for in content.
        
        mention_limit : `None`, `int`, Optional (Keyword only)
            The amount of mentions in a message after the rule is triggered.
        
        regex_patterns : `None`, `tuple` of `str`, Optional (Keyword only)
            Regular expression patterns which are matched against content.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # actions
        if actions is ...:
            actions = None
        else:
            actions = validate_actions(actions)
        
        # enabled
        if enabled is ...:
            enabled = True
        else:
            enabled = validate_enabled(enabled)
        
        # event_type
        if event_type is ...:
            event_type = AutoModerationEventType.message_send
        else:
            event_type = validate_event_type(event_type)
        
        # excluded_channel_ids
        if excluded_channel_ids is ...:
            excluded_channel_ids = None
        else:
            excluded_channel_ids = validate_excluded_channel_ids(excluded_channel_ids)
        
        # excluded_role_ids
        if excluded_role_ids is ...:
            excluded_role_ids = None
        else:
            excluded_role_ids = validate_excluded_role_ids(excluded_role_ids)
        
        # name
        if name is ...:
            name = ''
        else:
            name = validate_name(name)
        
        # trigger_type
        if trigger_type is ...:
            trigger_type = AutoModerationRuleTriggerType.none
        else:
            trigger_type = validate_trigger_type(trigger_type)
        
        # **keyword_parameters
        trigger_type = guess_rule_trigger_type_from_keyword_parameters(trigger_type, keyword_parameters)
        trigger_metadata = trigger_type.metadata_type(**keyword_parameters)
        
        self = object.__new__(cls)
        self.actions = actions
        self.creator_id = 0
        self.enabled = enabled
        self.event_type = event_type
        self.excluded_channel_ids = excluded_channel_ids
        self.excluded_role_ids = excluded_role_ids
        self.guild_id = 0
        self.id = 0
        self.name = name
        self.trigger_metadata = trigger_metadata
        self.trigger_type = trigger_type
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new ``AutoModerationRule`` from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Received auto moderation rule data.
        
        Returns
        -------
        self : ``AutoModerationRule``
            The created auto moderation rule.
        """
        auto_moderation_rule_id = parse_id(data)
        
        try:
            self = AUTO_MODERATION_RULES[auto_moderation_rule_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = auto_moderation_rule_id
            self._set_attributes(data)
            AUTO_MODERATION_RULES[auto_moderation_rule_id] = self
        
        else:
            self._update_attributes(data)
        
        return self
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Converts the auto moderation rule to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included.
                
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        
        put_actions_into(self.actions, data, defaults)
        
        if include_internals:
            put_creator_id_into(self.creator_id, data, defaults)
        
        put_enabled_into(self.enabled, data, defaults)
        put_event_type_into(self.event_type, data, defaults)
        put_excluded_channel_ids_into(self.excluded_channel_ids, data, defaults)
        put_excluded_role_ids_into(self.excluded_role_ids, data, defaults)
        
        if include_internals:
            put_guild_id_into(self.guild_id, data, defaults)
            put_id_into(self.id, data, defaults)
        
        put_name_into(self.name, data, defaults)
        put_trigger_metadata_into(self.trigger_metadata, data, defaults)
        put_trigger_type_into(self.trigger_type, data, defaults)
        
        return data
    
    
    def _set_attributes(self, data):
        """
        Sets the auto moderation rule's attributes (excluding ``.id``).
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Received guild profile data.
        """        
        self.creator_id = parse_creator_id(data)
        self.guild_id = parse_guild_id(data)
        
        self._update_attributes(data)
    
    
    def _update_attributes(self, data):
        """
        Updates the auto moderation rule with overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Received guild profile data.
        """
        self.actions = parse_actions(data)
        # creator_id | Internal field & cannot change
        self.enabled = parse_enabled(data)
        self.event_type = parse_event_type(data)
        self.excluded_channel_ids = parse_excluded_channel_ids(data)
        self.excluded_role_ids = parse_excluded_role_ids(data)
        # guild_id | Internal field & cannot change
        self.name = parse_name(data)
        # id | Already set & cannot change
        self.trigger_type = trigger_type = parse_trigger_type(data)
        self.trigger_metadata = parse_trigger_metadata(data, trigger_type)
    
    
    def _difference_update_attributes(self, data):
        """
        Updates the auto moderation rule and returns the changed attributes in a dictionary with the changed attributes
        in a `attribute-name`, `old-value` relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Received guild profile data.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `object`) items
            All item in the returned dict is optional.
            
            Might contain the following items:
            
            +-------------------------------+-----------------------------------------------------------+
            | Keys                          | Values                                                    |
            +===============================+===========================================================+
            | actions                       | `None`, `tuple` of ``AutoModerationAction``               |
            +-------------------------------+-----------------------------------------------------------+
            | enabled                       | `bool`                                                    |
            +-------------------------------+-----------------------------------------------------------+
            | event_type                    | ``AutoModerationEventType``                               |
            +-------------------------------+-----------------------------------------------------------+
            | excluded_channel_ids          | `None`, `tuple` of `int`                                  |
            +-------------------------------+-----------------------------------------------------------+
            | excluded_role_ids             | `None`, `tuple` of `int`                                  |
            +-------------------------------+-----------------------------------------------------------+
            | name                          | `str`                                                     |
            +-------------------------------+-----------------------------------------------------------+
            | trigger_metadata              | ``AutoModerationRuleTriggerMetadataBase``                 |
            +-------------------------------+-----------------------------------------------------------+
            | trigger_type                  | ``AutoModerationRuleTriggerType``                         |
            +-------------------------------+-----------------------------------------------------------+
        """
        old_attributes = {}
        
        # actions
        actions = parse_actions(data)
        if self.actions != actions:
            old_attributes['actions'] = self.actions
            self.actions = actions
        
        # creator_id |Internal field & cannot change
        
        # enabled
        enabled = parse_enabled(data)
        if self.enabled != enabled:
            old_attributes['enabled'] = self.enabled
            self.enabled = enabled
        
        # event_type
        event_type = parse_event_type(data)
        if self.event_type != event_type:
            old_attributes['event_type'] = self.event_type
            self.event_type = event_type
        
        # excluded_channel_ids
        excluded_channel_ids = parse_excluded_channel_ids(data)
        if self.excluded_channel_ids != excluded_channel_ids:
            old_attributes['excluded_channel_ids'] = self.excluded_channel_ids
            self.excluded_channel_ids = excluded_channel_ids
        
        # excluded_role_ids
        excluded_role_ids = parse_excluded_role_ids(data)
        if self.excluded_role_ids != excluded_role_ids:
            old_attributes['excluded_role_ids'] = self.excluded_role_ids
            self.excluded_role_ids = excluded_role_ids
        
        # guild_id | Internal field & cannot change
        
        # name
        name = parse_name(data)
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        # id | Already set & cannot change
        
        # trigger_type
        trigger_type = parse_trigger_type(data)
        if self.trigger_type is not trigger_type:
            old_attributes['trigger_type'] = self.trigger_type
            self.trigger_type = trigger_type
        
        # trigger_metadata
        trigger_metadata = parse_trigger_metadata(data, trigger_type)
        if self.trigger_metadata != trigger_metadata:
            old_attributes['trigger_metadata'] = self.trigger_metadata
            self.trigger_metadata = trigger_metadata
        
        return old_attributes
    
    
    def __eq__(self, other):
        """Returns whether the two auto moderation rules are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # id
        self_id = self.id
        other_id = other.id
        if self_id and other_id:
            return self_id == other_id
        
        # actions
        if self.actions != other.actions:
            return False
        
        # creator_id
        # Internal field
        
        # enabled
        if self.enabled != other.enabled:
            return False
        
        # event_type
        if self.event_type is not other.event_type:
            return False
        
        # excluded_channel_ids
        if self.excluded_channel_ids != other.excluded_channel_ids:
            return False
        
        # excluded_role_ids
        if self.excluded_role_ids != other.excluded_role_ids:
            return False
        
        # guild_id
        # Internal field
        
        # name
        if self.name != other.name:
            return False
        
        # trigger_metadata
        if self.trigger_metadata != other.trigger_metadata:
            return False
        
        # trigger_type
        if self.trigger_type is not other.trigger_type:
            return False
        
        return True
    
    
    def __ne__(self, other):
        """Returns whether the two auto moderation rules are not equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # id
        self_id = self.id
        other_id = other.id
        if self_id and other_id:
            return self_id != other_id
        
        # actions
        if self.actions != other.actions:
            return True
        
        # creator_id
        # Internal field
        
        # enabled
        if self.enabled != other.enabled:
            return True
        
        # event_type
        if self.event_type is not other.event_type:
            return True
        
        # excluded_channel_ids
        if self.excluded_channel_ids != other.excluded_channel_ids:
            return True
        
        # excluded_role_ids
        if self.excluded_role_ids != other.excluded_role_ids:
            return True
        
        # guild_id
        # Internal field
        
        # name
        if self.name != other.name:
            return True
        
        # trigger_metadata
        if self.trigger_metadata != other.trigger_metadata:
            return True
        
        # trigger_type
        if self.trigger_type is not other.trigger_type:
            return True
        
        return False
    
    
    def __hash__(self):
        """Returns the auto moderation rule's hash value."""
        
        # id
        self_id = self.id
        if self_id:
            return self_id
        
        hash_value = 0
        
        # actions
        actions = self.actions
        if (actions is not None):
            hash_value ^= len(actions)
            
            for action in actions:
                hash_value ^= hash(action)
        
        # creator_id | Internal field
        
        # enabled
        hash_value ^= self.enabled << 4
        
        # event_type
        hash_value ^= self.event_type.value << 8
        
        # excluded_channel_ids
        excluded_channel_ids = self.excluded_channel_ids
        if (excluded_channel_ids is not None):
            hash_value ^= len(excluded_channel_ids) << 12
            
            for excluded_channel_id in excluded_channel_ids:
                hash_value ^= excluded_channel_id
        
        # excluded_role_ids
        excluded_role_ids = self.excluded_role_ids
        if (excluded_role_ids is not None):
            hash_value ^= len(excluded_role_ids) << 16
            
            for excluded_role_id in excluded_role_ids:
                hash_value ^= excluded_role_id
        
        # guild_id | Internal field
        
        # name
        hash_value ^= hash(self.name)
                
        # trigger_metadata1
        trigger_metadata = self.trigger_metadata
        if (trigger_metadata is not None):
            hash_value ^= hash(trigger_metadata)
        
        # trigger_type
        hash_value ^= self.trigger_type.value << 20
        
        return hash_value
    
    
    def __repr__(self):
        """Returns the auto moderation rule's representation"""
        repr_parts = ['<', self.__class__.__name__]
        
        # system fields: `.id`, `.guild_id`, `.creator_id`
        
        # id
        id_ = self.id
        if id_ == 0:
            repr_parts.append(' partial')
        
        else:
            repr_parts.append(' id = ')
            repr_parts.append(repr(id_))
            
            repr_parts.append(', guild_id = ')
            repr_parts.append(repr(self.guild_id))
            
            repr_parts.append(', creator_id = ')
            repr_parts.append(repr(self.creator_id))
        
        # Information `.name`, `.trigger_type`
        
        # name
        repr_parts.append(', name = ')
        repr_parts.append(repr(self.name))
        
        # trigger_type
        trigger_type = self.trigger_type
        repr_parts.append(', trigger_type = ')
        repr_parts.append(repr(trigger_type.name))
        repr_parts.append(' ~ ')
        repr_parts.append(repr(trigger_type.value))
        
        # Additional: `.actions`, `.enabled`, `event_type`, `.excluded_channel_ids`, `.excluded_role_ids`, 
        # `.trigger_metadata`
        
        trigger_metadata = self.trigger_metadata
        if (trigger_metadata is not None):
            repr_parts.append(', trigger_metadata = ')
            repr_parts.append(repr(trigger_metadata))
        
        repr_parts.append(', actions = [')
        actions = self.actions
        if (actions is not None):
            limit = len(actions)
            index = 0
            
            while True:
                action = actions[index]
                repr_parts.append(repr(action))
                
                index += 1
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
        
        repr_parts.append(']')
        
        # enabled
        enabled = self.enabled
        if not enabled:
            repr_parts.append(', enabled = ')
            repr_parts.append(repr(enabled))
        
        event_type = self.event_type
        if (
            (event_type is not AutoModerationEventType.none) and
            (event_type is not AutoModerationEventType.message_send)
        ):
            repr_parts.append(', event_type = ')
            event_type.append(repr(event_type.name))
            event_type.append('~')
            event_type.append(repr(event_type.value))
        
        # excluded_channel_ids
        excluded_channel_ids = self.excluded_channel_ids
        if (excluded_channel_ids is not None):
            repr_parts.append(', excluded_channel_ids = [')
            
            limit = len(excluded_channel_ids)
            index = 0
            
            while True:
                excluded_channel_id = excluded_channel_ids[index]
                repr_parts.append(repr(excluded_channel_id))
                
                index += 1
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
        
        # excluded_role_ids
        excluded_role_ids = self.excluded_role_ids
        if (excluded_role_ids is not None):
            repr_parts.append(', excluded_role_ids = [')
            
            limit = len(excluded_role_ids)
            index = 0
            
            while True:
                excluded_role_id = excluded_role_ids[index]
                repr_parts.append(repr(excluded_role_id))
                
                index += 1
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
        
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    def copy(self):
        """
        Copies the auto moderation rule returning a new partial one.
        
        Returns
        -------
        new : ``AutoModerationRule``
        """
        new = object.__new__(type(self))
        
        # id | Internal field
        new.id = 0
        
        # actions
        actions = self.actions
        if (actions is not None):
            actions = tuple(action.copy() for action in actions)
        new.actions = actions
        
        # creator_id | Internal field
        new.creator_id = 0
        
        # enabled
        new.enabled = self.enabled
        
        # event_type
        new.event_type = self.event_type
        
        # excluded_channel_ids
        excluded_channel_ids = self.excluded_channel_ids
        if (excluded_channel_ids is not None):
            excluded_channel_ids = (*excluded_channel_ids,)
        new.excluded_channel_ids = excluded_channel_ids
        
        # excluded_role_ids
        excluded_role_ids = self.excluded_role_ids
        if (excluded_role_ids is not None):
            excluded_role_ids = (*excluded_role_ids,)
        new.excluded_role_ids = excluded_role_ids
        
        # guild_id
        # Internal field
        new.guild_id = 0
        
        # name
        new.name = self.name
        
        # trigger_metadata
        new.trigger_metadata = self.trigger_metadata.copy()
        
        # trigger_type
        new.trigger_type = self.trigger_type
        
        return new
    
    
    def copy_with(
        self,
        *,
        actions = ...,
        enabled = ...,
        event_type = ...,
        excluded_channel_ids = ...,
        excluded_role_ids = ...,
        name = ...,
        trigger_type=...,
        **keyword_parameters,
    ):
        """
        Copies the auto moderation rule with the given attributes replaced.

        Parameters
        ----------
        actions : `None`, ``AutoModerationAction``, `iterable` of ``AutoModerationAction``, Optional (keyword only)
             Actions which will execute when the rule is triggered.
         
        enabled : `bool` , Optional (Keyword only)
            Whether the rule is enabled.
        
        event_type : `None`, `int`, ``AutoModerationEventType``, Optional (Keyword only)
            For which events is the rule applied.
        
        excluded_channel_ids : `None`, `int`, ``Channel``, `iterable` of (`int`, ``Channel``), Optional (Keyword only)
            Excluded channels from the rule.
        
        excluded_role_ids : `None`, `int`, ``Role``, `iterable` of (`int`, ``Role``), Optional (Keyword only)
            Excluded roles from the rule.
        
        name : `str`, Optional (Keyword only)
            The rule's name.
        
        trigger_type : ``AutoModerationRuleTriggerType``, `int`, Optional (Keyword only)
            Auto moderation trigger type.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters defining how the rule is triggered.
        
        Other Parameters
        ----------------
        excluded_keywords : `None`, `str`, `iterable` of `str`, Optional (Keyword only)
            Excluded keywords from preset filter.
        
        keyword_presets : `None`, `int`, ``AutoModerationKeywordPresetType``, \
                `iterable` of (`int`, ``AutoModerationKeywordPresetType``), Optional (Keyword only)
            Keyword preset defined by Discord which will be searched for in content.
            
        keywords : `None`, `str`, `iterable` of `str`, Optional (Keyword only)
            Substrings which will be searched for in content.
        
        mention_limit : `None`, `int`, Optional (Keyword only)
            The amount of mentions in a message after the rule is triggered.
        
        regex_patterns : `None`, `tuple` of `str`, Optional (Keyword only)
            Regular expression patterns which are matched against content.
        
        Returns
        -------
        new : ``AutoModerationRule``
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # actions
        if actions is ...:
            actions = self.actions
            if (actions is not None):
                actions = tuple(action.copy() for action in actions)
        else:
            actions = validate_actions(actions)
        
        # enabled
        if enabled is ...:
            enabled = self.enabled
        else:
            enabled = validate_enabled(enabled)
        
        # event_type
        if event_type is ...:
            event_type = self.event_type
        else:
            event_type = validate_event_type(event_type)
        
        # excluded_channel_ids
        if excluded_channel_ids is ...:
            excluded_channel_ids = self.excluded_channel_ids
            if (excluded_channel_ids is not None):
                excluded_channel_ids = (*excluded_channel_ids,)
        else:
            excluded_channel_ids = validate_excluded_channel_ids(excluded_channel_ids)
        
        # excluded_role_ids
        if excluded_role_ids is ...:
            excluded_role_ids = self.excluded_role_ids
            if (excluded_role_ids is not None):
                excluded_role_ids = (*excluded_role_ids,)
        else:
            excluded_role_ids = validate_excluded_role_ids(excluded_role_ids)
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # trigger_type
        if trigger_type is ...:
            if keyword_parameters:
                trigger_type = guess_rule_trigger_type_from_keyword_parameters(
                    AutoModerationRuleTriggerType.none, keyword_parameters)
            else:
                trigger_type = self.trigger_type
        else:
            trigger_type = validate_trigger_type(trigger_type)
        
        # **keyword_parameters
        if trigger_type is self.trigger_type:
            trigger_metadata = self.trigger_metadata.copy_with(**keyword_parameters)
        else:
            trigger_metadata = trigger_type.metadata_type(**keyword_parameters)
        
        new = object.__new__(type(self))
        
        new.id = 0
        new.actions = actions
        new.creator_id = 0
        new.enabled = enabled
        new.event_type = event_type
        new.excluded_channel_ids = excluded_channel_ids
        new.excluded_role_ids = excluded_role_ids
        new.guild_id = 0
        new.name = name
        new.trigger_metadata = trigger_metadata
        new.trigger_type = trigger_type
        
        return new
    
    
    @classmethod
    def _create_empty(cls, rule_id):
        """
        Creates an auto moderation rule with it's attributes set as their default values.
        
        Parameters
        ----------
        rule_id : `int`
            The auto moderation rule's identifier.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.id = rule_id
        self.actions = None
        self.creator_id = 0
        self.enabled = True
        self.event_type = AutoModerationEventType.none
        self.excluded_channel_ids = None
        self.excluded_role_ids = None
        self.guild_id = 0
        self.name = ''
        self.trigger_metadata = AutoModerationRuleTriggerMetadataBase()
        self.trigger_type = AutoModerationRuleTriggerType.none
        return self
    
    
    @classmethod
    def precreate(cls, rule_id, **keyword_parameters):
        """
        Precreates the auto moderation rule by creating a new one if not yet exists of the given identifier.
        
        Parameters
        ----------
        rule_id : `int`
            The auto moderation rule's identifier.
        
        *keyword_parameters : Keyword parameters
            Keyword parameters defining how should the rule's attributes be set.
        
        Other Parameters
        ----------------
        actions : `None`, ``AutoModerationAction``, `iterable` of ``AutoModerationAction``, Optional (keyword only)
             Actions which will execute when the rule is triggered.
    
        creator_id : `int`, ``ClientUserBase``, Optional (Keyword only)
            The user who created the rule.
            
        enabled : `bool` , Optional (Keyword only)
            Whether the rule is enabled.
        
        event_type : `None`, `int`, ``AutoModerationEventType``, Optional (Keyword only)
            For which events is the rule applied.
        
        excluded_channel_ids : `None`, `int`, ``Channel``, `iterable` of (`int`, ``Channel``), Optional (Keyword only)
            Excluded channels from the rule.
        
        excluded_role_ids : `None`, `int`, ``Role``, `iterable` of (`int`, ``Role``), Optional (Keyword only)
            Excluded roles from the rule.
        
        guild_id : `int`, ``Guild``, Optional (Keyword only)
            The guild's identifier where the rule is.
        
        name : `str`, Optional (Keyword only)
            The rule's name.
        
        trigger_type : ``AutoModerationRuleTriggerType``, `int`, Optional (Keyword only)
            Auto moderation trigger type.
        
        excluded_keywords : `None`, `str`, `iterable` of `str`, Optional (Keyword only)
            Excluded keywords from preset filter.
        
        keyword_presets : `None`, `int`, ``AutoModerationKeywordPresetType``, \
                `iterable` of (`int`, ``AutoModerationKeywordPresetType``), Optional (Keyword only)
            Keyword preset defined by Discord which will be searched for in content.
            
        keywords : `None`, `str`, `iterable` of `str`, Optional (Keyword only)
            Substrings which will be searched for in content.
        
        mention_limit : `None`, `int`, Optional (Keyword only)
            The amount of mentions in a message after the rule is triggered.
        
        regex_patterns : `None`, `tuple` of `str`, Optional (Keyword only)
            Regular expression patterns which are matched against content.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
            - Extra or unused parameters given.
        ValueError
            - If a parameter's value is incorrect.
        """
        rule_id = validate_id(rule_id)
        
        if keyword_parameters:
            processed = []
            
            # trigger_type
            try:
                trigger_type = keyword_parameters.pop('trigger_type')
            except KeyError:
                trigger_type = AutoModerationRuleTriggerType.none
            else:
                trigger_type = validate_trigger_type(trigger_type)
            
            extra = process_precreate_parameters(keyword_parameters, PRECREATE_FIELDS, processed)
            
            # trigger_metadata
            if (extra is None):
                trigger_metadata = trigger_type.metadata_type()
            else:
                trigger_type = guess_rule_trigger_type_from_keyword_parameters(trigger_type, extra)
                trigger_metadata = trigger_type.metadata_type(**extra)
            
            if (trigger_type is not AutoModerationRuleTriggerType.none):
                processed.append(('trigger_type', trigger_type))
                processed.append(('trigger_metadata', trigger_metadata))
        
        else:
            processed = None
        
        try:
            self = AUTO_MODERATION_RULES[rule_id]
        except KeyError:
            self = cls._create_empty(rule_id)
            AUTO_MODERATION_RULES[rule_id] = self
        
        
        if (processed is not None):
            for item in processed:
                setattr(self, *item)
        
        return self
    
    
    @property
    def partial(self):
        """
        Returns whether the auto moderation rule is partial.
        
        Returns
        -------
        partial : `bool
        """
        return (not self.id)
    
    
    def iter_actions(self):
        """
        Iterates over the actions of the auto moderation rule.
        
        This method is an iterable generator.
        
        Yields
        ------
        action : ``AutoModerationAction``
        """
        actions = self.actions
        if (actions is not None):
            yield from actions
    
    
    @property
    def creator(self):
        """
        Returns who created the auto moderation rule.
        
        Returns
        -------
        creator : ``ClientUserBase``
        """
        creator_id = self.creator_id
        if creator_id:
            creator = create_partial_user_from_id(creator_id)
        else:
            creator = ZEROUSER
        
        return creator
    
    
    @property
    def guild(self):
        """
        Returns the auto moderation rule's guild. If the guild is not cached returns `None`
        
        Returns
        -------
        guild : `None`, ``Guild``
        """
        guild_id = self.guild_id
        if guild_id:
            return GUILDS.get(guild_id, None)
    
    
    def iter_excluded_channel_ids(self):
        """
        Iterates over the excluded channel identifiers from the rule.
        
        This method is an iterable generator.
        
        Yields
        ------
        excluded_channel_id : `int`
        """
        excluded_channel_ids = self.excluded_channel_ids
        if (excluded_channel_ids is not None):
            yield from excluded_channel_ids
    
    
    @property
    def excluded_channels(self):
        """
        Returns the excluded channels from the rule.
        
        Returns
        -------
        excluded_channels : `None`, `tuple` of ``Channel``
        """
        excluded_channel_ids = self.excluded_channel_ids
        if (excluded_channel_ids is None):
            excluded_channels = None
        
        else:
            guild_id = self.guild_id
            excluded_channels = tuple(
                create_partial_channel_from_id(excluded_channel_id, ChannelType.unknown, guild_id)
                for excluded_channel_id in excluded_channel_ids
            )
        
        return excluded_channels
    
    
    def iter_excluded_channels(self):
        """
        Iterates over the excluded channels from the rule.
        
        This method is an iterable generator.
        
        Yields
        ------
        excluded_channel : ``Channel``
        """
        excluded_channel_ids = self.excluded_channel_ids
        if (excluded_channel_ids is not None):
            guild_id = self.guild_id
            
            for excluded_channel_id in excluded_channel_ids:
                yield create_partial_channel_from_id(excluded_channel_id, ChannelType.unknown, guild_id)
    
    
    def iter_excluded_role_ids(self):
        """
        Iterates over the excluded role identifiers from the rule.
        
        This method is an iterable generator.
        
        Yields
        ------
        excluded_role_id : `int`
        """
        excluded_role_ids = self.excluded_role_ids
        if (excluded_role_ids is not None):
            yield from excluded_role_ids
    
    
    @property
    def excluded_roles(self):
        """
        Returns the excluded roles from the rule.
        
        Returns
        -------
        excluded_roles : `None`, `tuple` of ``Role``
        """
        excluded_role_ids = self.excluded_role_ids
        if (excluded_role_ids is None):
            excluded_roles = None
        
        else:
            excluded_roles = tuple(
                create_partial_role_from_id(excluded_role_id) for excluded_role_id in excluded_role_ids
            )
        
        return excluded_roles
    
    
    def iter_excluded_roles(self):
        """
        Iterates over the excluded roles from the rule.
        
        This method is an iterable generator.
        
        Yields
        ------
        excluded_role : ``Role``
        """
        excluded_role_ids = self.excluded_role_ids
        if (excluded_role_ids is not None):
            for excluded_role_id in excluded_role_ids:
                yield create_partial_role_from_id(excluded_role_id)
