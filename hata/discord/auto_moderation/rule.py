__all__ = ('AutoModerationRule',)

from ..bases import DiscordEntity
from ..channel import Channel, create_partial_channel_from_id
from ..core import AUTO_MODERATION_RULES
from ..preconverters import preconvert_preinstanced_type, preconvert_str
from ..role import Role, create_partial_role_from_id
from ..user import ZEROUSER, create_partial_user_from_id

from .action import AutoModerationAction
from .preinstanced import AutoModerationEventType, AutoModerationRuleTriggerType


def _validate_actions(actions):
    """
    Validates the given `actions` parameter.
    
    Parameters
    ----------
    actions : `None`, (`list`, `set`, `tuple`) of ``AutoModerationAction``
        Actions which will execute when the rule is triggered.
    
    Returns
    -------
    processed_actions : `None`, `tuple` of ``AutoModerationAction``
    
    Raises
    ------
    TypeError
        - If `actions`'s type is incorrect.
        - If an action's type is incorrect.
    """
    if actions is None:
        processed_actions = None
    
    elif isinstance(actions, AutoModerationAction):
        processed_actions = (actions, )
    
    else:
        iterator = getattr(type(actions), '__iter__', None)
        if iterator is None:
            raise TypeError(
                f'`actions` can be `None`, `{AutoModerationAction.__name__}`, '
                f'`iterable` of `{AutoModerationAction.__name__}`, '
                f'got {actions.__class__.__name__}; {actions!r}.'
            )
        
        processed_actions = None
        
        for action in actions:
            if not isinstance(action, AutoModerationAction):
                raise TypeError(
                    f'`actions` can can contain `{AutoModerationAction.__name__}` elements, '
                    f'got {action.__class__.__name__}; {action!r}; actions={actions!r}.'
                )
            
            if processed_actions is None:
                processed_actions = set()
            
            processed_actions.add(action)
    
    if (processed_actions is not None):
        processed_actions = tuple(sorted(processed_actions))
    
    return processed_actions


def _validate_enabled(enabled):
    """
    Validates the given `enabled` parameter.
    
    Parameters
    ----------
    enabled : `bool`
        Whether the rule is enabled.
    
    Returns
    -------
    enabled : `bool`
    
    Raises
    ------
    TypeError
        - If `enabled`'s type is incorrect.
    """
    if not isinstance(enabled, bool):
        raise TypeError(
            f'`enabled` can be `bool`, got {enabled.__class__.__name__}; {enabled!r}.'
        )
    
    return enabled


def _validate_event_type(event_type):
    """
    Validates the given `event_type` parameter.
    
    Parameters
    ----------
    event_type : `None`, `int`, ``AutoModerationEventType``
        For which events is the rule applied.
    
    Returns
    -------
    event_type : ``AutoModerationEventType``
    
    Raises
    ------
    TypeError
        - If `event_type`'s type is incorrect.
    """
    if event_type is None:
        event_type = AutoModerationEventType.message_send
    
    else:
        event_type = preconvert_preinstanced_type(event_type, 'event_type', AutoModerationEventType)
    
    return event_type


