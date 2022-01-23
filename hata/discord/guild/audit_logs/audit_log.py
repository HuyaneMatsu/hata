__all__ = ('AuditLog', )

from scarletio import WeakReferer

from ...channel import ChannelThread
from ...integration import Integration
from ...scheduled_event import ScheduledEvent
from ...user import User
from ...webhook import Webhook

from .audit_log_entry import AuditLogEntry


class AuditLog:
    """
    Whenever an admin action is performed on the API, an audit log entry is added to the respective guild's audit
    logs. This class represents a requested  collections of these entries.
    
    Attributes
    ----------
    _self_reference : `None` or ``WeakReferer`` to ``AuditLog``
        Weak reference to the audit log itself.
    entries : `list` of ``AuditLogEntry``
        A list of audit log entries, what the audit log contains.
    guild : ``Guild``
        The audit logs' respective guild.
    integrations : `dict` of (`int`, ``Integration``) items
        A dictionary what contains the mentioned integrations by the audit log's entries. The keys are the `id`-s of
        the integrations, meanwhile the values are the integrations themselves.
    scheduled_events : `dict` of (`int`, ``ScheduledEvent``) items
        A dictionary containing the scheduled events mentioned inside of the audit logs.
    threads : `dict` of (`int`, ``ChannelThread``) items
        A dictionary containing the mentioned threads inside of the audit logs.
    users : `dict` of (`int`, ``ClientUserBase``) items
        A dictionary, what contains the mentioned users by the audit log's entries. The keys are the `id`-s of the
        users, meanwhile the values are the users themselves.
    webhooks : `dict` of (`int`, ``Webhook``) items
        A dictionary what contains the mentioned webhook by the audit log's entries. The keys are the `id`-s of the
        webhooks, meanwhile the values are the values themselves.
    """
    __slots__ = (
        '__weakref__', '_self_reference', 'entries', 'guild', 'integrations', 'scheduled_events', 'threads', 'users',
        'webhooks'
    )
    
    def __new__(cls, data, guild):
        """
        Creates an ``AuditLog`` from the data received from Discord.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Data received from Discord.
        guild : ``Guild``
            The respective guild of the audit logs.
        """
        self = object.__new__(cls)
        self._self_reference = None
        self.entries = []
        self.guild = guild
        self.integrations = {}
        self.scheduled_events = {}
        self.threads = {}
        self.users = {}
        self.webhooks = {}
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
            Whether any entry was added to teh audit log.
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
                user = User(user_data)
                users[user.id] = user
        
        
        try:
            webhooks_data = data['webhook']
        except KeyError:
            pass
        else:
            webhooks = self.webhooks
            
            for webhook_data in webhooks_data:
                webhook = Webhook(webhook_data)
                webhooks[webhook.id] = webhook
        
        
        try:
            integration_datas = data['integrations']
        except KeyError:
            pass
        else:
            integrations = self.integrations
            
            for integration_data in integration_datas:
                integration = Integration(integration_data)
                integrations[integration.id] = integration
        
        
        try:
            thread_datas = data['threads']
        except KeyError:
            pass
        else:
            threads = self.threads
            
            for thread_data in thread_datas:
                thread = ChannelThread(thread_data, None, self.guild.id)
                threads[thread.id] = thread
        
        
        try:
            scheduled_event_datas = data['guild_scheduled_events']
        except KeyError:
            pass
        else:
            scheduled_events = self.scheduled_events
            
            for scheduled_event_data in scheduled_event_datas:
                scheduled_event = ScheduledEvent(scheduled_event_data)
                scheduled_events[scheduled_event.id] = scheduled_event
        
        
        entries = self.entries
        for entry_data in entry_datas:
            entries.append(AuditLogEntry(entry_data, self))
        
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
        """Returns the amount of entries, what the audit lgo contain."""
        return len(self.entries)
    
    
    def __getitem__(self,index):
        """Returns the specific audit log entry at the given index."""
        return self.entries.__getitem__(index)
    
    
    def __repr__(self):
        """Returns the representation of the Audit log."""
        return f'<{self.__class__.__name__} of {self.guild.name}, length={len(self.entries)}>'
