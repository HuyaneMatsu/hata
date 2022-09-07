from datetime import datetime as DateTime

import vampytest

from ... import ActivityAssets, ActivityFlag, ActivityParty, ActivitySecrets, ActivityTimestamps

from .. import RichActivityMetadata


def test__RichActivityMetadata__new__0():
    """
    Tests whether ``RichActivityMetadata.__new__`` works as intended.
    
    Case: no fields given.
    """
    keyword_parameters = {}
    activity_metadata = RichActivityMetadata(keyword_parameters)
    
    vampytest.assert_instance(activity_metadata, RichActivityMetadata)
    vampytest.assert_eq(keyword_parameters, {})

    vampytest.assert_instance(activity_metadata.application_id, int)
    vampytest.assert_instance(activity_metadata.assets, ActivityAssets, nullable=True)
    vampytest.assert_instance(activity_metadata.created_at, DateTime, nullable=True)
    vampytest.assert_instance(activity_metadata.details, str, nullable=True)
    vampytest.assert_instance(activity_metadata.flags, ActivityFlag)
    vampytest.assert_instance(activity_metadata.id, int)
    vampytest.assert_instance(activity_metadata.name, str)
    vampytest.assert_instance(activity_metadata.party, ActivityParty, nullable=True)
    vampytest.assert_instance(activity_metadata.secrets, ActivitySecrets, nullable=True)
    vampytest.assert_instance(activity_metadata.session_id, str, nullable=True)
    vampytest.assert_instance(activity_metadata.state, str, nullable=True)
    vampytest.assert_instance(activity_metadata.sync_id, str, nullable=True)
    vampytest.assert_instance(activity_metadata.timestamps, ActivityTimestamps, nullable=True)
    vampytest.assert_instance(activity_metadata.url, str, nullable=True)


def test__RichActivityMetadata__new__1():
    """
    Tests whether ``RichActivityMetadata.__new__`` works as intended.
    
    Case: all fields given.
    """
    application_id = 202209070000
    assets = ActivityAssets(image_large='senya')
    created_at = DateTime(2014, 9, 11)
    details = 'vocal'
    flags = ActivityFlag(1)
    id_ = 202209070001
    name = 'Iceon'
    party = ActivityParty(id_='Kamase-Tora')
    secrets = ActivitySecrets(join='deitarabochi')
    session_id = 'Autobahn'
    state = 'plain'
    sync_id = 'asia'
    timestamps = ActivityTimestamps(end=DateTime(2014, 9, 12), start=DateTime(2014, 9, 10))
    url = 'https://www.astil.dev/'
    
    keyword_parameters = {
        'application_id': application_id,
        'assets': assets,
        'created_at': created_at,
        'details': details,
        'flags': flags,
        'id_': id_,
        'name': name,
        'party': party,
        'secrets': secrets,
        'session_id': session_id,
        'state': state,
        'sync_id': sync_id,
        'timestamps': timestamps,
        'url': url,
    }
    activity_metadata = RichActivityMetadata(keyword_parameters)
    
    vampytest.assert_instance(activity_metadata, RichActivityMetadata)
    vampytest.assert_eq(keyword_parameters, {})
    
    vampytest.assert_eq(activity_metadata.application_id, application_id)
    vampytest.assert_eq(activity_metadata.assets, assets)
    vampytest.assert_eq(activity_metadata.created_at, created_at)
    vampytest.assert_eq(activity_metadata.details, details)
    vampytest.assert_eq(activity_metadata.flags, flags)
    vampytest.assert_eq(activity_metadata.id, id_)
    vampytest.assert_eq(activity_metadata.name, name)
    vampytest.assert_eq(activity_metadata.party, party)
    vampytest.assert_eq(activity_metadata.secrets, secrets)
    vampytest.assert_eq(activity_metadata.session_id, session_id)
    vampytest.assert_eq(activity_metadata.state, state)
    vampytest.assert_eq(activity_metadata.sync_id, sync_id)
    vampytest.assert_eq(activity_metadata.timestamps, timestamps)
    vampytest.assert_eq(activity_metadata.url, url)