def _validate_excluded_channel_ids(excluded_channels):
    """
    Validates the given `excluded_channels` parameter.
    
    Parameters
    ----------
    excluded_channels : `None`, `int`, `Channel`, `iterable` of (`int`, ``Channel``)
        Excluded channels from the rule.
    
    Returns
    -------
    excluded_channel_ids : `None`, `tuple` of `int`
    
    Raises
    ------
    TypeError
        - If `excluded_channels`'s type is incorrect.
        - If an excluded channel's type is incorrect.
    """
    if excluded_channels is None:
        excluded_channel_ids = None
    
    elif isinstance(excluded_channels, int):
        excluded_channel_ids = (excluded_channels, )
    
    elif isinstance(excluded_channels, Channel):
        excluded_channel_ids = (excluded_channels.id, )
    
    else:
        iterator = getattr(type(excluded_channels), '__iter__', None)
        if iterator is None:
            raise TypeError(
                f'`excluded_channels` can be `None`, `int`, `{Channel.__name__}`, '
                f'`iterable` of (`int`, `{Channel.__name__}`), '
                f'got {excluded_channels.__class__.__name__}; {excluded_channels!r}.'
            )
        
        excluded_channel_ids = None
        
        for excluded_channel in excluded_channels:
            if isinstance(excluded_channel, Channel):
                excluded_channel_id = excluded_channel.id
            
            elif isinstance(excluded_channel, int):
                excluded_channel_id = excluded_channel
            
            else:
                raise TypeError(
                    f'`excluded_channels` can can contain (`int`, `{Channel.__name__}`) elements, '
                    f'got {excluded_channel.__class__.__name__}; {excluded_channel!r}; '
                    f'actions={excluded_channels!r}.'
                )
            
            if excluded_channel_ids is None:
                excluded_channel_ids = set()
            
            excluded_channel_ids.add(excluded_channel_id)
        
        if (excluded_channel_ids is not None):
            excluded_channel_ids = tuple(sorted(excluded_channel_ids))
    
    return excluded_channel_ids


def _validate_excluded_role_ids(excluded_roles):
    """
    Validates the given `excluded_roles` parameter.
    
    Parameters
    ----------
    excluded_roles : `None`, `int`, ``Role``, `iterable` of (`int`, ``Role``)
        Excluded roles from the rule.
    
    Returns
    -------
    excluded_role_ids : `None`, `tuple` of `int`
    
    Raises
    ------
    TypeError
        - If `excluded_roles`'s type is incorrect.
        - If an excluded role's type is incorrect.
    """
    if excluded_roles is None:
        excluded_role_ids = None
    
    elif isinstance(excluded_roles, int):
        excluded_role_ids = (excluded_roles, )
    
    elif isinstance(excluded_roles, Role):
        excluded_role_ids = (excluded_roles.id, )
    
    else:
        iterator = getattr(type(excluded_roles), '__iter__', None)
        if iterator is None:
            raise TypeError(
                f'`excluded_roles` can be `None`, `int`, `{Role.__name__}`, '
                f'`iterable` of (`int`, `{Role.__name__}`), '
                f'got {excluded_roles.__class__.__name__}; {excluded_roles!r}.'
            )
        
        excluded_role_ids = None
        
        for excluded_role in excluded_roles:
            if isinstance(excluded_role, Role):
                excluded_role_id = excluded_role.id
            
            elif isinstance(excluded_role, int):
                excluded_role_id = excluded_role
            
            else:
                raise TypeError(
                    f'`excluded_roles` can can contain (`int`, `{Role.__name__}`) elements, '
                    f'got {excluded_role.__class__.__name__}; {excluded_role!r}; '
                    f'actions={excluded_roles!r}.'
                )
            
            if excluded_role_ids is None:
                excluded_role_ids = set()
            
            excluded_role_ids.add(excluded_role_id)
        
        if (excluded_role_ids is not None):
            excluded_role_ids = tuple(sorted(excluded_role_ids))
    
    return excluded_role_ids


def _validate_name(name):
    """
    Validates the given `name` parameter.
    
    Parameters
    ----------
    name : `str`
        The rule's name.
    
    Returns
    -------
    name : `str`
    
    Raises
    ------
    TypeError
        - If `enabled`'s type is incorrect.
    ValueError
        - If `name`'s length is out of the expected range.
    """
    return preconvert_str(name, 'name', 1, 2048)


