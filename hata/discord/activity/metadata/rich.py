__all__ = ('ActivityMetadataRich',)

import warnings
from datetime import datetime

from scarletio import copy_docs

from ...preconverters import preconvert_flag, preconvert_snowflake, preconvert_str
from ...utils import datetime_to_millisecond_unix_time, is_url, millisecond_unix_time_to_datetime

from ..fields import ActivityAssets, ActivityParty, ActivitySecrets, ActivityTimestamps
from ..flags import ActivityFlag

from .base import ActivityMetadataBase


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
        The activity's party.
    secrets : `None`, ``ActivitySecrets``
        The activity's secrets. Defaults to `None`.
    session_id : `None`, `str`
        Spotify activity's session's id. Defaults to `None`.
    state : `None`, `str`
        The player's current party status. Defaults to `None`.
    sync_id : `None`, `str`
        The ID of the currently playing track of a spotify activity. Defaults to `None`.
    timestamps : `None`, ``ActivityTimestamps``
        The activity's timestamps.
    url : `None`, `str`
        The url of the stream (Twitch or Youtube only). Defaults to `None`.
    """
    __slots__ = (
        'application_id', 'assets', 'created_at', 'details', 'flags', 'id', 'name', 'party', 'secrets', 'session_id',
        'state', 'sync_id', 'timestamps', 'url'
    )
    
    @copy_docs(ActivityMetadataBase.__new__)
    def __new__(cls, keyword_parameters):
        # application_id
        try:
            application_id = keyword_parameters.pop('application_id')
        except KeyError:
            application_id = 0
        else:
            application_id = preconvert_snowflake(application_id, 'application_id')
        
        # assets
        try:
            assets = keyword_parameters.pop('assets')
        except KeyError:
            assets = None
        else:
            if (assets is not None) and (not isinstance(assets, ActivityAssets)):
                raise TypeError(
                    f'`assets` can be `None`, `{ActivityAssets.__name__}`, got '
                    f'{assets.__class__.__name__}; {assets!r}.'
                )
        
        # created_at
        try:
            created_at = keyword_parameters.pop('created_at')
        except KeyError:
            created_at = None
        else:
            if (created_at is not None) and (not isinstance(created_at, datetime)):
                raise TypeError(
                    f'`created_at` can be `datetime`, got {created_at.__class__.__name__}; {created_at!r}.'
                )
        
        # details
        try:
            details = keyword_parameters.pop('details')
        except KeyError:
            details = None
        else:
            if (details is not None):
                details = preconvert_str(details, 'details', 0, 2048)
                if (not details):
                    details = None
        
        # flags
        try:
            flags = keyword_parameters.pop('flags')
        except KeyError:
            flags = ActivityFlag()
        else:
            flags = preconvert_flag(flags, 'flags', ActivityFlag)
        
        try:
            activity_id = keyword_parameters.pop('id_')
        except KeyError:
            pass
        else:
            warnings.warn(
                (
                    f'`{cls.__name__}.__new__`\'s `id_` parameter is deprecated and will be removed in 2023 Marc. '
                    f'Please use `activity_id` instead.'
                ),
                FutureWarning,
                stacklevel = 2,
            )
            
            keyword_parameters['activity_id'] = activity_id
        
        # activity_id
        try:
            activity_id = keyword_parameters.pop('activity_id')
        except KeyError:
            activity_id = 0
        else:
            activity_id = preconvert_snowflake(activity_id, 'activity_id')
        
        # name
        try:
            name = keyword_parameters.pop('name')
        except KeyError:
            name = ''
        else:
            name = preconvert_str(name, 'name', 1, 2048)
        
        # party
        try:
            party = keyword_parameters.pop('party')
        except KeyError:
            party = None
        else:
            if (party is not None) and (not isinstance(party, ActivityParty)):
                raise TypeError(
                    f'`party` can be `None`, `{ActivityParty.__name__}`, got '
                    f'{party.__class__.__name__}; {party!r}.'
                )
        
        # secrets
        try:
            secrets = keyword_parameters.pop('secrets')
        except KeyError:
            secrets = None
        else:
            if (secrets is not None) and (not isinstance(secrets, ActivitySecrets)):
                raise TypeError(
                    f'`secrets` can be `None`, `{ActivitySecrets.__name__}`, got '
                    f'{secrets.__class__.__name__}; {secrets!r}.'
                )
        
        # session_id
        try:
            session_id = keyword_parameters.pop('session_id')
        except KeyError:
            session_id = None
        else:
            if (session_id is not None):
                session_id = preconvert_str(session_id, 'session_id', 0, 2048)
                if (not session_id):
                    session_id = None
        
        # state
        try:
            state = keyword_parameters.pop('state')
        except KeyError:
            state = None
        else:
            if (state is not None):
                state = preconvert_str(state, 'state', 0, 2048)
                if (not state):
                    state = None
        
        # timestamps
        try:
            timestamps = keyword_parameters.pop('timestamps')
        except KeyError:
            timestamps = None
        else:
            if (timestamps is not None) and (not isinstance(timestamps, ActivityTimestamps)):
                raise TypeError(
                    f'`timestamps` can be `None`, `{ActivityTimestamps.__name__}`, got '
                    f'{timestamps.__class__.__name__}; {timestamps!r}.'
                )
        
        # sync_id
        try:
            sync_id = keyword_parameters.pop('sync_id')
        except KeyError:
            sync_id = None
        else:
            if (sync_id is not None):
                sync_id = preconvert_str(sync_id, 'sync_id', 0, 2048)
                if (not sync_id):
                    sync_id = None
        
        # url
        try:
            url = keyword_parameters.pop('url')
        except KeyError:
            url = None
        else:
            if (url is not None):
                url = preconvert_str(url, 'url', 0, 2048)
                if url:
                    assert is_url(url), f'`url` was not given as a valid url, got {url!r}.'
                else:
                    url = None
        
        
        self = object.__new__(cls)
        self.name = name
        
        self.application_id = application_id
        self.details = details
        self.flags = flags
        self.state = state
        self.party = party
        self.assets = assets
        self.secrets = secrets
        self.sync_id = sync_id
        self.session_id = session_id
        self.created_at = created_at
        self.id = activity_id
        self.timestamps = timestamps
        self.url = url
        
        return self
    
    
    @copy_docs(ActivityMetadataBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' name=')
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
        
        # application_id
        application_id = data.get('application_id', None)
        if (application_id is None):
            application_id = 0
        else:
            application_id = int(application_id)
        self.application_id = application_id
        
        # id
        try:
            raw_id = data['id']
        except KeyError:
            id_ = 0
        else:
            try:
                id_ = int(raw_id, base=16)
            except ValueError:
                # Some activity types have `custom` id-s, at those cases we default back to `0`.
                id_ = 0
        
        self.id = id_
        
        self._update_attributes(data)
        return self
    
    
    @copy_docs(ActivityMetadataBase.to_data)
    def to_data(self, *, include_internals=False, user=False):
        data = {}
        
        # name
        data['name'] = self.name
        
        # url
        url = self.url
        if (url is not None):
            data['url'] = url
        
        if user or include_internals:
            # assets
            assets = self.assets
            if (assets is not None) and assets:
                data['assets'] = assets.to_data()
            
            # details
            details = self.details
            if (details is not None):
                data['details'] = details
            
            # party
            party = self.party
            if (party is not None) and party:
                data['party'] = party.to_data()
            
            # secrets
            secrets = self.secrets
            if (secrets is not None) and secrets:
                data['secrets'] = secrets.to_data()
            
            # state
            state = self.state
            if (state is not None):
                data['state'] = state
            
            # timestamps
            timestamps = self.timestamps
            if (timestamps is not None) and timestamps:
                data['timestamps'] = timestamps.to_data()
        
        
        if include_internals:
            # application_id | receive only?
            application_id = self.application_id
            if application_id:
                data['application_id'] = str(application_id)
            
            # created_at | receive only?
            created_at = self.created_at
            if (created_at is not None):
                data['created_at'] = datetime_to_millisecond_unix_time(created_at)
            
            # flags | spotify only
            flags = self.flags
            if flags:
                data['flags'] = int(flags)
            
            # session_id | spotify only
            session_id = self.session_id
            if (session_id is not None):
                data['session_id'] = session_id
            
            # sync_id | spotify only
            sync_id = self.sync_id
            if (sync_id is not None):
                data['sync_id'] = sync_id
        
        return data
    
    
    @copy_docs(ActivityMetadataBase._update_attributes)
    def _update_attributes(self, data):
        # application_id
        # never changes
        
        # assets
        assets_data = data.get('assets', None)
        if (assets_data is None):
            assets = None
        else:
            assets = ActivityAssets.from_data(assets_data)
        self.assets = assets
        
        # created_at
        created_at = data.get('created_at', None)
        if (created_at is not None):
            created_at = millisecond_unix_time_to_datetime(created_at)
        self.created_at = created_at
        
        # details
        self.details = data.get('details', None)
        
        # flags
        self.flags = ActivityFlag(data.get('flags', 0))
        
        # id
        # Never changes
        
        # name
        self.name = data.get('name', '')
        
        # party
        party_data = data.get('party', None)
        if (party_data is None):
            party = None
        else:
            party = ActivityParty.from_data(party_data)
        self.party = party
        
        # secrets
        secrets_data = data.get('secrets', None)
        if (secrets_data is None):
            secrets = None
        else:
            secrets = ActivitySecrets.from_data(secrets_data)
        self.secrets = secrets
        
        # session_id
        self.session_id = data.get('session_id', None)
        
        # state
        self.state = data.get('state', None)
        
        # sync_id
        self.sync_id = data.get('sync_id', None)
        
        # timestamps
        timestamps_data = data.get('timestamps', None)
        if timestamps_data is None:
            timestamps = None
        else:
            timestamps = ActivityTimestamps.from_data(timestamps_data)
        self.timestamps = timestamps
        
        # url
        self.url = data.get('url', None)
    
    
    @copy_docs(ActivityMetadataBase._difference_update_attributes)
    def _difference_update_attributes(self, data):
        old_attributes = {}
        
        # application_id
        application_id = data.get('application_id', None)
        if (application_id is None):
            application_id = 0
        else:
            application_id = int(application_id)
        
        if self.application_id != application_id:
            old_attributes['application_id'] = self.application_id
            self.application_id = application_id
        
        # assets
        assets_data = data.get('assets', None)
        if (assets_data is None):
            assets = None
        else:
            assets = ActivityAssets.from_data(assets_data)
        
        if self.assets != assets:
            old_attributes['assets'] = self.assets
            self.assets = assets
        
        # created_at
        created_at = data.get('created_at', None)
        if created_at is not None:
            created_at = millisecond_unix_time_to_datetime(created_at)
        
        if self.created_at != created_at:
            old_attributes['created_at'] = self.created_at
            self.created_at = created_at
        
        # details
        details = data.get('details', None)
        if self.details != details:
            old_attributes['details'] = self.details
            self.details = details
        
        # flags
        flags = data.get('flags', 0)
        if self.flags != flags:
            old_attributes['flags'] = self.flags
            self.flags = ActivityFlag(flags)
        
        # name
        name = data.get('name', '')
        
        if self.name != name:
            old_attributes['name'] = self.name
            self.name = name
        
        # party
        party_data = data.get('party', None)
        if (party_data is None):
            party = None
        else:
            party = ActivityParty.from_data(party_data)
        
        if self.party != party:
            old_attributes['party'] = self.party
            self.party = party
        
        # secrets
        secrets_data = data.get('secrets', None)
        if (secrets_data is None):
            secrets = None
        else:
            secrets = ActivitySecrets.from_data(secrets_data)
        
        if self.secrets != secrets:
            old_attributes['secrets'] = self.secrets
            self.secrets = secrets
        
        # session_id
        session_id = data.get('session_id', None)
        if self.session_id != session_id:
            old_attributes['session_id'] = self.session_id
            self.session_id = session_id
        
        # state
        state = data.get('state', None)
        
        if self.state != state:
            old_attributes['state'] = self.state
            self.state = state
        
        # sync_id
        sync_id = data.get('sync_id', None)
        if self.sync_id != sync_id:
            old_attributes['sync_id'] = self.sync_id
            self.sync_id = sync_id
        
        # timestamps
        timestamps_data = data.get('timestamps', None)
        if timestamps_data is None:
            timestamps = None
        else:
            timestamps = ActivityTimestamps.from_data(timestamps_data)
        
        if self.timestamps != timestamps:
            old_attributes['timestamps'] = self.timestamps
            self.timestamps = timestamps
        
        # url
        url = data.get('url', None)
        if self.url != url:
            old_attributes['url'] = self.url
            self.url = url
        
        return old_attributes
