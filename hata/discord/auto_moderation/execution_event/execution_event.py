__all__ = ('AutoModerationActionExecutionEvent',)

from scarletio import copy_docs

from ...bases import EventBase
from ...channel import ChannelType, create_partial_channel_from_id
from ...core import AUTO_MODERATION_RULES, GUILDS
from ...message import Message
from ...user import create_partial_user_from_id

from ..action import AutoModerationAction
from ..rule import AutoModerationRuleTriggerType

from .fields import (
    parse_action, parse_alert_system_message_id, parse_channel_id, parse_content, parse_guild_id, parse_matched_content,
    parse_matched_keyword, parse_rule_id, parse_rule_trigger_type, parse_user_id, put_action_into,
    put_alert_system_message_id_into, put_channel_id_into, put_content_into, put_guild_id_into,
    put_matched_content_into, put_matched_keyword_into, put_rule_id_into, put_rule_trigger_type_into, put_user_id_into,
    validate_action, validate_alert_system_message_id, validate_channel_id, validate_content, validate_guild_id,
    validate_matched_content, validate_matched_keyword, validate_rule_id, validate_rule_trigger_type, validate_user_id
)


class AutoModerationActionExecutionEvent(EventBase):
    """
    Represents an auto moderation rule's execution.
    
    Attributes
    ----------
    action : ``AutoModerationAction``
        The action which was executed.
    
    alert_system_message_id : `int`
        The id of the system auto moderation message posted as a result of this action.
        
        > Will default to `0` if the action's type is not `AutoModerationActionType.send_alert_message`.
    
    channel_id : `int`
        The channel's identifier where the user content was posted.
        
        > Defaults to `0` if not applicable.
    
    content : `None`, `str`
        The user generated text content.
    
    guild_id : `int`
        The guild's identifier where the action was executed.
    
    matched_content : `None`, `str`
        The substring in the user submitted content that triggered the rule.
    
    matched_keyword : `None`, `str`
        The matched keyword of the triggered rule.
    
    rule_id : `int`
        The triggered rule's identifier.
    
    rule_trigger_type : ``AutoModerationRuleTriggerType``
        The triggered rule's type.
    
    user_id : `int`
        The user who generated the content triggering the rule.
    """
    __slots__ = (
        'action', 'alert_system_message_id', 'channel_id', 'content', 'guild_id', 'matched_content', 'matched_keyword',
        'rule_id', 'rule_trigger_type', 'user_id'
    )
    
    
    def __new__(
        cls,
        *,
        action = ..., 
        alert_system_message_id = ...,
        channel_id = ...,
        content = ...,
        guild_id = ...,
        matched_content = ...,
        matched_keyword = ...,
        rule_id = ...,
        rule_trigger_type = ...,
        user_id = ...,
    ):
        """
        Creates a new auto mod execution event.
        
        Parameters
        ----------
        action : `None`, ``AutoModerationAction``, Optional (Keyword only)
            The action which was executed.
        
        alert_system_message_id : `None`, ``Message``, `int`, Optional (Keyword only)
            The id of the system auto moderation message posted as a result of this action.
        
        channel_id : `None`, ``Channel``, `int`, Optional (Keyword only)
            The channel's identifier where the user content was posted.
        
        content : `None`, `str`, Optional (Keyword only)
            The user generated text content.
        
        guild_id : `None`, ``Guild``, `int`, Optional (Keyword only)
            The guild's identifier where the action was executed.
        
        matched_content : `None`, `str`, Optional (Keyword only)
            The substring in the user submitted content that triggered the rule.
        
        matched_keyword : `None`, `str`, Optional (Keyword only)
            The matched keyword of the triggered rule.
        
        rule_id : `None`, ``AutoModerationRule``, `int`, Optional (Keyword only)
            The triggered rule's identifier.
        
        rule_trigger_type : `None`, ``AutoModerationRuleTriggerType``, `int`, Optional (Keyword only)
            The triggered rule's type.
        
        user_id : `None`, ``ClientUserBase``, `int`, Optional (Keyword only)
            The user who generated the content triggering the rule.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # action
        if action is ...:
            action = AutoModerationAction()
        else:
            action = validate_action(action)
        
        # alert_system_message_id
        if alert_system_message_id is ...:
            alert_system_message_id = 0
        else:
            alert_system_message_id = validate_alert_system_message_id(alert_system_message_id)
        
        # channel_id
        if channel_id is ...:
            channel_id = 0
        else:
            channel_id = validate_channel_id(channel_id)
        
        # content
        if content is ...:
            content = None
        else:
            content = validate_content(content)
        
        # guild_id
        if guild_id is ...:
            guild_id = 0
        else:
            guild_id = validate_guild_id(guild_id)
        
        # matched_content
        if matched_content is ...:
            matched_content = None
        else:
            matched_content = validate_matched_content(matched_content)
        
        # matched_keyword
        if matched_keyword is ...:
            matched_keyword = None
        else:
            matched_keyword = validate_matched_keyword(matched_keyword)
        
        # rule_id
        if rule_id is ...:
            rule_id = 0
        else:
            rule_id = validate_rule_id(rule_id)
        
        # rule_trigger_type
        if rule_trigger_type is ...:
            rule_trigger_type = AutoModerationRuleTriggerType.none
        else:
            rule_trigger_type = validate_rule_trigger_type(rule_trigger_type)
        
        # user_id
        if user_id is ...:
            user_id = 0
        else:
            user_id = validate_user_id(user_id)
        
        # Construct
        
        self = object.__new__(cls)
        self.action = action
        self.alert_system_message_id = alert_system_message_id
        self.channel_id = channel_id
        self.content = content
        self.guild_id = guild_id
        self.matched_content = matched_content
        self.matched_keyword = matched_keyword
        self.rule_id = rule_id
        self.rule_trigger_type = rule_trigger_type
        self.user_id = user_id
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new ``AutoModerationActionExecutionEvent`` from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Auto moderation execution event data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.action = parse_action(data)
        self.alert_system_message_id = parse_alert_system_message_id(data)
        self.channel_id = parse_channel_id(data)
        self.content = parse_content(data)
        self.guild_id = parse_guild_id(data)
        self.matched_content = parse_matched_content(data)
        self.matched_keyword = parse_matched_keyword(data)
        self.rule_id = parse_rule_id(data)
        self.rule_trigger_type = parse_rule_trigger_type(data)
        self.user_id = parse_user_id(data)
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the event to json serializable representation dictionary.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        Returns
        -------
        data : `dict` of (`str`, `str`) items
        """
        data = {}
        put_action_into(self.action, data, defaults)
        put_alert_system_message_id_into(self.alert_system_message_id, data, defaults)
        put_channel_id_into(self.channel_id, data, defaults)
        put_content_into(self.content, data, defaults)
        put_guild_id_into(self.guild_id, data, defaults)
        put_matched_content_into(self.matched_content, data, defaults)
        put_matched_keyword_into(self.matched_keyword, data, defaults)
        put_rule_id_into(self.rule_id, data, defaults)
        put_rule_trigger_type_into(self.rule_trigger_type, data, defaults)
        put_user_id_into(self.user_id, data, defaults)
        return data
    
    
    @copy_docs(EventBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        # Descriptive fields `.guild_id`, `.channel_id`, `.user_id`, `.rule_id`.
        
        # guild_id
        guild_id = self.guild_id
        if guild_id:
            repr_parts.append(' guild_id = ')
            repr_parts.append(repr(guild_id))
            
            field_added = True
            
        else:
            field_added = False
        
        # channel_id
        channel_id = self.channel_id
        if channel_id:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' channel_id = ')
            repr_parts.append(repr(channel_id))
        
        if field_added:
            repr_parts.append(',')
        
        # user_id
        repr_parts.append(' user_id = ')
        repr_parts.append(repr(self.user_id))
        
        # rule_id
        repr_parts.append(', rule_id = ')
        repr_parts.append(repr(self.rule_id))
        
        # Extra fields: `.action`, `.alert_system_message_id`, `.content`, `.matched_content`, `.matched_keyword`
        #    `rule_trigger_type`.
        
        # alert_system_message_id
        alert_system_message_id = self.alert_system_message_id
        if alert_system_message_id:
            repr_parts.append(', alert_system_message_id = ')
            repr_parts.append(repr(alert_system_message_id))
        
        # action
        repr_parts.append(', action = ')
        repr_parts.append(repr(self.action))
        
        # content
        repr_parts.append(', content = ')
        repr_parts.append(repr(self.content))
        
        
        # rule_trigger_type
        rule_trigger_type = self.rule_trigger_type
        repr_parts.append(', rule_trigger_type = ')
        repr_parts.append(repr(rule_trigger_type.name))
        repr_parts.append(' ~ ')
        repr_parts.append(repr(rule_trigger_type.value))
        
        # matched_content
        matched_content = self.matched_content
        if (matched_content is not None):
            repr_parts.append(', matched_content = ')
            repr_parts.append(repr(matched_content))
        
        # matched_keyword
        matched_keyword = self.matched_keyword
        if (matched_keyword is not None):
            repr_parts.append(', matched_keyword = ')
            repr_parts.append(repr(matched_keyword))

        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(EventBase.__len__)
    def __len__(self):
        return 4
    
    
    @copy_docs(EventBase.__iter__)
    def __iter__(self):
        yield self.guild_id
        yield self.channel_id
        yield self.user_id
        yield self.rule_id
    
    
    @copy_docs(EventBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # action
        hash_value ^= hash(self.action)
        
        # alert_system_message_id
        hash_value ^= self.alert_system_message_id
        
        # channel_id
        hash_value ^= self.channel_id
        
        # content
        hash_value ^= hash(self.content)
        
        # guild_id
        hash_value ^= self.guild_id
        
        # matched_content
        matched_content = self.matched_content
        if (matched_content is not None):
            hash_value ^= hash(matched_content)
        
        # matched_keyword
        matched_keyword = self.matched_keyword
        if (matched_keyword is not None):
            hash_value ^= hash(matched_keyword)
        
        # rule_id
        hash_value ^= self.rule_id
        
        # rule_trigger_type
        hash_value ^= self.rule_trigger_type.value
        
        # user_id
        hash_value ^= self.user_id
        
        return hash_value
    
    
    @copy_docs(EventBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        # action
        if self.action != other.action:
            return False
        
        # alert_system_message_id
        if self.alert_system_message_id != other.alert_system_message_id:
            return False
        
        # channel_id
        if self.channel_id != other.channel_id:
            return False
        
        # content
        if self.content != other.content:
            return False
        
        # guild_id
        if self.guild_id != other.guild_id:
            return False
        
        # matched_content
        if self.matched_content != other.matched_content:
            return False
        
        # matched_keyword
        if self.matched_keyword != other.matched_keyword:
            return False
        
        # rule_id
        if self.rule_id != other.rule_id:
            return False
        
        # rule_trigger_type
        if self.rule_trigger_type != other.rule_trigger_type:
            return False
        
        # user_id
        if self.user_id != other.user_id:
            return False
        
        return True
    
    
    def copy(self):
        """
        Returns a copy of the event.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.action = self.action.copy()
        new.alert_system_message_id = self.alert_system_message_id
        new.channel_id = self.channel_id
        new.content = self.content
        new.guild_id = self.guild_id
        new.matched_content = self.matched_content
        new.matched_keyword = self.matched_keyword
        new.rule_id = self.rule_id
        new.rule_trigger_type = self.rule_trigger_type
        new.user_id = self.user_id
        return new
    
    
    def copy_with(
        self,
        *,
        action = ..., 
        alert_system_message_id = ...,
        channel_id = ...,
        content = ...,
        guild_id = ...,
        matched_content = ...,
        matched_keyword = ...,
        rule_id = ...,
        rule_trigger_type = ...,
        user_id = ...,
    ):
        """
        Returns a copy of the event with it's attributes modified based on the defined fields.
        
        Parameters
        ----------
        action : `None`, ``AutoModerationAction``, Optional (Keyword only)
            The action which was executed.
        
        alert_system_message_id : `None`, ``Message``, `int`, Optional (Keyword only)
            The id of the system auto moderation message posted as a result of this action.
        
        channel_id : `None`, ``Channel``, `int`, Optional (Keyword only)
            The channel's identifier where the user content was posted.
        
        content : `None`, `str`, Optional (Keyword only)
            The user generated text content.
        
        guild_id : `None`, ``Guild``, `int`, Optional (Keyword only)
            The guild's identifier where the action was executed.
        
        matched_content : `None`, `str`, Optional (Keyword only)
            The substring in the user submitted content that triggered the rule.
        
        matched_keyword : `None`, `str`, Optional (Keyword only)
            The matched keyword of the triggered rule.
        
        rule_id : `None`, ``AutoModerationRule``, `int`, Optional (Keyword only)
            The triggered rule's identifier.
        
        rule_trigger_type : `None`, ``AutoModerationRuleTriggerType``, `int`, Optional (Keyword only)
            The triggered rule's type.
        
        user_id : `None`, ``ClientUserBase``, `int`, Optional (Keyword only)
            The user who generated the content triggering the rule.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # action
        if action is ...:
            action = self.action.copy()
        else:
            action = validate_action(action)
        
        # alert_system_message_id
        if alert_system_message_id is ...:
            alert_system_message_id = self.alert_system_message_id
        else:
            alert_system_message_id = validate_alert_system_message_id(alert_system_message_id)
        
        # channel_id
        if channel_id is ...:
            channel_id = self.channel_id
        else:
            channel_id = validate_channel_id(channel_id)
        
        # content
        if content is ...:
            content = self.content
        else:
            content = validate_content(content)
        
        # guild_id
        if guild_id is ...:
            guild_id = self.guild_id
        else:
            guild_id = validate_guild_id(guild_id)
        
        # matched_content
        if matched_content is ...:
            matched_content = self.matched_content
        else:
            matched_content = validate_matched_content(matched_content)
        
        # matched_keyword
        if matched_keyword is ...:
            matched_keyword = self.matched_keyword
        else:
            matched_keyword = validate_matched_keyword(matched_keyword)
        
        # rule_id
        if rule_id is ...:
            rule_id = self.rule_id
        else:
            rule_id = validate_rule_id(rule_id)
        
        # rule_trigger_type
        if rule_trigger_type is ...:
            rule_trigger_type = self.rule_trigger_type
        else:
            rule_trigger_type = validate_rule_trigger_type(rule_trigger_type)
        
        # user_id
        if user_id is ...:
            user_id = self.user_id
        else:
            user_id = validate_user_id(user_id)
        
        # Construct
        
        new = object.__new__(type(self))
        new.action = action
        new.alert_system_message_id = alert_system_message_id
        new.channel_id = channel_id
        new.content = content
        new.guild_id = guild_id
        new.matched_content = matched_content
        new.matched_keyword = matched_keyword
        new.rule_id = rule_id
        new.rule_trigger_type = rule_trigger_type
        new.user_id = user_id
        return new
    
    
    @property
    def channel(self):
        """
        Returns the channel where the user content was posted. Returns a partial channel if not cached,
        
        Returns
        -------
        channel : `None`, ``Channel``
        """
        channel_id = self.channel_id
        if channel_id:
            return create_partial_channel_from_id(channel_id, ChannelType.unknown, self.guild_id)
    
    
    @property
    def guild(self):
        """
        Returns the guild where the action was executed. Returns `None` if the guild is not cached.
        
        > The guild must be cached.
        
        Returns
        -------
        guild : `None`, ``Guild``
        """
        guild_id = self.guild_id
        if guild_id:
            return GUILDS.get(guild_id, None)
    
    
    @property
    def user(self):
        """
        Returns the user who generated the content triggering the rule. Returns a partial user if not cached.
        
        Returns
        -------
        user : ``ClientUserBase``
        """
        return create_partial_user_from_id(self.user_id)
    
    
    @property
    def alert_system_message(self):
        """
        Returns the sent alert message. If the message is not cached will return a partial one.
        
        Returns
        -------
        message : `None`, ``Message``
        """
        alert_system_message_id = self.alert_system_message_id
        if alert_system_message_id:
            return Message._create_from_partial_fields(alert_system_message_id, self.channel_id, self.guild_id)
    
    
    @property
    def rule(self):
        """
        Returns the auto moderation rule that executed the event. Returns `None` if the message is not cached.
        
        Returns
        -------
        message : `None`, ``AutoModerationRule``
        """
        rule_id = self.rule_id
        if rule_id:
            return AUTO_MODERATION_RULES.get(rule_id, None)