def _validate_trigger_type_with_metadata_options(
    trigger_type, excluded_keywords, keyword_presets, keywords, mention_limit
):
    """
    Validates the given `trigger_type` with the `keyword_presets`, `keywords` options. If any option is given, the
    `trigger_type` will default towards it. On any mismatch exception is raised.
    
    Parameters
    ----------
    trigger_type : `Ellipsis`, `int`, ``AutoModerationRuleTriggerType``
        Auto moderation trigger type.
    
    keyword_presets : `Ellipsis`, `None`, `int`, ``AutoModerationKeywordPresetType``, \
            `iterable` of (`int`, ``AutoModerationKeywordPresetType``)
        Keyword preset defined by Discord which will be searched for in content.
    
    excluded_keywords : `Ellipsis`, `None`, `str`, `iterable` of `str`
        Excluded keywords from preset filter.

    keywords : `Ellipsis`, `None`, `str`, `iterable` of `str`
        Substrings which will be searched for in content.
    
    mention_limit : `Ellipsis`, `None`, `int`
        The amount of mentions in a message after the rule is triggered.
    
    Returns
    -------
    trigger_metadata : `None`, ``AutoModerationRuleTriggerMetadata``
        Trigger type specific metadata if applicable.
    trigger_type : ``AutoModerationRuleTriggerType``
        The final processed trigger type.
    
    Raises
    ------
    TypeError
        - If a parameter's type is incorrect.
        - If there are multiple mutually exclusive options.
        - If trigger type not detectable.
        - If multiple trigger types detected.
    ValueError
        - If a parameter's value is incorrect.
    """
    if (trigger_type is not ...):
        trigger_type = preconvert_preinstanced_type(trigger_type, 'trigger_type', AutoModerationRuleTriggerType)
    
    if (keyword_presets is not ...) + (keywords is not ...) + (mention_limit is not ...)> 1:
        raise TypeError(
            f'`keyword_presets` and `keywords` parameters are mutually exclusive, got '
            f'keyword_presets={keyword_presets!r}; keywords={keywords!r}.'
        )
    
    if (keyword_presets is not ...):
        if (excluded_keywords is ...):
            excluded_keywords = None
        
        probable_trigger_type = AutoModerationRuleTriggerType.keyword_preset
        metadata_parameters = (keyword_presets, excluded_keywords, )
    
    elif (excluded_keywords is not ...):
        raise TypeError(
            f'`excluded_keywords` is only meaningful with `keyword_presets` parameter, '
            f'got excluded_keywords={excluded_keywords!r}.'
        )
    
    elif (keywords is not ...):
        probable_trigger_type = AutoModerationRuleTriggerType.keyword
        metadata_parameters = (keywords, )
    
    elif (mention_limit is not ...):
        probable_trigger_type = AutoModerationRuleTriggerType.mention_spam
        metadata_parameters = (mention_limit, )
        
    else:
        probable_trigger_type = None
        metadata_parameters = ()
    
    
    if (trigger_type is ...):
        if (probable_trigger_type is None):
            raise TypeError(
                f'`trigger_type` is not given or is given as `None`, and cannot be detected from `keyword_presets` '
                'or from `keywords` parameters.'
            )
        
        trigger_type = probable_trigger_type
    
    else:
        if (probable_trigger_type is not None):
            if (trigger_type is not probable_trigger_type):
                if (keyword_presets is not ...):
                    received_parameter_name = 'keyword_presets'
                    received_parameter_value = keyword_presets
                
                elif (keywords is not ...):
                    received_parameter_name = 'keywords'
                    received_parameter_value = keywords
                
                else:
                    received_parameter_name = 'mention_limit'
                    received_parameter_value = mention_limit
                
                raise TypeError(
                    f'Both `trigger_type` and `{received_parameter_name}` parameters refer to a different '
                    f'trigger type, got trigger_type={trigger_type!r}, '
                    f'{received_parameter_name}={received_parameter_value!r}.'
                )
    
    trigger_metadata_type = trigger_type.metadata_type
    if (trigger_metadata_type is None):
        trigger_metadata = None
    
    else:
        trigger_metadata = trigger_metadata_type(*metadata_parameters)
    
    return trigger_metadata, trigger_type


