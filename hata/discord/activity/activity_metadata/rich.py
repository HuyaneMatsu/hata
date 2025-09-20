__all__ = ('ActivityMetadataRich',)

from scarletio import copy_docs

from .base import ActivityMetadataBase
from .fields import (
    parse_application_id, parse_assets, parse_buttons, parse_created_at, parse_details, parse_details_url, parse_flags,
    parse_id, parse_name, parse_party, parse_secrets, parse_session_id, parse_state, parse_state_url, parse_sync_id,
    parse_timestamps, parse_url, put_application_id, put_assets, put_buttons, put_created_at, put_details,
    put_details_url, put_flags, put_id, put_name, put_party, put_secrets, put_session_id, put_state, put_state_url,
    put_sync_id, put_timestamps, put_url, validate_application_id, validate_assets, validate_buttons,
    validate_created_at, validate_details, validate_details_url, validate_flags, validate_id, validate_name,
    validate_party, validate_secrets, validate_session_id, validate_state, validate_state_url, validate_sync_id,
    validate_timestamps, validate_url
)
from .flags import ActivityFlag


class ActivityMetadataRich(ActivityMetadataBase):
    """
    Represents a Discord rich activity.
    
    Attributes
    ----------
    application_id : `int`
        The id of the activity's application. Defaults to `0`.
    
    assets : ``None | ActivityAssets``
        The activity's assets. Defaults to `None`.
    
    buttons : `None | tuple<str>`
        The labels of the buttons on the activity.
    
    created_at : `None | DateTime`
        When the activity was created. Defaults to Discord epoch.
    
    details : `None | str`
        What the player is currently doing. Defaults to `None`.
    
    details_url : `None | str`
        Url to open when a user click on the player is currently doing.
    
    flags : ``ActivityFlag``
        The flags of the activity. Defaults to `ActivityFlag(0)`
    
    id : `int`
        The id of the activity. Defaults to `0`.
    
    name : `str`
        The activity's name.
    
    party : ``None | ActivityParty``
        The activity's party. Defaults to `None`.
    
    secrets : ``None | ActivitySecrets``
        The activity's secrets. Defaults to `None`.
    
    session_id : `None | str`
        Spotify activity's session's id. Defaults to `None`.
    
    state : `None | str`
        The player's current party status. Defaults to `None`.
    
    state : `None | str`
        Url to open when a user clicks on a player's current party status.
    
    sync_id : `None | str`
        The id of the currently playing track of a spotify activity. Defaults to `None`.
    
    timestamps : `None | ActivityTimestamps`
        The activity's timestamps.
    
    url : `None | str`
        The url of the stream (Twitch or Youtube only). Defaults to `None`.
    """
    __slots__ = (
        'application_id', 'assets', 'buttons', 'created_at', 'details', 'details_url', 'flags', 'id', 'name', 'party',
        'secrets', 'session_id', 'state', 'state_url', 'sync_id', 'timestamps', 'url'
    )
    
    
    def __new__(
        cls,
        *,
        activity_id = ...,
        application_id = ...,
        assets = ...,
        buttons = ...,
        created_at = ...,
        details = ...,
        details_url = ...,
        flags = ...,
        name = ...,
        party = ...,
        secrets = ...,
        session_id = ...,
        state = ...,
        state_url = ...,
        sync_id = ...,
        timestamps = ...,
        url = ...,
    ):
        """
        Creates a new rich activity metadata from the given parameters.
        
        Attributes
        ----------
        activity_id : `int`, Optional (Keyword only)
            The id of the activity.
        
        application_id : `int`, Optional (Keyword only)
            The id of the activity's application.
        
        assets : ``None | ActivityAssets``, Optional (Keyword only)
            The activity's assets
    
        buttons : `None | str | iterable<str>`, Optional (Keyword only)
            The labels of the buttons on the activity.
        
        created_at : `None | DateTime`, Optional (Keyword only)
            When the activity was created.
        
        details : `None | str`, Optional (Keyword only)
            What the player is currently doing.
        
        details_url : `None | str`, Optional (Keyword only)
            Url to open when a user click on the player is currently doing.
        
        flags : `ActivityFlag | int`, Optional (Keyword only)
            The flags of the activity.
        
        name : `str`, Optional (Keyword only)
            The activity's name.
        
        party : ``None | ActivityParty``, Optional (Keyword only)
            The activity's party.
        
        secrets : ``None | ActivitySecrets``, Optional (Keyword only)
            The activity's secrets.
        
        session_id : `None | str`, Optional (Keyword only)
            Spotify activity's session's id.
        
        state : `None | str`, Optional (Keyword only)
            The player's current party status.
        
        state_url : `None | str`, Optional (Keyword only)
            Url to open when a user clicks on a player's current party status.
        
        sync_id : `None | str`, Optional (Keyword only)
            The id of the currently playing track of a spotify activity.
        
        timestamps : `None | ActivityTimestamps`, Optional (Keyword only)
            The activity's timestamps.
        
        url : `None | str`, Optional (Keyword only)
            The url of the stream (Twitch or Youtube only).
        
        Raises
        ------
        TypeError
            - If a parameter's type is unexpected.
        ValueError
           - If an parameter's value is unexpected.
        """
        # application_id
        if application_id is ...:
            application_id = 0
        else:
            application_id = validate_application_id(application_id)
        
        # assets
        if assets is ...:
            assets = None
        else:
            assets = validate_assets(assets)
        
        if buttons is ...:
            buttons = None
        else:
            buttons = validate_buttons(buttons)
        
        # created_at
        if created_at is ...:
            created_at = None
        else:
            created_at = validate_created_at(created_at)
        
        # details
        if details is ...:
            details = None
        else:
            details = validate_details(details)
        
        # details_url
        if details_url is ...:
            details_url = None
        else:
            details_url = validate_details_url(details_url)
        
        # flags
        if flags is ...:
            flags = ActivityFlag()
        else:
            flags = validate_flags(flags)
        
        # activity_id
        if activity_id is ...:
            activity_id = 0
        else:
            activity_id = validate_id(activity_id)
        
        # name
        if name is ...:
            name = ''
        else:
            name = validate_name(name)
        
        # party
        if party is ...:
            party = None
        else:
            party = validate_party(party)
        
        # secrets
        if secrets is ...:
            secrets = None
        else:
            secrets = validate_secrets(secrets)
        
        # session_id
        if session_id is ...:
            session_id = None
        else:
            session_id = validate_session_id(session_id)
        
        # state
        if state is ...:
            state = None
        else:
            state = validate_state(state)
        
        # state_url
        if state_url is ...:
            state_url = None
        else:
            state_url = validate_state_url(state_url)
        
        # sync_id
        if sync_id is ...:
            sync_id = None
        else:
            sync_id = validate_sync_id(sync_id)
        
        # timestamps
        if timestamps is ...:
            timestamps = None
        else:
            timestamps = validate_timestamps(timestamps)
        
        # url
        if url is ...:
            url = None
        else:
            url = validate_url(url)
        
        # Construct
        self = object.__new__(cls)
        self.application_id = application_id
        self.assets = assets
        self.created_at = created_at
        self.buttons = buttons
        self.details = details
        self.details_url = details_url
        self.flags = flags
        self.id = activity_id
        self.name = name
        self.party = party
        self.secrets = secrets
        self.session_id = session_id
        self.state = state
        self.state_url = state_url
        self.sync_id = sync_id
        self.timestamps = timestamps
        self.url = url
        return self
    
    
    @classmethod
    @copy_docs(ActivityMetadataBase.from_keyword_parameters)
    def from_keyword_parameters(cls, keyword_parameters):
        return cls(
            activity_id = keyword_parameters.pop('activity_id', ...),
            application_id = keyword_parameters.pop('application_id', ...),
            assets = keyword_parameters.pop('assets', ...),
            buttons = keyword_parameters.pop('buttons', ...),
            created_at = keyword_parameters.pop('created_at', ...),
            details = keyword_parameters.pop('details', ...),
            details_url = keyword_parameters.pop('details_url', ...),
            flags = keyword_parameters.pop('flags', ...),
            name = keyword_parameters.pop('name', ...),
            party = keyword_parameters.pop('party', ...),
            secrets = keyword_parameters.pop('secrets', ...),
            session_id = keyword_parameters.pop('session_id', ...),
            state = keyword_parameters.pop('state', ...),
            state_url = keyword_parameters.pop('state_url', ...),
            sync_id = keyword_parameters.pop('sync_id', ...),
            timestamps = keyword_parameters.pop('timestamps', ...),
            url = keyword_parameters.pop('url', ...),
        )
    
    
    @copy_docs(ActivityMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.name))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(ActivityMetadataBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        # application_id
        hash_value ^= self.application_id
        
        # assets
        assets = self.assets
        if (assets is not None):
            hash_value ^= hash(assets)
        
        # buttons
        buttons = self.buttons
        if (buttons is not None):
            hash_value ^= len(buttons) << 2
            for button in buttons:
                hash_value ^= hash(button)
        
        # created_at
        created_at = self.created_at
        if (created_at is not None):
            hash_value ^= hash(created_at)
        
        # details
        details = self.details
        if (details is not None):
            hash_value ^= hash(details)
        
        # details_url
        details_url = self.details_url
        if (details_url is not None):
            hash_value ^= hash(details_url)
        
        # flags
        hash_value ^= self.flags
        
        # id
        hash_value ^= self.id
        
        # name
        hash_value ^= hash(self.name)
        
        # party
        party = self.party
        if (party is not None):
            hash_value ^= hash(party)
        
        # secrets
        secrets = self.secrets
        if (secrets is not None):
            hash_value ^= hash(secrets)
        
        # session_id
        session_id = self.session_id
        if (session_id is not None):
            hash_value ^= hash(session_id)
        
        # state
        state = self.state
        if (state is not None):
            hash_value ^= hash(state)
        
        # state_url
        state_url = self.state_url
        if (state_url is not None):
            hash_value ^= hash(state_url)
        
        # sync_id
        sync_id = self.sync_id
        if (sync_id is not None):
            hash_value ^= hash(sync_id)
        
        # timestamps
        timestamps = self.timestamps
        if (timestamps is not None):
            hash_value ^= hash(timestamps)
        
        # url
        url = self.url
        if (url is not None):
            hash_value ^= hash(url)
        
        return hash_value
    
    
    @copy_docs(ActivityMetadataBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # application_id
        if self.application_id != other.application_id:
            return False
        
        # assets
        if self.assets != other.assets:
            return False
        
        # buttons
        if self.buttons != other.buttons:
            return False
        
        # created_at
        if self.created_at != other.created_at:
            return False
        
        # details
        if self.details != other.details:
            return False
        
        # details_url
        if self.details_url != other.details_url:
            return False
        
        # flags
        if self.flags != other.flags:
            return False
        
        # id
        if self.id != other.id:
            return False
        
        # name
        if self.name != other.name:
            return False
        
        # party
        if self.party != other.party:
            return False
        
        # secrets
        if self.secrets != other.secrets:
            return False
        
        # session_id
        if self.session_id != other.session_id:
            return False
        
        # state
        if self.state != other.state:
            return False
        
        # state_url
        if self.state_url != other.state_url:
            return False
        
        # sync_id
        if self.sync_id != other.sync_id:
            return False
        
        # timestamps
        if self.timestamps != other.timestamps:
            return False
        
        # url
        if self.url != other.url:
            return False
        
        return True
    
    
    @classmethod
    @copy_docs(ActivityMetadataBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        self.application_id = parse_application_id(data)
        self.id = parse_id(data)
        self._update_attributes(data)
        return self
    
    
    @copy_docs(ActivityMetadataBase.to_data)
    def to_data(self, *, defaults = False, include_internals = False, user = False):
        data = {}
        
        put_name(self.name, data, defaults)
        put_state(self.state, data, defaults)
        put_state_url(self.state_url, data, defaults)
        put_url(self.url, data, defaults)
        
        if user or include_internals:
            put_assets(self.assets, data, defaults)
            put_buttons(self.buttons, data, defaults)
            put_details(self.details, data, defaults)
            put_details_url(self.details_url, data, defaults)
            put_party(self.party, data, defaults)
            put_secrets(self.secrets, data, defaults)
            put_timestamps(self.timestamps, data, defaults)
        
        if include_internals:
            # receive only?
            put_application_id(self.application_id, data, defaults)
            put_created_at(self.created_at, data, defaults)
            put_id(self.id, data, defaults)
            
            # spotify only?
            put_flags(self.flags, data, defaults)
            put_session_id(self.session_id, data, defaults)
            put_sync_id(self.sync_id, data, defaults)
        
        return data
    
    
    @copy_docs(ActivityMetadataBase._update_attributes)
    def _update_attributes(self, data):
        # application_id & id never changes
        
        self.assets = parse_assets(data)
        self.created_at = parse_created_at(data)
        self.buttons = parse_buttons(data)
        self.details = parse_details(data)
        self.details_url = parse_details_url(data)
        self.flags = parse_flags(data)
        self.name = parse_name(data)
        self.party = parse_party(data)
        self.secrets = parse_secrets(data)
        self.session_id = parse_session_id(data)
        self.state = parse_state(data)
        self.state_url = parse_state_url(data)
        self.sync_id = parse_sync_id(data)
        self.timestamps = parse_timestamps(data)
        self.url = parse_url(data)
    
    
    @copy_docs(ActivityMetadataBase._difference_update_attributes)
    def _difference_update_attributes(self, data):
        old_attributes = {}
        
        # application_id & id never changes
        
        # assets
        assets = parse_assets(data)
        if self.assets != assets:
            old_attributes['assets'] = self.assets
            self.assets = assets
        
        # buttons
        buttons = parse_buttons(data)
        if self.buttons != buttons:
            old_attributes['buttons'] = self.buttons
            self.buttons = buttons
        
        # created_at
        created_at = parse_created_at(data)
        if self.created_at != created_at:
            old_attributes['created_at'] = self.created_at
            self.created_at = created_at
        
        # details
        details = parse_details(data)
        if self.details != details:
            old_attributes['details'] = self.details
            self.details = details
        
        # details_url
        details_url = parse_details_url(data)
        if self.details_url != details_url:
            old_attributes['details_url'] = self.details_url
            self.details_url = details_url
        
        # flags
        flags = parse_flags(data)
        if self.flags != flags:
            old_attributes['flags'] = self.flags
            self.flags = flags
        
        # name
        name = parse_name(data)
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        # party
        party = parse_party(data)
        if self.party != party:
            old_attributes['party'] = self.party
            self.party = party
        
        # secrets
        secrets = parse_secrets(data)
        if self.secrets != secrets:
            old_attributes['secrets'] = self.secrets
            self.secrets = secrets
        
        # session_id
        session_id = parse_session_id(data)
        if self.session_id != session_id:
            old_attributes['session_id'] = self.session_id
            self.session_id = session_id
        
        # state
        state = parse_state(data)
        if self.state != state:
            old_attributes['state'] = self.state
            self.state = state
        
        # state_url
        state_url = parse_state_url(data)
        if self.state_url != state_url:
            old_attributes['state_url'] = self.state_url
            self.state_url = state_url
        
        # sync_id
        sync_id = parse_sync_id(data)
        if self.sync_id != sync_id:
            old_attributes['sync_id'] = self.sync_id
            self.sync_id = sync_id
        
        # timestamps
        timestamps = parse_timestamps(data)
        if self.timestamps != timestamps:
            old_attributes['timestamps'] = self.timestamps
            self.timestamps = timestamps
        
        # url
        url = parse_url(data)
        if self.url != url:
            old_attributes['url'] = self.url
            self.url = url
        
        return old_attributes
    
    
    @copy_docs(ActivityMetadataBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        new.application_id = self.application_id
        assets = self.assets
        if (assets is not None):
            assets = assets.copy()
        new.assets = assets
        
        buttons = self.buttons
        if (buttons is not None):
            buttons = (*buttons,)
        new.buttons = buttons
        
        new.created_at = self.created_at
        new.details = self.details
        new.details_url = self.details_url
        new.flags = self.flags
        new.id = self.id
        new.name = self.name
        party = self.party
        if (party is not None):
            party = party.copy()
        new.party = party
        secrets = self.secrets
        if (secrets is not None):
            secrets = secrets.copy()
        new.secrets = secrets
        new.session_id = self.session_id
        new.state = self.state
        new.state_url = self.state_url
        new.sync_id = self.sync_id
        timestamps = self.timestamps
        if (timestamps is not None):
            timestamps = timestamps.copy()
        new.timestamps = timestamps
        new.url = self.url
        return new
    
    
    def copy_with(
        self, 
        *,
        activity_id = ...,
        application_id = ...,
        assets = ...,
        buttons = ...,
        created_at = ...,
        details = ...,
        details_url = ...,
        flags = ...,
        name = ...,
        party = ...,
        secrets = ...,
        session_id = ...,
        state = ...,
        state_url = ...,
        sync_id = ...,
        timestamps = ...,
        url = ...,
    ):
        """
        Copies the rich activity metadata with the given fields.
        
        Attributes
        ----------
        activity_id : `int`, Optional (Keyword only)
            The id of the activity.
        
        application_id : `int`, Optional (Keyword only)
            The id of the activity's application.
        
        assets : ``None | ActivityAssets``, Optional (Keyword only)
            The activity's assets
        
        buttons : `None | str | iterable<str>`, Optional (Keyword only)
            The labels of the buttons on the activity.
        
        created_at : `None | DateTime`, Optional (Keyword only)
            When the activity was created.
        
        details : `None | str`, Optional (Keyword only)
            What the player is currently doing.
        
        details_url : `None | str`, Optional (Keyword only)
            Url to open when a user click on the player is currently doing.
        
        flags : `ActivityFlag | int`, Optional (Keyword only)
            The flags of the activity.
        
        name : `str`, Optional (Keyword only)
            The activity's name.
        
        party : ``None | ActivityParty``, Optional (Keyword only)
            The activity's party.
        
        secrets : ``None | ActivitySecrets``, Optional (Keyword only)
            The activity's secrets.
        
        session_id : `None | str`, Optional (Keyword only)
            Spotify activity's session's id.
        
        state : `None | str`, Optional (Keyword only)
            The player's current party status.
        
        state_url : `None | str`, Optional (Keyword only)
            Url to open when a user clicks on a player's current party status.
        
        sync_id : `None | str`, Optional (Keyword only)
            The id of the currently playing track of a spotify activity.
        
        timestamps : `None | ActivityTimestamps`, Optional (Keyword only)
            The activity's timestamps.
        
        url : `None | str`, Optional (Keyword only)
            The url of the stream (Twitch or Youtube only).
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is unexpected.
        ValueError
           - If an parameter's value is unexpected.
        """
        # application_id
        if application_id is ...:
            application_id = self.application_id
        else:
            application_id = validate_application_id(application_id)
        
        # assets
        if assets is ...:
            assets = self.assets
            if (assets is not None):
                assets = assets.copy()
        else:
            assets = validate_assets(assets)
        
        # buttons
        if buttons is ...:
            buttons = self.buttons
            if (buttons is not None):
                buttons = (*buttons,)
        else:
            buttons = validate_buttons(buttons)
        
        # created_at
        if created_at is ...:
            created_at = self.created_at
        else:
            created_at = validate_created_at(created_at)
        
        # details
        if details is ...:
            details = self.details
        else:
            details = validate_details(details)
        
        # details_url
        if details_url is ...:
            details_url = self.details_url
        else:
            details_url = validate_details_url(details_url)
        
        # flags
        if flags is ...:
            flags = self.flags
        else:
            flags = validate_flags(flags)
        
        # activity_id
        if activity_id is ...:
            activity_id = self.id
        else:
            activity_id = validate_id(activity_id)
        
        # name
        if name is ...:
            name = self.name
        else:
            name = validate_name(name)
        
        # party
        if party is ...:
            party = self.party
            if (party is not None):
                party = party.copy()
        else:
            party = validate_party(party)
        
        # secrets
        if secrets is ...:
            secrets = self.secrets
            if (secrets is not None):
                secrets = secrets.copy()
        else:
            secrets = validate_secrets(secrets)
        
        # session_id
        if session_id is ...:
            session_id = self.session_id
        else:
            session_id = validate_session_id(session_id)
        
        # state
        if state is ...:
            state = self.state
        else:
            state = validate_state(state)
        
        # state_url
        if state_url is ...:
            state_url = self.state_url
        else:
            state_url = validate_state_url(state_url)
        
        # sync_id
        if sync_id is ...:
            sync_id = self.sync_id
        else:
            sync_id = validate_sync_id(sync_id)
        
        # timestamps
        if timestamps is ...:
            timestamps = self.timestamps
            if (timestamps is not None):
                timestamps = timestamps.copy()
        else:
            timestamps = validate_timestamps(timestamps)
        
        # url
        if url is ...:
            url = self.url
        else:
            url = validate_url(url)
        
        # Construct
        new = object.__new__(type(self))
        new.application_id = application_id
        new.assets = assets
        new.buttons = buttons
        new.created_at = created_at
        new.details = details
        new.details_url = details_url
        new.flags = flags
        new.id = activity_id
        new.name = name
        new.party = party
        new.secrets = secrets
        new.session_id = session_id
        new.state = state
        new.state_url = state_url
        new.sync_id = sync_id
        new.timestamps = timestamps
        new.url = url
        return new
    
    
    @copy_docs(ActivityMetadataBase.copy_with_keyword_parameters)
    def copy_with_keyword_parameters(self, keyword_parameters):
        return self.copy_with(
            activity_id = keyword_parameters.pop('activity_id', ...),
            application_id = keyword_parameters.pop('application_id', ...),
            assets = keyword_parameters.pop('assets', ...),
            buttons = keyword_parameters.pop('buttons', ...),
            created_at = keyword_parameters.pop('created_at', ...),
            details = keyword_parameters.pop('details', ...),
            details_url = keyword_parameters.pop('details_url', ...),
            flags = keyword_parameters.pop('flags', ...),
            name = keyword_parameters.pop('name', ...),
            party = keyword_parameters.pop('party', ...),
            secrets = keyword_parameters.pop('secrets', ...),
            session_id = keyword_parameters.pop('session_id', ...),
            state = keyword_parameters.pop('state', ...),
            state_url = keyword_parameters.pop('state_url', ...),
            sync_id = keyword_parameters.pop('sync_id', ...),
            timestamps = keyword_parameters.pop('timestamps', ...),
            url = keyword_parameters.pop('url', ...),
        )
