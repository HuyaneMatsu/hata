__all__ = ('AutoModerationActionExecutionEvent',)

from scarletio import copy_docs

from ..bases import EventBase
from ..core import GUILDS
from ..channel import create_partial_channel_from_id
from ..user import create_partial_user_from_id

from .action import AutoModerationAction
from .preinstanced import AutoModerationRuleTriggerType


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
    
    content : `str`
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
    
    def __new__(cls, data):
        """
        Creates a new ``AutoModerationActionExecutionEvent`` from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Auto moderation execution event data.
        """
        self = object.__new__(cls)
        
        # action
        self.action = AutoModerationAction.from_data(data['action'])
        
        # alert_system_message_id
        alert_system_message_id = data.get('alert_system_message_id', None)
        if (alert_system_message_id is None):
            alert_system_message_id = 0
        else:
            alert_system_message_id = int(alert_system_message_id)
        self.alert_system_message_id = alert_system_message_id
        
        # channel_id
        channel_id = data.get('channel_id', None)
        if (channel_id is None):
            channel_id = 0
        else:
            channel_id = int(channel_id)
        self.channel_id = channel_id
        
        # content
        self.content = data['content']
        
        # guild_id
        guild_id = data.get('guild_id', None)
        if guild_id is None:
            guild_id = 0
        else:
            guild_id = int(guild_id)
        self.guild_id = guild_id
        
        # matched_content
        matched_content = data.get('matched_content', None)
        if (matched_content is not None) and not matched_content:
            matched_content = None
        
        self.matched_content = matched_content
        
        # matched_keyword
        matched_keyword = data.get('matched_keyword', None)
        if (matched_keyword is not None) and not matched_keyword:
            matched_keyword = None
        self.matched_keyword = matched_keyword
        
        # rule_id
        self.rule_id = int(data['rule_id'])
        
        # rule_trigger_type
        self.rule_trigger_type = AutoModerationRuleTriggerType.get(data['rule_trigger_type'])
        
        # user_id
        self.user_id = int(data['user_id'])
        
        return self
    
    
    @copy_docs(EventBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        # Descriptive fields `.guild_id`, `.channel_id`, `.user_id`, `.rule_id`.
        
        # guild_id
        guild_id = self.guild_id
        if guild_id:
            repr_parts.append(' guild_id=')
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
            
            repr_parts.append(' channel_id=')
            repr_parts.append(repr(channel_id))
        
        if field_added:
            repr_parts.append(',')
        
        # user_id
        repr_parts.append(' user_id=')
        repr_parts.append(repr(self.user_id))
        
        # rule_id
        repr_parts.append(', rule_id=')
        repr_parts.append(repr(self.rule_id))
        
        # Extra fields: `.action`, `.alert_system_message_id`, `.content`, `.matched_content`, `.matched_keyword`
        #    `rule_trigger_type`.
        
        # alert_system_message_id
        alert_system_message_id = self.alert_system_message_id
        if alert_system_message_id:
            repr_parts.append(', alert_system_message_id=')
            repr_parts.append(repr(alert_system_message_id))
        
        # action
        repr_parts.append(', action=')
        repr_parts.append(repr(self.action))
        
        # content
        repr_parts.append(', content=')
        repr_parts.append(repr(self.content))
        
        
        # rule_trigger_type
        rule_trigger_type = self.rule_trigger_type
        repr_parts.append(', rule_trigger_type=')
        repr_parts.append(repr(rule_trigger_type.name))
        repr_parts.append('~')
        repr_parts.append(repr(rule_trigger_type.value))
        
        # matched_content
        matched_content = self.matched_content
        if (matched_content is not None):
            repr_parts.append(', matched_content=')
            repr_parts.append(repr(matched_content))
        
        # matched_keyword
        matched_keyword = self.matched_keyword
        if (matched_keyword is not None):
            repr_parts.append(', matched_keyword=')
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
    
    
    @property
    def channel(self):
        """
        Returns the channel where the user content was posted.
        
        Returns
        -------
        channel : `None`, ``Channel``
        """
        channel_id = self.channel_id
        if channel_id:
            return create_partial_channel_from_id(channel_id, -1, self.guild_id)
    
    
    @property
    def guild(self):
        """
        Returns the guild where the action was executed.
        
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
        Returns the user who generated the content triggering the rule.
        
        Returns
        -------
        user : ``ClientUserBase``
        """
        return create_partial_user_from_id(self.user_id)