class AutoModerationRule(DiscordEntity, immortal=True):
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
        The guild's identifier where the role is. Defaults to `0`.
    
    name : `str`
        The rule's name.
    
    trigger_metadata : `None`, ``AutoModerationRuleTriggerMetadata``
        Trigger type specific metadata if applicable.
    
    trigger_type : ``AutoModerationRuleTriggerType``
        Characterizes the type of content which can trigger the rule.
    """
    __slots__ = (
        'actions', 'creator_id', 'enabled', 'event_type', 'excluded_channel_ids', 'excluded_role_ids', 'guild_id',
        'name', 'trigger_metadata', 'trigger_type'
    )
    
    
    def __new__(
        cls, name, actions, trigger_type=..., *, enabled=True, event_type=None, excluded_channels=None,
        excluded_keywords=..., excluded_roles=None, keyword_presets=..., keywords=..., mention_limit=...
    ):
        """
        Creates a new auto moderation rule with the given parameters.
        
        Parameters
        ----------
        name : `str`
            The rule's name.
        
        actions : `None`, ``AutoModerationAction``, `iterable` of ``AutoModerationAction``
             Actions which will execute when the rule is triggered.
        
        trigger_type : ``AutoModerationRuleTriggerType``, `int`, Optional
            Auto moderation trigger type.
            
            By passing `keyword_presets` parameter you can define the trigger type as 
            `AutoModerationRuleTriggerType.keyword_preset`, or by passing the `keywords` you can define it as 
            `AutoModerationRuleTriggerType.keyword`.
            
            > `keyword_preset` triggers also accept an additional `excluded_keywords` parameter.
        
        enabled : `bool` = `True`, Optional (Keyword only)
            Whether the rule is enabled.
        
        event_type : `None`, `int`, ``AutoModerationEventType`` = `AutoModerationEventType.message_send` \
                , Optional (Keyword only)
            For which events is the rule applied.
        
        excluded_channels : `None`, `int`, ``Channel``, `iterable` of (`int`, ``Channel``) = `None`, \
                Optional (Keyword only)
            Excluded channels from the rule.
        
        excluded_keywords : `None`, `str`, `iterable` of `str`, Optional (Keyword only)
            Excluded keywords from preset filter.
            
            > Only meaningful with the `keyword_presets` parameter.
        
        excluded_roles : `None`, `int`, ``Role``, `iterable` of (`int`, ``Role``) = `None`, Optional (Keyword only)
            Excluded roles from the rule.
        
        keyword_presets : `None`, `int`, ``AutoModerationKeywordPresetType``, \
                `iterable` of (`int`, ``AutoModerationKeywordPresetType``), Optional (Keyword only)
            Keyword preset defined by Discord which will be searched for in content.
            
            > Mutually exclusive with the `keywords` and `mention_limit` parameters.
        
        keywords : `None`, `str`, `iterable` of `str`, Optional (Keyword only)
            Substrings which will be searched for in content.
            
            > Mutually exclusive with the `keyword_presets` and `mention_limit` parameters.
        
        mention_limit : `None`, `int`, Optional (Keyword only)
            The amount of mentions in a message after the rule is triggered.
            
            > Mutually exclusive with the `keyword_presets` and `keywords` parameters.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # actions
        actions = _validate_actions(actions)
        
        # enabled
        enabled = _validate_enabled(enabled)
        
        # event_type
        event_type = _validate_event_type(event_type)
        
        # excluded_channel_ids
        excluded_channel_ids = _validate_excluded_channel_ids(excluded_channels)
        
        # excluded_role_ids
        excluded_role_ids = _validate_excluded_role_ids(excluded_roles)
        
        # name
        name = _validate_name(name)
        
        # trigger_type & keywords & keyword_presets
        trigger_metadata, trigger_type = _validate_trigger_type_with_metadata_options(
            trigger_type, excluded_keywords, keyword_presets, keywords, mention_limit
        )
        
        self = object.__new__(cls)
        self.id = 0
        self.actions = actions
        self.creator_id = 0
        self.enabled = enabled
        self.event_type = event_type
        self.excluded_channel_ids = excluded_channel_ids
        self.excluded_role_ids = excluded_role_ids
        self.guild_id = 0
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
        data : `dict` of (`str`, `Any`) items
            Received auto moderation rule data.
        
        Returns
        -------
        self : ``AutoModerationRule``
            The created auto moderation rule.
        """
        auto_moderation_rule_id = int(data['id'])
        
        try:
            self = AUTO_MODERATION_RULES[auto_moderation_rule_id]
        except KeyError:
            self = object.__new__(cls)
            
            self.id = auto_moderation_rule_id
            
            # creator_id
            creator_id = data.get('creator_id', None)
            if creator_id is None:
                creator_id = 0
            else:
                creator_id = int(creator_id)
            self.creator_id = creator_id
            
            # guild_id
            guild_id = data.get('guild_id', None)
            if (guild_id is None):
                guild_id = 0
            else:
                guild_id = int(guild_id)
            self.guild_id = guild_id
            
            AUTO_MODERATION_RULES[auto_moderation_rule_id] = self
        
        self._update_attributes(data)
        return self
    
    
    def to_data(self):
        """
        Converts the auto moderation rule to a json serializable object.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        data = {}
        
        # id
        # Internal field
        
        # actions
        data['actions'] = [auto_moderation_action.to_data() for auto_moderation_action in self.iter_actions()]
        
        # creator_id
        # Internal field
        
        # enabled
        data['enabled'] = self.enabled
        
        # event_type
        data['event_type'] = self.event_type.value
        
        # excluded_channel_ids
        data['exempt_channels'] = [*self.iter_excluded_channel_ids()]
        
        # excluded_role_ids
        data['exempt_roles'] = [*self.iter_excluded_role_ids()]
        
        # guild_id
        # Internal field
        
        # name
        data['name'] = self.name
        
        # trigger_metadata
        trigger_metadata = self.trigger_metadata
        if (trigger_metadata is None):
            trigger_metadata_data = {}
        else:
            trigger_metadata_data = trigger_metadata.to_data()
        data['trigger_metadata'] = trigger_metadata_data
        
        # trigger_type
        data['trigger_type'] = self.trigger_type.value
        
        return data
    
    
    def _update_attributes(self, data):
        """
        Updates the auto moderation rule with overwriting it's old attributes.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received guild profile data.
        """
        # id
        # Already set & cannot change
        
        # actions
        action_array = data['actions']
        if action_array:
            actions = tuple(
                AutoModerationAction.from_data(auto_moderation_action_data)
                for auto_moderation_action_data in action_array
            )
        else:
            actions = None
        
        self.actions = actions
        
        # creator_id
        # Internal field & cannot change
        
        # enabled
        self.enabled = data['enabled']
        
        # event_type
        self.event_type = AutoModerationEventType.get(data['event_type'])
        
        # excluded_channel_ids
        excluded_channel_id_array = data['exempt_channels']
        if excluded_channel_id_array:
            excluded_channel_ids = tuple(sorted(int(channel_id) for channel_id in excluded_channel_id_array))
        else:
            excluded_channel_ids = None
        self.excluded_channel_ids = excluded_channel_ids
        
        # excluded_role_ids
        excluded_role_id_array = data['exempt_roles']
        if excluded_role_id_array:
            excluded_role_ids = tuple(sorted(int(role_id) for role_id in excluded_role_id_array))
        else:
            excluded_role_ids = None
        self.excluded_role_ids = excluded_role_ids
        
        # guild_id
        # Internal field & cannot change
        
        # name
        self.name = data['name']
        
        # trigger_metadata & trigger_type
        trigger_type = AutoModerationRuleTriggerType.get(data['trigger_type'])
        trigger_metadata_type = trigger_type.metadata_type
        if (trigger_metadata_type is None):
            trigger_metadata = None
        else:
            trigger_metadata = trigger_metadata_type.from_data(data['trigger_metadata'])
        
        self.trigger_type = trigger_type
        self.trigger_metadata = trigger_metadata
    
    
    def _difference_update_attributes(self, data):
        """
        Updates the auto moderation rule and returns the changed attributes in a dictionary with the changed attributes
        in a `attribute-name`, `old-value` relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received guild profile data.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
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
            | trigger_metadata              | ``AutoModerationRuleTriggerMetadata``                     |
            +-------------------------------+-----------------------------------------------------------+
            | trigger_type                  | ``AutoModerationRuleTriggerType``                         |
            +-------------------------------+-----------------------------------------------------------+
        """
        old_attributes = {}
        
        # id
        # Already set & cannot change
        
        # actions
        action_array = data['actions']
        if action_array:
            actions = tuple(
                AutoModerationAction.from_data(auto_moderation_action_data)
                for auto_moderation_action_data in action_array
            )
        else:
            actions = None
        
        if self.actions != actions:
            old_attributes['actions'] = self.actions
            self.actions = actions
        
        # creator_id
        # Internal field & cannot change
        
        # enabled
        enabled = data['enabled']
        if self.enabled != enabled:
            old_attributes['enabled'] = self.enabled
            self.enabled = enabled
        
        # event_type
        event_type = AutoModerationEventType.get(data['event_type'])
        if self.event_type != event_type:
            old_attributes['event_type'] = self.event_type
            self.event_type = event_type
        
        # excluded_channel_ids
        excluded_channel_id_array = data['exempt_channels']
        if excluded_channel_id_array:
            excluded_channel_ids = tuple(sorted(int(channel_id) for channel_id in excluded_channel_id_array))
        else:
            excluded_channel_ids = None
        
        if self.excluded_channel_ids != excluded_channel_ids:
            old_attributes['excluded_channel_ids'] = self.excluded_channel_ids
            self.excluded_channel_ids = excluded_channel_ids
        
        # excluded_role_ids
        excluded_role_id_array = data['exempt_roles']
        if excluded_role_id_array:
            excluded_role_ids = tuple(sorted(int(role_id) for role_id in excluded_role_id_array))
        else:
            excluded_role_ids = None
        
        if self.excluded_role_ids != excluded_role_ids:
            old_attributes['excluded_role_ids'] = self.excluded_role_ids
            self.excluded_role_ids = excluded_role_ids
        
        # guild_id
        # Internal field & cannot change
        
        # name
        name = data['name']
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        # trigger_metadata & trigger_type
        trigger_type = AutoModerationRuleTriggerType.get(data['trigger_type'])
        trigger_metadata_type = trigger_type.metadata_type
        if (trigger_metadata_type is None):
            trigger_metadata = None
        else:
            trigger_metadata = trigger_metadata_type.from_data(data['trigger_metadata'])
            
        if self.trigger_metadata != trigger_metadata:
            old_attributes['trigger_metadata'] = self.trigger_metadata
            self.trigger_metadata = trigger_metadata
        
        if self.trigger_type is not trigger_type:
            old_attributes['trigger_type'] = self.trigger_type
            self.trigger_type = trigger_type
        
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
        
        # creator_id
        # Internal field
        
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
        
        # guild_id
        # Internal field
        
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
            repr_parts.append(' id=')
            repr_parts.append(repr(id_))
            
            repr_parts.append(', guild_id=')
            repr_parts.append(repr(self.guild_id))
            
            repr_parts.append(', creator_id=')
            repr_parts.append(repr(self.creator_id))
        
        # Information `.name`, `.trigger_type`
        
        # name
        repr_parts.append(', name=')
        repr_parts.append(repr(self.name))
        
        # trigger_type
        trigger_type = self.trigger_type
        repr_parts.append(', trigger_type=')
        repr_parts.append(repr(trigger_type.name))
        repr_parts.append('~')
        repr_parts.append(repr(trigger_type.value))
        
        # Additional: `.actions`, `.enabled`, `event_type`, `.excluded_channel_ids`, `.excluded_role_ids`, 
        # `.trigger_metadata`
        
        trigger_metadata = self.trigger_metadata
        if (trigger_metadata is not None):
            repr_parts.append(', trigger_metadata=')
            repr_parts.append(repr(trigger_metadata))
        
        repr_parts.append(', actions=[')
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
            repr_parts.append(', enabled=')
            repr_parts.append(repr(enabled))
        
        event_type = self.event_type
        if (
            (event_type is not AutoModerationEventType.none) and
            (event_type is not AutoModerationEventType.message_send)
        ):
            repr_parts.append(', event_type=')
            event_type.append(repr(event_type.name))
            event_type.append('~')
            event_type.append(repr(event_type.value))
        
        # excluded_channel_ids
        excluded_channel_ids = self.excluded_channel_ids
        if (excluded_channel_ids is not None):
            repr_parts.append(', excluded_channel_ids=[')
            
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
            repr_parts.append(', excluded_role_ids=[')
            
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
        
        # id
        # Internal field
        new.id = 0
        
        # actions
        actions = self.actions
        if (actions is not None):
            actions = tuple(action.copy() for action in actions)
        new.actions = actions
        
        # creator_id
        # Internal field
        new.creator_id = 0
        
        # enabled
        new.enabled = self.enabled
        
        # event_type
        new.event_type = self.event_type
        
        # excluded_channel_ids
        excluded_channel_ids = self.excluded_channel_ids
        if (excluded_channel_ids is not None):
            excluded_channel_ids = tuple(excluded_channel_id for excluded_channel_id in excluded_channel_ids)
        new.excluded_channel_ids = excluded_channel_ids
        
        # excluded_role_ids
        excluded_role_ids = self.excluded_role_ids
        if (excluded_role_ids is not None):
            excluded_role_ids = tuple(excluded_role_id for excluded_role_id in excluded_role_ids)
        new.excluded_role_ids = excluded_role_ids
        
        # guild_id
        # Internal field
        new.guild_id = 0
        
        # name
        new.name = self.name
        
        # trigger_metadata
        trigger_metadata = self.trigger_metadata
        if (trigger_metadata is not None):
            trigger_metadata = trigger_metadata.copy()
        new.trigger_metadata = trigger_metadata
        
        # trigger_type
        new.trigger_type = self.trigger_type
        
        return new
    
    
    def copy_with(self, **keyword_parameters):
        """
        Copies the auto moderation rule with the given attributes replaced.
        
        Parameters
        ----------
        actions : `None`, ``AutoModerationAction``, `iterable` of ``AutoModerationAction``, Optional (Keyword only)
            Actions which will execute when the rule is triggered.
        
        enabled : `bool` = `True`, Optional (Keyword only)
            Whether the rule is enabled.
        
        event_type : `None`, `int`, ``AutoModerationEventType`` = `AutoModerationEventType.message_send` \
                , Optional (Keyword only)
            For which events is the rule applied.
        
        excluded_channels : `None`, `int`, ``Channel``, `iterable` of (`int`, ``Channel``) = `None` \
                , Optional (Keyword only)
            Excluded channels from the rule.
        
        excluded_keywords : `None`, `str`, `iterable` of `str`, Optional (Keyword only)
            Excluded keywords from preset filter.
            
            > Only meaningful with the `keyword_presets` parameter.
        
        excluded_roles : `None`, `int`, ``Role``, `iterable` of (`int`, ``Role``) = `None`, Optional (Keyword only)
            Excluded roles from the rule.
        
        keyword_presets : `None`, `int`, ``AutoModerationKeywordPresetType``, \
                `iterable` of (`int`, ``AutoModerationKeywordPresetType``), Optional (Keyword only)
            Keyword preset defined by Discord which will be searched for in content.
            
            > Mutually exclusive with the `keywords` and `mention_limit` parameters.
        
        keywords : `None`, `str`, `iterable` of `str`, Optional (Keyword only)
            Substrings which will be searched for in content.
            
            > Mutually exclusive with the `keyword_presets` and `mention_limit` parameters.
        
        mention_limit : `None`, `int`, Optional (Keyword only)
            The amount of mentions in a message after the rule is triggered.
            
            > Mutually exclusive with the `keyword_presets` and `keywords` parameters.
        
        name : `str`, Optional (Keyword only)
            The rule's name.
        
        trigger_type : ``AutoModerationRuleTriggerType``, `int`, Optional (Keyword only)
            Auto moderation trigger type.
            
            By passing `keyword_presets` parameter you can define the trigger type as 
            `AutoModerationRuleTriggerType.keyword_preset`, or by passing the `keywords` you can define it as 
            `AutoModerationRuleTriggerType.keyword`.
        
        Returns
        -------
        new : ``AutoModerationRule``
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
            - If a parameter is unexpected.
        ValueError
            - If a parameter's value is incorrect.
        """
        # id
        # Internal field
        
        # actions
        try:
            actions = keyword_parameters.pop('actions')
        except KeyError:
            actions = self.actions
            if (actions is not None):
                actions = tuple(action.copy() for action in actions)
        else:
            actions = _validate_actions(actions)
        
        # creator_id
        # internal field
        
        # enabled
        try:
            enabled = keyword_parameters.pop('enabled')
        except KeyError:
            enabled = self.enabled
        else:
            enabled = _validate_enabled(enabled)
        
        # enabled
        try:
            event_type = keyword_parameters.pop('event_type')
        except KeyError:
            event_type = self.event_type
        else:
            event_type = _validate_event_type(event_type)
        
        # excluded_channel_ids
        try:
            excluded_channels = keyword_parameters.pop('excluded_channels')
        except KeyError:
            
            excluded_channel_ids = self.excluded_channel_ids
            if (excluded_channel_ids is not None):
                excluded_channel_ids = tuple(excluded_channel_id for excluded_channel_id in excluded_channel_ids)
        
        else:
            excluded_channel_ids = _validate_excluded_channel_ids(excluded_channels)
        
        # excluded_role_ids
        try:
            excluded_roles = keyword_parameters.pop('excluded_roles')
        except KeyError:
            
            excluded_role_ids = self.excluded_role_ids
            if (excluded_role_ids is not None):
                excluded_role_ids = tuple(excluded_role_id for excluded_role_id in excluded_role_ids)
        
        else:
            excluded_role_ids = _validate_excluded_role_ids(excluded_roles)
        
        # name
        try:
            name = keyword_parameters.pop('name')
        except KeyError:
            name = self.name
        
        else:
            name = _validate_name(name)
        
        # trigger_metadata & trigger_type
        trigger_type = keyword_parameters.pop('trigger_type', ...)
        excluded_keywords = keyword_parameters.pop('excluded_keywords', ...)
        keyword_presets = keyword_parameters.pop('keyword_presets', ...)
        keywords = keyword_parameters.pop('keywords', ...)
        mention_limit = keyword_parameters.pop('mention_limit', ...)
        
        if (trigger_type is ...) and (keyword_presets is ...) and (keywords is ...) and (mention_limit is ...):
            trigger_metadata = self.trigger_metadata
            if (trigger_metadata is not None):
                trigger_metadata = trigger_metadata.copy()
            
            trigger_type = self.trigger_type
            
        else:
            trigger_metadata, trigger_type = _validate_trigger_type_with_metadata_options(
                trigger_type, excluded_keywords, keyword_presets, keywords, mention_limit
            )
        
        if keyword_parameters:
            raise TypeError(
                f'Extra or unused parameters: {keyword_parameters!r}.'
            )
        
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
                create_partial_channel_from_id(excluded_channel_id, -1, guild_id)
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
                yield create_partial_channel_from_id(excluded_channel_id, -1, guild_id)
    
    
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
