from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...activity_assets import ActivityAssets
from ...activity_party import ActivityParty
from ...activity_secrets import ActivitySecrets
from ...activity_timestamps import ActivityTimestamps

from ..flags import ActivityFlag
from ..rich import ActivityMetadataRich


def _assert_fields_set(activity_metadata):
    """
    Asserts whether every fields are set of the given activity metadata.
    
    Parameters
    ----------
    activity_metadata : ``ActivityMetadataRich``
        The activity metadata to check.
    """
    vampytest.assert_instance(activity_metadata, ActivityMetadataRich)
    vampytest.assert_instance(activity_metadata.application_id, int)
    vampytest.assert_instance(activity_metadata.assets, ActivityAssets, nullable = True)
    vampytest.assert_instance(activity_metadata.created_at, DateTime, nullable = True)
    vampytest.assert_instance(activity_metadata.details, str, nullable = True)
    vampytest.assert_instance(activity_metadata.flags, ActivityFlag)
    vampytest.assert_instance(activity_metadata.id, int)
    vampytest.assert_instance(activity_metadata.name, str)
    vampytest.assert_instance(activity_metadata.party, ActivityParty, nullable = True)
    vampytest.assert_instance(activity_metadata.secrets, ActivitySecrets, nullable = True)
    vampytest.assert_instance(activity_metadata.session_id, str, nullable = True)
    vampytest.assert_instance(activity_metadata.state, str, nullable = True)
    vampytest.assert_instance(activity_metadata.sync_id, str, nullable = True)
    vampytest.assert_instance(activity_metadata.timestamps, ActivityTimestamps, nullable = True)
    vampytest.assert_instance(activity_metadata.url, str, nullable = True)
    

def test__ActivityMetadataRich__new__0():
    """
    Tests whether ``ActivityMetadataRich.__new__`` works as intended.
    
    Case: no fields given.
    """
    activity_metadata = ActivityMetadataRich()
    _assert_fields_set(activity_metadata)


def test__ActivityMetadataRich__new__1():
    """
    Tests whether ``ActivityMetadataRich.__new__`` works as intended.
    
    Case: all fields given.
    """
    application_id = 202209070000
    assets = ActivityAssets(image_large = 'senya')
    created_at = DateTime(2014, 9, 11, tzinfo = TimeZone.utc)
    details = 'vocal'
    flags = ActivityFlag(1)
    activity_id = 202209070001
    name = 'Iceon'
    party = ActivityParty(party_id = 'Kamase-Tora')
    secrets = ActivitySecrets(join = 'deitarabochi')
    session_id = 'Autobahn'
    state = 'plain'
    sync_id = 'asia'
    timestamps = ActivityTimestamps(
        end = DateTime(2014, 9, 12, tzinfo = TimeZone.utc),
        start = DateTime(2014, 9, 10, tzinfo = TimeZone.utc),
    )
    url = 'https://www.astil.dev/'
    
    activity_metadata = ActivityMetadataRich(
        application_id = application_id,
        assets = assets,
        created_at = created_at,
        details = details,
        flags = flags,
        activity_id = activity_id,
        name = name,
        party = party,
        secrets = secrets,
        session_id = session_id,
        state = state,
        sync_id = sync_id,
        timestamps = timestamps,
        url = url,
    )
    _assert_fields_set(activity_metadata)
    
    vampytest.assert_eq(activity_metadata.application_id, application_id)
    vampytest.assert_eq(activity_metadata.assets, assets)
    vampytest.assert_eq(activity_metadata.created_at, created_at)
    vampytest.assert_eq(activity_metadata.details, details)
    vampytest.assert_eq(activity_metadata.flags, flags)
    vampytest.assert_eq(activity_metadata.id, activity_id)
    vampytest.assert_eq(activity_metadata.name, name)
    vampytest.assert_eq(activity_metadata.party, party)
    vampytest.assert_eq(activity_metadata.secrets, secrets)
    vampytest.assert_eq(activity_metadata.session_id, session_id)
    vampytest.assert_eq(activity_metadata.state, state)
    vampytest.assert_eq(activity_metadata.sync_id, sync_id)
    vampytest.assert_eq(activity_metadata.timestamps, timestamps)
    vampytest.assert_eq(activity_metadata.url, url)


def test__ActivityMetadataRich__from_keyword_parameters__0():
    """
    Tests whether ``ActivityMetadataRich.from_keyword_parameters`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    activity_metadata = ActivityMetadataRich.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(activity_metadata)
    
    vampytest.assert_eq(keyword_parameters, {})


def test__ActivityMetadataRich__from_keyword_parameters__1():
    """
    Tests whether ``ActivityMetadataRich.from_keyword_parameters`` works as intended.
    
    Case: all fields given.
    """
    application_id = 202304090000
    assets = ActivityAssets(image_large = 'senya')
    created_at = DateTime(2014, 9, 11, tzinfo = TimeZone.utc)
    details = 'vocal'
    flags = ActivityFlag(1)
    activity_id = 202304090001
    name = 'Iceon'
    party = ActivityParty(party_id = 'Kamase-Tora')
    secrets = ActivitySecrets(join = 'deitarabochi')
    session_id = 'Autobahn'
    state = 'plain'
    sync_id = 'asia'
    timestamps = ActivityTimestamps(
        end = DateTime(2014, 9, 12, tzinfo = TimeZone.utc),
        start = DateTime(2014, 9, 10, tzinfo = TimeZone.utc),
    )
    url = 'https://www.astil.dev/'
    
    keyword_parameters = {
        'application_id': application_id,
        'assets': assets,
        'created_at': created_at,
        'details': details,
        'flags': flags,
        'activity_id': activity_id,
        'name': name,
        'party': party,
        'secrets': secrets,
        'session_id': session_id,
        'state': state,
        'sync_id': sync_id,
        'timestamps': timestamps,
        'url': url,
    }
    activity_metadata = ActivityMetadataRich.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(activity_metadata)
    
    vampytest.assert_eq(keyword_parameters, {})
    
    vampytest.assert_eq(activity_metadata.application_id, application_id)
    vampytest.assert_eq(activity_metadata.assets, assets)
    vampytest.assert_eq(activity_metadata.created_at, created_at)
    vampytest.assert_eq(activity_metadata.details, details)
    vampytest.assert_eq(activity_metadata.flags, flags)
    vampytest.assert_eq(activity_metadata.id, activity_id)
    vampytest.assert_eq(activity_metadata.name, name)
    vampytest.assert_eq(activity_metadata.party, party)
    vampytest.assert_eq(activity_metadata.secrets, secrets)
    vampytest.assert_eq(activity_metadata.session_id, session_id)
    vampytest.assert_eq(activity_metadata.state, state)
    vampytest.assert_eq(activity_metadata.sync_id, sync_id)
    vampytest.assert_eq(activity_metadata.timestamps, timestamps)
    vampytest.assert_eq(activity_metadata.url, url)
