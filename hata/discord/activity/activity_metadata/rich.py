__all__ = ('ActivityMetadataRich',)

from scarletio import copy_docs

from .base import ActivityMetadataBase
from .fields import (
    parse_application_id, parse_assets, parse_created_at, parse_details, parse_flags, parse_id, parse_name, parse_party,
    parse_secrets, parse_session_id, parse_state, parse_sync_id, parse_timestamps, parse_url, put_application_id_into,
    put_assets_into, put_created_at_into, put_details_into, put_flags_into, put_id_into, put_name_into, put_party_into,
    put_secrets_into, put_session_id_into, put_state_into, put_sync_id_into, put_timestamps_into, put_url_into,
    validate_application_id, validate_assets, validate_created_at, validate_details, validate_flags, validate_id,
    validate_name, validate_party, validate_secrets, validate_session_id, validate_state, validate_sync_id,
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
    assets : `None`, ``ActivityAssets``
        The activity's assets. Defaults to `None`.
    created_at : `None`, `datetime`
        When the activity was created. Defaults to Discord epoch.
    details : `None`, `str`
        What the player is currently doing. Defaults to `None`.
    flags : ``ActivityFlag``
        The flags of the activity. Defaults to `ActivityFlag(0)`
    id : `int`
        The id of the activity. Defaults to `0`.
    name : `str`
        The activity's name.
    party : `None`, ``ActivityParty``
        The activity's party. Defaults to `None`.
    secrets : `None`, ``ActivitySecrets``
        The activity's secrets. Defaults to `None`.
    session_id : `None`, `str`
        Spotify activity's session's id. Defaults to `None`.
    state : `None`, `str`
        The player's current party status. Defaults to `None`.
    sync_id : `None`, `str`
        The id of the currently playing track of a spotify activity. Defaults to `None`.
    timestamps : `None`, ``ActivityTimestamps``
        The activity's timestamps.
    url : `None`, `str`
        The url of the stream (Twitch or Youtube only). Defaults to `None`.
    """
    __slots__ = (
        'application_id', 'assets', 'created_at', 'details', 'flags', 'id', 'name', 'party', 'secrets', 'session_id',
        'state', 'sync_id', 'timestamps', 'url'
    )
    
    
    def __new__(
        cls,
        *,
        activity_id = ...,
        application_id = ...,
        assets = ...,
        created_at = ...,
        details = ...,
        flags = ...,
        name = ...,
        party = ...,
        secrets = ...,
        session_id = ...,
        state = ...,
        sync_id = ...,
        timestamps = ...,
        url = ...,
    ):
        """
        Creates a new rich activity metadata from the given parameters.
        
        Attributes
        ----------
        activity_id : `int`
            The id of the activity.
        application_id : `int`
            The id of the activity's application.
        assets : `None`, ``ActivityAssets``
            The activity's assets
        created_at : `None`, `datetime`
            When the activity was created.
        details : `None`, `str`
            What the player is currently doing.
        flags : ``ActivityFlag``, `int`
            The flags of the activity.
        name : `str`
            The activity's name.
        party : `None`, ``ActivityParty``
            The activity's party.
        secrets : `None`, ``ActivitySecrets``
            The activity's secrets.
        session_id : `None`, `str`
            Spotify activity's session's id. 
        state : `None`, `str`
            The player's current party status.
        sync_id : `None`, `str`
            The id of the currently playing track of a spotify activity.
        timestamps : `None`, ``ActivityTimestamps``
            The activity's timestamps.
        url : `None`, `str`, Optional
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
        self.details = details
        self.flags = flags
        self.id = activity_id
        self.name = name
        self.party = party
        self.secrets = secrets
        self.session_id = session_id
        self.state = state
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
            created_at = keyword_parameters.pop('created_at', ...),
            details = keyword_parameters.pop('details', ...),
            flags = keyword_parameters.pop('flags', ...),
            name = keyword_parameters.pop('name', ...),
            party = keyword_parameters.pop('party', ...),
            secrets = keyword_parameters.pop('secrets', ...),
            session_id = keyword_parameters.pop('session_id', ...),
            state = keyword_parameters.pop('state', ...),
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
        
        # created_at
        created_at = self.created_at
        if (created_at is not None):
            hash_value ^= hash(created_at)
        
        # details
        details = self.details
        if (details is not None):
            hash_value ^= hash(details)
        
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
        
        # created_at
        if self.created_at != other.created_at:
            return False
        
        # details
        if self.details != other.details:
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
        
        put_name_into(self.name, data, defaults)
        put_url_into(self.url, data, defaults)
        
        if user or include_internals:
            put_assets_into(self.assets, data, defaults)
            put_details_into(self.details, data, defaults)
            put_party_into(self.party, data, defaults)
            put_secrets_into(self.secrets, data, defaults)
            put_state_into(self.state, data, defaults)
            put_timestamps_into(self.timestamps, data, defaults)
        
        if include_internals:
            # receive only?
            put_application_id_into(self.application_id, data, defaults)
            put_created_at_into(self.created_at, data, defaults)
            put_id_into(self.id, data, defaults)
            
            # spotify only?
            put_flags_into(self.flags, data, defaults)
            put_session_id_into(self.session_id, data, defaults)
            put_sync_id_into(self.sync_id, data, defaults)
        
        return data
    
    
    @copy_docs(ActivityMetadataBase._update_attributes)
    def _update_attributes(self, data):
        # application_id & id never changes
        
        self.assets = parse_assets(data)
        self.created_at = parse_created_at(data)
        self.details = parse_details(data)
        self.flags = parse_flags(data)
        self.name = parse_name(data)
        self.party = parse_party(data)
        self.secrets = parse_secrets(data)
        self.session_id = parse_session_id(data)
        self.state = parse_state(data)
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
        new.created_at = self.created_at
        new.details = self.details
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
        created_at = ...,
        details = ...,
        flags = ...,
        name = ...,
        party = ...,
        secrets = ...,
        session_id = ...,
        state = ...,
        sync_id = ...,
        timestamps = ...,
        url = ...,
    ):
        """
        Copies the rich activity metadata with the given fields.
        
        Attributes
        ----------
        activity_id : `int`
            The id of the activity.
        application_id : `int`
            The id of the activity's application.
        assets : `None`, ``ActivityAssets``
            The activity's assets
        created_at : `None`, `datetime`
            When the activity was created.
        details : `None`, `str`
            What the player is currently doing.
        flags : ``ActivityFlag``, `int`
            The flags of the activity.
        name : `str`
            The activity's name.
        party : `None`, ``ActivityParty``
            The activity's party.
        secrets : `None`, ``ActivitySecrets``
            The activity's secrets.
        session_id : `None`, `str`
            Spotify activity's session's id. 
        state : `None`, `str`
            The player's current party status.
        sync_id : `None`, `str`
            The id of the currently playing track of a spotify activity.
        timestamps : `None`, ``ActivityTimestamps``
            The activity's timestamps.
        url : `None`, `str`, Optional
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
        new.created_at = created_at
        new.details = details
        new.flags = flags
        new.id = activity_id
        new.name = name
        new.party = party
        new.secrets = secrets
        new.session_id = session_id
        new.state = state
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
            created_at = keyword_parameters.pop('created_at', ...),
            details = keyword_parameters.pop('details', ...),
            flags = keyword_parameters.pop('flags', ...),
            name = keyword_parameters.pop('name', ...),
            party = keyword_parameters.pop('party', ...),
            secrets = keyword_parameters.pop('secrets', ...),
            session_id = keyword_parameters.pop('session_id', ...),
            state = keyword_parameters.pop('state', ...),
            sync_id = keyword_parameters.pop('sync_id', ...),
            timestamps = keyword_parameters.pop('timestamps', ...),
            url = keyword_parameters.pop('url', ...),
        )
