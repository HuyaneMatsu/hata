__all__ = ('AuditLog', )

from scarletio import RichAttributeErrorBaseType, WeakReferer, copy_func, export, set_docs

from ...core import GUILDS

from .fields import (
    parse_application_commands, parse_auto_moderation_rules, parse_entries, parse_integrations, parse_scheduled_events,
    parse_threads, parse_users, parse_webhooks, put_application_commands, put_auto_moderation_rules,
    put_entries, put_integrations, put_scheduled_events, put_threads, put_users,
    put_webhooks, validate_application_commands, validate_auto_moderation_rules, validate_entries,
    validate_guild_id, validate_integrations, validate_scheduled_events, validate_threads, validate_users,
    validate_webhooks
)
from .helpers import _merge_dictionaries, _merge_lists


@export
class AuditLog(RichAttributeErrorBaseType):
    """
    Whenever an admin action is performed on the API, an audit log entry is added to the respective guild's audit
    logs. This class represents a requested  collections of these entries.
    
    Attributes
    ----------
    _self_reference : `None | WeakReferer<instance>`
        Weak reference to the audit log itself.
    application_commands : `None`, `dict` of (`int`, ``ApplicationCommand``) items
        A dictionary that contains the mentioned application commands by the audit log entries. The keys are the `id`-s
        of the application commands, meanwhile the values are the application commands themselves.
    auto_moderation_rules : `None`, `dict` of (`int`, ``ApplicationCommand``) items
        A dictionary that contains the mentioned auto moderation rules by the audit log's entries. The keys
        are the `id`-s of the rules and the values are the rules themselves.
    entries : `None`, `list` of ``AuditLogEntry``
        A list of audit log entries that the audit log contains.
    guild_id : `int`
        The audit logs' respective guild's identifier.
    integrations : `None`, `dict` of (`int`, ``Integration``) items
        A dictionary that contains the mentioned integrations by the audit log's entries. The keys are the `id`-s of
        the integrations, meanwhile the values are the integrations themselves.
    scheduled_events : `None`, `dict` of (`int`, ``ScheduledEvent``) items
        A dictionary that containing the mentioned scheduled events by the the audit log's entries.
    threads : `None`, `dict` of (`int`, ``Channel``) items
        A dictionary that containing the mentioned threads by the audit log's entries.
    users : `None`, `dict` of (`int`, ``ClientUserBase``) items
        A dictionary that contains the mentioned users by the audit log's entries. The keys are the `id`-s of the
        users, meanwhile the values are the users themselves.
    webhooks : `None`, `dict` of (`int`, ``Webhook``) items
        A dictionary that contains the mentioned webhook by the audit log's entries. The keys are the `id`-s of the
        webhooks, meanwhile the values are the values themselves.
    """
    __slots__ = (
        '__weakref__', '_self_reference', 'application_commands', 'auto_moderation_rules', 'entries', 'guild_id',
        'integrations', 'scheduled_events', 'threads', 'users', 'webhooks'
    )
    
    def __new__(
        cls,
        application_commands = ...,
        auto_moderation_rules = ...,
        entries = ...,
        guild_id = ...,
        integrations = ...,
        scheduled_events = ...,
        threads = ...,
        users = ...,
        webhooks = ...,
    ):
        """
        Creates a new audit log instance.
        
        Parameters
        ----------
        application_commands : `None`, `iterable` of ``ApplicationCommand``, Optional (Keyword only)
            The mentioned application commands by the audit log's entries.
        auto_moderation_rules : `None`, `iterable` of ``ApplicationCommand``, Optional (Keyword only)
            The mentioned auto moderation rules inside of the audit log's entries.
        entries : `None`, `iterable` of ``AuditLogEntry``, Optional (Keyword only)
            The audit log entries that the audit log contains.
        guild_id : `int`
            The audit log' respective guild's identifier.
        integrations : `None`, `iterable` of ``Integration``, Optional (Keyword only)
            The mentioned integrations by the audit log's entries
        scheduled_events : `None`, `iterable` of ``ScheduledEvent``, Optional (Keyword only)
            The mentioned scheduled events mentioned by the audit log's entries.
        threads : `None`, `iterable` of ``Channel``, Optional (Keyword only)
            The mentioned threads inside of the audit log's entries.
        users : `None`, `iterable` of ``ClientUserBase``, Optional (Keyword only)
            The mentioned users by the audit log's entries.
        webhooks : `None`, `iterable` of ``Webhook`, Optional (Keyword only)
            The mentioned webhook by the audit log's entries.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # application_commands
        if application_commands is ...:
            application_commands = None
        else:
            application_commands = validate_application_commands(application_commands)
        
        # auto_moderation_rules
        if auto_moderation_rules is ...:
            auto_moderation_rules = None
        else:
            auto_moderation_rules = validate_auto_moderation_rules(auto_moderation_rules)
        
        # entries
        if entries is ...:
            entries = None
        else:
            entries = validate_entries(entries)
        
        # guild_id
        if guild_id is ...:
            guild_id = 0
        else:
            guild_id = validate_guild_id(guild_id)
        
        # integrations
        if integrations is ...:
            integrations = None
        else:
            integrations = validate_integrations(integrations)
        
        # scheduled_events
        if scheduled_events is ...:
            scheduled_events = None
        else:
            scheduled_events = validate_scheduled_events(scheduled_events)
        
        # threads
        if threads is ...:
            threads = None
        else:
            threads = validate_threads(threads)
        
        # users
        if users is ...:
            users = None
        else:
            users = validate_users(users)
        
        # webhooks
        if webhooks is ...:
            webhooks = None
        else:
            webhooks = validate_webhooks(webhooks)
        
        # Construct
        self = object.__new__(cls)
        self._self_reference = None
        self.application_commands = application_commands
        self.auto_moderation_rules = auto_moderation_rules
        self.entries = entries
        self.guild_id = guild_id
        self.integrations = integrations
        self.scheduled_events = scheduled_events
        self.threads = threads
        self.users = users
        self.webhooks = webhooks
        
        # Postprocess
        for entry in self.iter_entries():
            entry._link_parent_soft(self)
        
        return self
    
    
    @classmethod
    def from_data(cls, data, guild_id = 0):
        """
        Creates an audit log from the data,
        
        Parameters
        ----------
        data : `dict<str, object>`
            Audit log data.
        guild_id : `int` = `0`, Optional
            The respective guild's identifier of the audit logs.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self._self_reference = None
        self.application_commands = parse_application_commands(data)
        self.auto_moderation_rules = parse_auto_moderation_rules(data)
        self.entries = None
        self.guild_id = guild_id
        self.integrations = parse_integrations(data)
        self.scheduled_events = parse_scheduled_events(data)
        self.threads = parse_threads(data, guild_id)
        self.users = parse_users(data)
        self.webhooks = parse_webhooks(data)
        
        # We need self for entries.
        self.entries = parse_entries(data, self)
        
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Serialises the audit log.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        put_application_commands(self.application_commands, data, defaults)
        put_auto_moderation_rules(self.auto_moderation_rules, data, defaults)
        put_entries(self.entries, data, defaults)
        put_integrations(self.integrations, data, defaults)
        put_scheduled_events(self.scheduled_events, data, defaults)
        put_threads(self.threads, data, defaults)
        put_users(self.users, data, defaults)
        put_webhooks(self.webhooks, data, defaults)
        return data
    
    
    @classmethod
    def from_many(cls, audit_logs):
        """
        Creates a new audit log from many audit logs.
        
        Parameters
        ----------
        audit_logs : `list<AuditLog>`
            Audit logs to merge.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self._self_reference = None
        self.application_commands = _merge_dictionaries(audit_log.application_commands for audit_log in audit_logs)
        self.auto_moderation_rules = _merge_dictionaries(audit_log.auto_moderation_rules for audit_log in audit_logs)
        self.entries = _merge_lists(audit_log.entries for audit_log in audit_logs)
        self.guild_id = audit_logs[0].guild_id if audit_logs else 0
        self.integrations = _merge_dictionaries(audit_log.integrations for audit_log in audit_logs)
        self.scheduled_events = _merge_dictionaries(audit_log.scheduled_events for audit_log in audit_logs)
        self.threads = _merge_dictionaries(audit_log.threads for audit_log in audit_logs)
        self.users = _merge_dictionaries(audit_log.users for audit_log in audit_logs)
        self.webhooks = _merge_dictionaries(audit_log.webhooks for audit_log in audit_logs)
        return self
    
    
    def copy(self):
        """
        Copies the audit log.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new._self_reference = None
        
        # application_commands
        application_commands = self.application_commands
        if (application_commands is not None):
            application_commands = application_commands.copy()
        new.application_commands = application_commands
        
        # auto_moderation_rules
        auto_moderation_rules = self.auto_moderation_rules
        if (auto_moderation_rules is not None):
            auto_moderation_rules = auto_moderation_rules.copy()
        new.auto_moderation_rules = auto_moderation_rules
        
        # entries
        entries = self.entries
        if (entries is not None):
            entries = [entry.copy() for entry in entries]
        new.entries = entries
        
        # guild_id
        new.guild_id = self.guild_id
        
        # integrations
        integrations = self.integrations
        if (integrations is not None):
            integrations = integrations.copy()
        new.integrations = integrations
        
        # scheduled_events
        scheduled_events = self.scheduled_events
        if (scheduled_events is not None):
            scheduled_events = scheduled_events.copy()
        new.scheduled_events = scheduled_events
        
        # threads
        threads = self.threads
        if (threads is not None):
            threads = threads.copy()
        new.threads = threads
        
        # users
        users = self.users
        if (users is not None):
            users = users.copy()
        new.users = users
        
        # webhooks
        webhooks = self.webhooks
        if (webhooks is not None):
            webhooks = webhooks.copy()
        new.webhooks = webhooks
        
        # Postprocess
        for entry in new.iter_entries():
            entry._link_parent_hard(new)
        
        return new
    
    
    def copy_with(
        self,
        application_commands = ...,
        auto_moderation_rules = ...,
        entries = ...,
        guild_id = ...,
        integrations = ...,
        scheduled_events = ...,
        threads = ...,
        users = ...,
        webhooks = ...,
    ):
        """
        Copies the audit log with the given fields.
        
        Parameters
        ----------
        application_commands : `None`, `iterable` of ``ApplicationCommand``, Optional (Keyword only)
            The mentioned application commands by the audit log's entries.
        auto_moderation_rules : `None`, `iterable` of ``ApplicationCommand``, Optional (Keyword only)
            The mentioned auto moderation rules inside of the audit log's entries.
        entries : `None`, `iterable` of ``AuditLogEntry``, Optional (Keyword only)
            The audit log entries that the audit log contains.
        guild_id : `int`
            The audit log' respective guild's identifier.
        integrations : `None`, `iterable` of ``Integration``, Optional (Keyword only)
            The mentioned integrations by the audit log's entries
        scheduled_events : `None`, `iterable` of ``ScheduledEvent``, Optional (Keyword only)
            The mentioned scheduled events mentioned by the audit log's entries.
        threads : `None`, `iterable` of ``Channel``, Optional (Keyword only)
            The mentioned threads inside of the audit log's entries.
        users : `None`, `iterable` of ``ClientUserBase``, Optional (Keyword only)
            The mentioned users by the audit log's entries.
        webhooks : `None`, `iterable` of ``Webhook`, Optional (Keyword only)
            The mentioned webhook by the audit log's entries.
        
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
        # application_commands
        if application_commands is ...:
            application_commands = self.application_commands
            if (application_commands is not None):
                application_commands = application_commands.copy()
        else:
            application_commands = validate_application_commands(application_commands)
        
        # auto_moderation_rules
        if auto_moderation_rules is ...:
            auto_moderation_rules = self.auto_moderation_rules
            if (auto_moderation_rules is not None):
                auto_moderation_rules = auto_moderation_rules.copy()
        else:
            auto_moderation_rules = validate_auto_moderation_rules(auto_moderation_rules)
        
        # entries
        if entries is ...:
            entries = self.entries
            if (entries is not None):
                entries = [entry.copy() for entry in entries]
            
            entries_new = True
        else:
            entries = validate_entries(entries)
            entries_new = False
        
        # guild_id
        if guild_id is ...:
            guild_id = self.guild_id
        else:
            guild_id = validate_guild_id(guild_id)
        
        # integrations
        if integrations is ...:
            integrations = self.integrations
            if (integrations is not None):
                integrations = integrations.copy()
        else:
            integrations = validate_integrations(integrations)
        
        # scheduled_events
        if scheduled_events is ...:
            scheduled_events = self.scheduled_events
            if (scheduled_events is not None):
                scheduled_events = scheduled_events.copy()
        else:
            scheduled_events = validate_scheduled_events(scheduled_events)
        
        # threads
        if threads is ...:
            threads = self.threads
            if (threads is not None):
                threads = threads.copy()
        else:
            threads = validate_threads(threads)
        
        # users
        if users is ...:
            users = self.users
            if (users is not None):
                users = users.copy()
        else:
            users = validate_users(users)
        
        # webhooks
        if webhooks is ...:
            webhooks = self.webhooks
            if (webhooks is not None):
                webhooks = webhooks.copy()
        else:
            webhooks = validate_webhooks(webhooks)
        
        # Construct
        new = object.__new__(type(self))
        new._self_reference = None
        new.application_commands = application_commands
        new.auto_moderation_rules = auto_moderation_rules
        new.entries = entries
        new.guild_id = guild_id
        new.integrations = integrations
        new.scheduled_events = scheduled_events
        new.threads = threads
        new.users = users
        new.webhooks = webhooks
        
        # Postprocess
        if entries_new:
            for entry in new.iter_entries():
                entry._link_parent_hard(new)
        else:
            for entry in new.iter_entries():
                entry._link_parent_soft(new)
        
        return new
    
    
    def __iter__(self):
        """Iterates over the audit log's entries."""
        entries = self.entries
        if (entries is not None):
            yield from entries
    
    
    def __reversed__(self):
        """Reversed iterator over the audit log's entries."""
        entries = self.entries
        if (entries is not None):
            yield from reversed(entries)
    
    
    def __len__(self):
        """Returns the amount of entries that the audit log contain."""
        entries = self.entries
        if (entries is None):
            return 0
        
        return len(entries)
    
    
    def __getitem__(self, index):
        """Returns the specific audit log entry at the given index."""
        entries = self.entries
        if entries is None:
            if isinstance(index, int):
                raise IndexError(index)
            
            if isinstance(index, slice):
                return []
            
            raise TypeError(
                f'`index` can be either `int` or `slice`, got {type(index).__name__}; {index!r}.'
            )
        
        return entries[index]
    
    
    def __repr__(self):
        """Returns the representation of the Audit log."""
        return f'<{type(self).__name__} length = {len(self)}>'
    
    
    def __bool__(self):
        """Returns whether the audit log entry contains at least 1 element."""
        return (self.entries is not None)
    
    
    def __eq__(self, other):
        """Returns whether the two audit logs are equal."""
        # Shortcut
        if self is other:
            return True
        
        # Check type
        if type(self) is not type(other):
            return NotImplemented
        
        # First check guild_id and entries since they are the one who probably diverge.
        # guild_id
        if self.guild_id != other.guild_id:
            return False
        
        # entries
        if self.entries != other.entries:
            return False
        
        # application_commands
        if self.application_commands != other.application_commands:
            return False
        
        # auto_moderation_rules
        if self.auto_moderation_rules != other.auto_moderation_rules:
            return False
        
        # integrations
        if self.integrations != other.integrations:
            return False
        
        # scheduled_events
        if self.scheduled_events != other.scheduled_events:
            return False
        
        # threads
        if self.threads != other.threads:
            return False
        
        # users
        if self.users != other.users:
            return False
        
        # webhooks
        if self.webhooks != other.webhooks:
            return False
        
        return True
    
    
    def _get_self_reference(self):
        """
        Returns a self (weak) reference to the audit log itself.
        
        Returns
        -------
        self_reference : ``WeakReferer``
        """
        self_reference = self._self_reference
        if (self_reference is None):
            self_reference = WeakReferer(self)
            self._self_reference = self_reference
        
        return self_reference
    
    
    @property
    def guild(self):
        """
        Returns the audit log's guild.
        
        Returns
        -------
        guild : ``None | Guild``
        """
        return GUILDS.get(self.guild_id, None)
    
    
    # Getters
    
    def get_application_command(self, application_command_id):
        """
        Gets the application command for the given identifier.
        
        Parameters
        ----------
        application_command_id : `int`
            Application command identifier.
        
        Returns
        -------
        application_command : `None | ApplicationCommand`
        """
        application_commands = self.application_commands
        if (application_commands is not None):
            return application_commands.get(application_command_id, None)
    
    
    def get_auto_moderation_rule(self, auto_moderation_rule_id):
        """
        Gets the auto moderation rule for the given identifier.
        
        Parameters
        ----------
        auto_moderation_rule_id : `int`
            Auto moderation rule identifier.
        
        Returns
        -------
        auto_moderation_rule : `None | AutoModerationRule`
        """
        auto_moderation_rules = self.auto_moderation_rules
        if (auto_moderation_rules is not None):
            return auto_moderation_rules.get(auto_moderation_rule_id, None)
    
    
    def get_integration(self, integration_id):
        """
        Gets the integration for the given identifier.
        
        Parameters
        ----------
        integration_id : `int`
            integration identifier.
        
        Returns
        -------
        integration : `None | Integration`
        """
        integrations = self.integrations
        if (integrations is not None):
            return integrations.get(integration_id, None)
    
    
    def get_scheduled_event(self, scheduled_event_id):
        """
        Gets the scheduled event for the given identifier.
        
        Parameters
        ----------
        scheduled_event_id : `int`
            Scheduled event identifier.
        
        Returns
        -------
        scheduled_event : `None | ScheduledEvent`
        """
        scheduled_events = self.scheduled_events
        if (scheduled_events is not None):
            return scheduled_events.get(scheduled_event_id, None)
    
    
    def get_thread(self, thread_id):
        """
        Gets the thread for the given identifier.
        
        Parameters
        ----------
        thread_id : `int`
            Thread identifier.
        
        Returns
        -------
        thread : `None | Channel`
        """
        threads = self.threads
        if (threads is not None):
            return threads.get(thread_id, None)
    
    
    def get_user(self, user_id):
        """
        Gets the user for the given identifier.
        
        Parameters
        ----------
        user_id : `int`
            User identifier.
        
        Returns
        -------
        user : `None | ClientUserBase`
        """
        users = self.users
        if (users is not None):
            return users.get(user_id, None)
    
    
    def get_webhook(self, Webhook_id):
        """
        Gets the webhook for the given identifier.
        
        Parameters
        ----------
        webhook_id : `int`
            Webhook identifier.
        
        Returns
        -------
        webhook : `None | Webhook`
        """
        webhooks = self.webhooks
        if (webhooks is not None):
            return webhooks.get(Webhook_id, None)
    
    
    # Iterators
    
    
    def iter_application_commands(self):
        """
        Iterates over the application commands.
        
        This method is an iterable generator.
        
        Yields
        ------
        application_command : ``ApplicationCommand``
        """
        application_commands = self.application_commands
        if (application_commands is not None):
            yield from application_commands.values()
    
    
    def iter_auto_moderation_rules(self):
        """
        Iterates over the auto moderation rules.
        
        This method is an iterable generator.
        
        Yields
        ------
        auto_moderation_rule : ``AutoModerationRule``
        """
        auto_moderation_rules = self.auto_moderation_rules
        if (auto_moderation_rules is not None):
            yield from auto_moderation_rules.values()
    
    
    iter_entries = set_docs(
        copy_func(__iter__),
        """
        Iterates over the entries.
        
        This method is an iterable generator.
        
        Yields
        ------
        entry : ``AuditLogEntry``
        """
    )
    
    
    def iter_integrations(self):
        """
        Iterates over the integrations.
        
        This method is an iterable generator.
        
        Yields
        ------
        integration : ``Integration``
        """
        integrations = self.integrations
        if (integrations is not None):
            yield from integrations.values()
    
    
    def iter_scheduled_events(self):
        """
        Iterates over the scheduled events.
        
        This method is an iterable generator.
        
        Yields
        ------
        scheduled_event : ``ScheduledEvent``
        """
        scheduled_events = self.scheduled_events
        if (scheduled_events is not None):
            yield from scheduled_events.values()    
    
    
    def iter_threads(self):
        """
        Iterates over the threads.
        
        This method is an iterable generator.
        
        Yields
        ------
        thread : ``Channel``
        """
        threads = self.threads
        if (threads is not None):
            yield from threads.values()
    
    
    def iter_users(self):
        """
        Iterates over the users.
        
        This method is an iterable generator.
        
        Yields
        ------
        user : ``ClientUserBase``
        """
        users = self.users
        if (users is not None):
            yield from users.values()
    
    
    def iter_webhooks(self):
        """
        Iterates over the webhooks.
        
        This method is an iterable generator.
        
        Yields
        ------
        webhook : ``Webhook``
        """
        webhooks = self.webhooks
        if (webhooks is not None):
            yield from webhooks.values()
