from datetime import datetime as DateTime

import vampytest

from ... import ActivityAssets, ActivityFlag, ActivityParty, ActivitySecrets, ActivityTimestamps

from .. import ActivityMetadataRich


def test__ActivityMetadataRich__repr():
    """
    Tests whether ``ActivityMetadataRich.__repr__`` works as intended.
    """
    application_id = 202209070013
    assets = ActivityAssets(image_large='senya')
    created_at = DateTime(2014, 9, 11)
    details = 'vocal'
    flags = ActivityFlag(1)
    id_ = 202209070014
    name = 'Iceon'
    party = ActivityParty(id_='Kamase-Tora')
    secrets = ActivitySecrets(join='deitarabochi')
    session_id = 'Autobahn'
    state = 'plain'
    sync_id = 'asia'
    timestamps = ActivityTimestamps(end=DateTime(2014, 9, 12), start=DateTime(2014, 9, 10))
    url = 'https://www.astil.dev/'
    
    activity_metadata = ActivityMetadataRich({
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
    })
    
    vampytest.assert_instance(repr(activity_metadata), str)


def test__ActivityMetadataRich__hash():
    """
    Tests whether ``ActivityMetadataRich.__hash__`` works as intended.
    """
    application_id = 202209070015
    assets = ActivityAssets(image_large='senya')
    created_at = DateTime(2014, 9, 11)
    details = 'vocal'
    flags = ActivityFlag(1)
    id_ = 202209070016
    name = 'Iceon'
    party = ActivityParty(id_='Kamase-Tora')
    secrets = ActivitySecrets(join='deitarabochi')
    session_id = 'Autobahn'
    state = 'plain'
    sync_id = 'asia'
    timestamps = ActivityTimestamps(end=DateTime(2014, 9, 12), start=DateTime(2014, 9, 10))
    url = 'https://www.astil.dev/'
    
    activity_metadata = ActivityMetadataRich({
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
    })
    
    vampytest.assert_instance(hash(activity_metadata), int)


def test__ActivityMetadataRich__eq():
    """
    Tests whether ``ActivityMetadataRich.__eq__`` works as intended.
    """
    application_id = 202209070017
    assets = ActivityAssets(image_large='senya')
    created_at = DateTime(2014, 9, 11)
    details = 'vocal'
    flags = ActivityFlag(1)
    id_ = 202209070018
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
    activity_metadata = ActivityMetadataRich(keyword_parameters.copy())
    
    vampytest.assert_eq(activity_metadata, activity_metadata)
    vampytest.assert_ne(activity_metadata, object())
    
    for field_name, field_value in (
        ('application_id', 0),
        ('assets', None),
        ('created_at', None),
        ('details', None),
        ('flags', ActivityFlag(0)),
        ('id_', 0),
        ('name', ''),
        ('party', None),
        ('secrets', None),
        ('session_id', None),
        ('state', None),
        ('sync_id', None),
        ('timestamps', None),
        ('url', None),
    ):
        temporary_activity_metadata = ActivityMetadataRich({**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(temporary_activity_metadata, activity_metadata)
