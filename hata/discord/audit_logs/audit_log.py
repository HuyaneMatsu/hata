__all__ = ('AuditLog', )

from scarletio import RichAttributeErrorBaseType, WeakReferer

from ..application_command import ApplicationCommand
from ..auto_moderation import AutoModerationRule
from ..channel import Channel
from ..core import GUILDS
from ..integration import Integration
from ..scheduled_event import ScheduledEvent
from ..user import User
from ..webhook import Webhook

from .audit_log_entry import AuditLogEntry


class AuditLog(RichAttributeErrorBaseType):
    """
    Whenever an admin action is performed on the API, an audit log entry is added to the respective guild's audit
    logs. This class represents a requested  collections of these entries.
    
    Attributes
    ----------
    _self_reference : `None` or ``WeakReferer`` to ``AuditLog``
        Weak reference to the audit log itself.
    application_commands : `dict` of (`int`, ``ApplicationCommand``) items
        A dictionary that contains the mentioned application commands by the audi log entries. The keys are the `id`-s
        of the application commands, meanwhile the values are the application commands themselves.
    auto_moderation_rules : `dict` of (`int`, ``ApplicationCommand``) items
        A dictionary that contains the auto moderation rules mentioned inside of the audit log entries. The keys
        are the `id`-s of the rules and the values are the rules themselves.
    entries : `list` of ``AuditLogEntry``
        A list of audit log entries that the audit log contains.
    guild_id : `int`
        The audit logs' respective guild's identifier.
    integrations : `dict` of (`int`, ``Integration``) items
        A dictionary that contains the mentioned integrations by the audit log's entries. The keys are the `id`-s of
        the integrations, meanwhile the values are the integrations themselves.
    scheduled_events : `dict` of (`int`, ``ScheduledEvent``) items
        A dictionary containing the scheduled events mentioned inside of the audit logs.
    threads : `dict` of (`int`, ``Channel``) items
        A dictionary containing the mentioned threads inside of the audit logs.
    users : `dict` of (`int`, ``ClientUserBase``) items
        A dictionary that contains the mentioned users by the audit log's entries. The keys are the `id`-s of the
        users, meanwhile the values are the users themselves.
    webhooks : `dict` of (`int`, ``Webhook``) items
        A dictionary that contains the mentioned webhook by the audit log's entries. The keys are the `id`-s of the
        webhooks, meanwhile the values are the values themselves.
    """
    __slots__ = (
        '__weakref__', '_self_reference', 'application_commands', 'auto_moderation_rules', 'entries', 'guild_id',
        'integrations', 'scheduled_events', 'threads', 'users', 'webhooks'
    )
    
    def __new__(cls, data, guild_id):
        """
        Creates an ``AuditLog`` from the data received from Discord.
        
        Parameters
        ----------
        data : `None`, `dict` of (`str`, `Any`) items
            Data received from Discord.
        guild_id : `int`
            The respective guild's identifier of the audit logs.
        """
        self = object.__new__(cls)
        self._self_reference = None
        self.application_commands = {}
        self.auto_moderation_rules = {}
        self.entries = []
        self.guild_id = guild_id
        self.integrations = {}
        self.scheduled_events = {}
        self.threads = {}
        self.users = {}
        self.webhooks = {}
        
        if (data is not None):
            self._populate(data)
        
        return self
    
    
    def _populate(self, data):
        """
        Populates the audit log entry with the given data.
        
        Parameters
        ----------
        data : `dict` (`str`, `Any`) items
            Audit log data.
        
        Returns
        -------
        populated : `bool`
            Whether any entry was added to the audit log.
        """
        try:
            entry_datas = data['audit_log_entries']
        except KeyError:
            return False
        
        if not entry_datas:
            return False
        
        
        try:
            users_data = data['users']
        except KeyError:
            pass
        else:
            users = self.users
            
            for user_data in users_data:
                user = User.from_data(user_data)
                users[user.id] = user
        
        
        try:
            application_command_datas = data['application_commands']
        except KeyError:
            pass
        else:
            application_commands = self.application_commands
            
            for application_command_data in application_command_datas:
                application_command = ApplicationCommand.from_data(application_command_data)
                application_commands[application_command.id] = application_command
        
        
        try:
            auto_moderation_rule_datas = data['auto_moderation_rules']
        except KeyError:
            pass
        else:
            auto_moderation_rules = self.auto_moderation_rules
            
            for auto_moderation_rule_data in auto_moderation_rule_datas:
                auto_moderation_rule = AutoModerationRule.from_data(auto_moderation_rule_data)
                auto_moderation_rules[auto_moderation_rule.id] = auto_moderation_rule
        
        
        try:
            webhooks_data = data['webhook']
        except KeyError:
            pass
        else:
            webhooks = self.webhooks
            
            for webhook_data in webhooks_data:
                webhook = Webhook.from_data(webhook_data)
                webhooks[webhook.id] = webhook
        
        
        try:
            integration_datas = data['integrations']
        except KeyError:
            pass
        else:
            integrations = self.integrations
            
            for integration_data in integration_datas:
                integration = Integration.from_data(integration_data)
                integrations[integration.id] = integration
        
        
        try:
            thread_datas = data['threads']
        except KeyError:
            pass
        else:
            threads = self.threads
            
            for thread_data in thread_datas:
                thread = Channel.from_data(thread_data, None, self.guild_id)
                threads[thread.id] = thread
        
        
        try:
            scheduled_event_datas = data['guild_scheduled_events']
        except KeyError:
            pass
        else:
            scheduled_events = self.scheduled_events
            
            for scheduled_event_data in scheduled_event_datas:
                scheduled_event = ScheduledEvent.from_data(scheduled_event_data)
                scheduled_events[scheduled_event.id] = scheduled_event
        
        
        entries = self.entries
        for entry_data in entry_datas:
            entry = AuditLogEntry(entry_data, self)
            if (entry is not None):
                entries.append(entry)
        
        return True
    
    
    def _get_self_reference(self):
        self_reference = self._self_reference
        if (self_reference is None):
            self_reference = WeakReferer(self)
            self._self_reference = self_reference
        
        return self_reference
    
    
    def __iter__(self):
        """Iterates over the audit log's entries."""
        return iter(self.entries)
    
    
    def __reversed__(self):
        """Reversed iterator over the audit log's entries."""
        return reversed(self.entries)
    
    
    def __len__(self):
        """Returns the amount of entries that the audit lgo contain."""
        return len(self.entries)
    
    
    def __getitem__(self,index):
        """Returns the specific audit log entry at the given index."""
        return self.entries.__getitem__(index)
    
    
    def __repr__(self):
        """Returns the representation of the Audit log."""
        return f'<{self.__class__.__name__} length = {len(self.entries)}>'
    
    
    @property
    def guild(self):
        """
        Returns the audit log's guild.
        
        Returns
        -------
        guild : `None`, ``Guild``
        """
        return GUILDS.get(self.guild_id, None)
