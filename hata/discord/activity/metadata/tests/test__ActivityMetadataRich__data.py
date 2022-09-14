from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_millisecond_unix_time

from ... import ActivityAssets, ActivityFlag, ActivityParty, ActivitySecrets, ActivityTimestamps

from .. import ActivityMetadataRich


def test__ActivityMetadataRich__from_data__0():
    """
    Tests whether ``ActivityMetadataRich.from_data`` works as intended.
    
    Case: No fields given.
    """
    activity_metadata = ActivityMetadataRich.from_data({})
    
    vampytest.assert_instance(activity_metadata, ActivityMetadataRich)
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


def test__ActivityMetadataRich__from_data__1():
    """
    Tests whether ``ActivityMetadataRich.from_data`` works as intended.
    
    Case: All fields given.
    """
    application_id = 202209070002
    assets = ActivityAssets(image_large='senya')
    created_at = DateTime(2014, 9, 11)
    details = 'vocal'
    flags = ActivityFlag(1)
    id_ = 202209070003
    name = 'Iceon'
    party = ActivityParty(id_='Kamase-Tora')
    secrets = ActivitySecrets(join='deitarabochi')
    session_id = 'Autobahn'
    state = 'plain'
    sync_id = 'asia'
    timestamps = ActivityTimestamps(end=DateTime(2014, 9, 12), start=DateTime(2014, 9, 10))
    url = 'https://www.astil.dev/'
    
    activity_metadata = ActivityMetadataRich.from_data({
        'application_id': str(application_id),
        'assets': assets.to_data(),
        'created_at': datetime_to_millisecond_unix_time(created_at),
        'details': details,
        'flags': int(flags),
        'id': format(id_, 'x'),
        'name': name,
        'party': party.to_data(),
        'secrets': secrets.to_data(),
        'session_id': session_id,
        'state': state,
        'sync_id': sync_id,
        'timestamps': timestamps.to_data(),
        'url': url,
    })
    
    vampytest.assert_instance(activity_metadata, ActivityMetadataRich)
    
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


def test__ActivityMetadataRich__to_data():
    """
    Tests whether ``ActivityMetadataRich.to_data`` works as intended.
    """
    application_id = 202209070004
    assets = ActivityAssets(image_large='senya')
    created_at = DateTime(2014, 9, 11)
    details = 'vocal'
    flags = ActivityFlag(1)
    id_ = 202209070005
    name = 'Iceon'
    party = ActivityParty(id_='Kamase-Tora')
    secrets = ActivitySecrets(join='deitarabochi')
    session_id = 'Autobahn'
    state = 'plain'
    sync_id = 'asia'
    timestamps = ActivityTimestamps(end=DateTime(2014, 9, 12), start=DateTime(2014, 9, 10))
    url = 'https://www.astil.dev/'
    
    data = ActivityMetadataRich({
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
    }).to_data()
    
    vampytest.assert_in('name', data)
    vampytest.assert_in('url', data)
    
    vampytest.assert_eq(data['name'], name)
    vampytest.assert_eq(data['url'], url)
    
    vampytest.assert_not_in('application_id', data)
    vampytest.assert_not_in('assets', data)
    vampytest.assert_not_in('created_at', data)
    vampytest.assert_not_in('details', data)
    vampytest.assert_not_in('flags', data)
    vampytest.assert_not_in('id', data)
    vampytest.assert_not_in('party', data)
    vampytest.assert_not_in('secrets', data)
    vampytest.assert_not_in('session_id', data)
    vampytest.assert_not_in('state', data)
    vampytest.assert_not_in('sync_id', data)
    vampytest.assert_not_in('timestamps', data)


def test__ActivityMetadataRich__to_data__user():
    """
    Tests whether `ActivityMetadataRich.to_data(user = True)` works as intended.
    """
    application_id = 202209070006
    assets = ActivityAssets(image_large='senya')
    created_at = DateTime(2014, 9, 11)
    details = 'vocal'
    flags = ActivityFlag(1)
    id_ = 202209070007
    name = 'Iceon'
    party = ActivityParty(id_='Kamase-Tora')
    secrets = ActivitySecrets(join='deitarabochi')
    session_id = 'Autobahn'
    state = 'plain'
    sync_id = 'asia'
    timestamps = ActivityTimestamps(end=DateTime(2014, 9, 12), start=DateTime(2014, 9, 10))
    url = 'https://www.astil.dev/'
    
    data = ActivityMetadataRich({
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
    }).to_data(user = True)
    
    vampytest.assert_in('assets', data)
    vampytest.assert_in('details', data)
    vampytest.assert_in('name', data)
    vampytest.assert_in('party', data)
    vampytest.assert_in('secrets', data)
    vampytest.assert_in('state', data)
    vampytest.assert_in('timestamps', data)
    vampytest.assert_in('url', data)
    
    vampytest.assert_eq(data['assets'], assets.to_data())
    vampytest.assert_eq(data['details'], details)
    vampytest.assert_eq(data['name'], name)
    vampytest.assert_eq(data['party'], party.to_data())
    vampytest.assert_eq(data['secrets'], secrets.to_data())
    vampytest.assert_eq(data['state'], state)
    vampytest.assert_eq(data['timestamps'], timestamps.to_data())
    vampytest.assert_eq(data['url'], url)
    
    vampytest.assert_not_in('application_id', data)
    vampytest.assert_not_in('created_at', data)
    vampytest.assert_not_in('flags', data)
    vampytest.assert_not_in('id', data)
    vampytest.assert_not_in('session_id', data)
    vampytest.assert_not_in('sync_id', data)


def test__ActivityMetadataRich__to_data__include_internals():
    """
    Tests whether `ActivityMetadataRich.to_data(include_internals = True)` works as intended.
    """
    application_id = 202209070008
    assets = ActivityAssets(image_large='senya')
    created_at = DateTime(2014, 9, 11)
    details = 'vocal'
    flags = ActivityFlag(1)
    id_ = 202209070009
    name = 'Iceon'
    party = ActivityParty(id_='Kamase-Tora')
    secrets = ActivitySecrets(join='deitarabochi')
    session_id = 'Autobahn'
    state = 'plain'
    sync_id = 'asia'
    timestamps = ActivityTimestamps(end=DateTime(2014, 9, 12), start=DateTime(2014, 9, 10))
    url = 'https://www.astil.dev/'
    
    data = ActivityMetadataRich({
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
    }).to_data(include_internals = True)
    
    vampytest.assert_in('application_id', data)
    vampytest.assert_in('assets', data)
    vampytest.assert_in('created_at', data)
    vampytest.assert_in('details', data)
    vampytest.assert_in('flags', data)
    vampytest.assert_in('name', data)
    vampytest.assert_in('party', data)
    vampytest.assert_in('secrets', data)
    vampytest.assert_in('session_id', data)
    vampytest.assert_in('state', data)
    vampytest.assert_in('sync_id', data)
    vampytest.assert_in('timestamps', data)
    vampytest.assert_in('url', data)
    
    vampytest.assert_eq(data['application_id'], str(application_id))
    vampytest.assert_eq(data['assets'], assets.to_data())
    vampytest.assert_eq(data['created_at'], datetime_to_millisecond_unix_time(created_at))
    vampytest.assert_eq(data['details'], details)
    vampytest.assert_eq(data['flags'], flags)
    vampytest.assert_eq(data['name'], name)
    vampytest.assert_eq(data['party'], party.to_data())
    vampytest.assert_eq(data['secrets'], secrets.to_data())
    vampytest.assert_eq(data['session_id'], session_id)
    vampytest.assert_eq(data['state'], state)
    vampytest.assert_eq(data['sync_id'], sync_id)
    vampytest.assert_eq(data['timestamps'], timestamps.to_data())
    vampytest.assert_eq(data['url'], url)
    
    vampytest.assert_not_in('id', data)


def test__ActivityMetadataRich__update_attributes():
    """
    Tests whether ``ActivityMetadataRich._update_attributes`` works as intended.
    """
    application_id = 202209070010
    old_assets = ActivityAssets(image_large='senya')
    new_assets = ActivityAssets(image_small='merami')
    old_created_at = DateTime(2014, 9, 11)
    new_created_at = DateTime(2012, 9, 11)
    old_details = 'vocal'
    new_details = 'pop'
    old_flags = ActivityFlag(1)
    new_flags = ActivityFlag(2)
    id_ = 202209070011
    old_name = 'Iceon'
    new_name = 'Worldly'
    old_party = ActivityParty(id_='Kamase-Tora')
    new_party = ActivityParty(max_ = 12, size = 6)
    old_secrets = ActivitySecrets(join='deitarabochi')
    new_secrets = ActivitySecrets(join='Flower')
    old_session_id = 'Autobahn'
    new_session_id = 'flower'
    old_state = 'plain'
    new_state = 'land'
    old_sync_id = 'asia'
    new_sync_id = 'past'
    old_timestamps = ActivityTimestamps(end=DateTime(2014, 9, 12), start=DateTime(2014, 9, 10))
    new_timestamps = ActivityTimestamps(end=DateTime(2012, 9, 12), start=DateTime(2012, 9, 10))
    old_url = 'https://www.astil.dev/'
    new_url = 'https://www.astil.dev/project/hata/'

    activity_metadata = ActivityMetadataRich({
        'application_id': application_id,
        'assets': old_assets,
        'created_at': old_created_at,
        'details': old_details,
        'flags': old_flags,
        'id_': id_,
        'name': old_name,
        'party': old_party,
        'secrets': old_secrets,
        'session_id': old_session_id,
        'state': old_state,
        'sync_id': old_sync_id,
        'timestamps': old_timestamps,
        'url': old_url,
    })
    
    activity_metadata._update_attributes({
        'assets': new_assets.to_data(),
        'created_at': datetime_to_millisecond_unix_time(new_created_at),
        'details': new_details,
        'flags': int(new_flags),
        'name': new_name,
        'party': new_party.to_data(),
        'secrets': new_secrets.to_data(),
        'session_id': new_session_id,
        'state': new_state,
        'sync_id': new_sync_id,
        'timestamps': new_timestamps.to_data(),
        'url': new_url,
    })

    vampytest.assert_eq(activity_metadata.assets, new_assets)
    vampytest.assert_eq(activity_metadata.created_at, new_created_at)
    vampytest.assert_eq(activity_metadata.details, new_details)
    vampytest.assert_eq(activity_metadata.flags, new_flags)
    vampytest.assert_eq(activity_metadata.name, new_name)
    vampytest.assert_eq(activity_metadata.party, new_party)
    vampytest.assert_eq(activity_metadata.secrets, new_secrets)
    vampytest.assert_eq(activity_metadata.session_id, new_session_id)
    vampytest.assert_eq(activity_metadata.state, new_state)
    vampytest.assert_eq(activity_metadata.sync_id, new_sync_id)
    vampytest.assert_eq(activity_metadata.timestamps, new_timestamps)
    vampytest.assert_eq(activity_metadata.url, new_url)


def test__ActivityMetadataRich__difference_update_attributes():
    """
    Tests whether ``ActivityMetadataRich._difference_update_attributes`` works as intended.
    """
    application_id = 202209070012
    old_assets = ActivityAssets(image_large='senya')
    new_assets = ActivityAssets(image_small='merami')
    old_created_at = DateTime(2014, 9, 11)
    new_created_at = DateTime(2012, 9, 11)
    old_details = 'vocal'
    new_details = 'pop'
    old_flags = ActivityFlag(1)
    new_flags = ActivityFlag(2)
    id_ = 202209070013
    old_name = 'Iceon'
    new_name = 'Worldly'
    old_party = ActivityParty(id_='Kamase-Tora')
    new_party = ActivityParty(max_ = 12, size = 6)
    old_secrets = ActivitySecrets(join='deitarabochi')
    new_secrets = ActivitySecrets(join='Flower')
    old_session_id = 'Autobahn'
    new_session_id = 'flower'
    old_state = 'plain'
    new_state = 'land'
    old_sync_id = 'asia'
    new_sync_id = 'past'
    old_timestamps = ActivityTimestamps(end=DateTime(2014, 9, 12), start=DateTime(2014, 9, 10))
    new_timestamps = ActivityTimestamps(end=DateTime(2012, 9, 12), start=DateTime(2012, 9, 10))
    old_url = 'https://www.astil.dev/'
    new_url = 'https://www.astil.dev/project/hata/'

    activity_metadata = ActivityMetadataRich({
        'application_id': application_id,
        'assets': old_assets,
        'created_at': old_created_at,
        'details': old_details,
        'flags': old_flags,
        'id_': id_,
        'name': old_name,
        'party': old_party,
        'secrets': old_secrets,
        'session_id': old_session_id,
        'state': old_state,
        'sync_id': old_sync_id,
        'timestamps': old_timestamps,
        'url': old_url,
    })
    
    old_attributes = activity_metadata._difference_update_attributes({
        'assets': new_assets.to_data(),
        'created_at': datetime_to_millisecond_unix_time(new_created_at),
        'details': new_details,
        'flags': int(new_flags),
        'name': new_name,
        'party': new_party.to_data(),
        'secrets': new_secrets.to_data(),
        'session_id': new_session_id,
        'state': new_state,
        'sync_id': new_sync_id,
        'timestamps': new_timestamps.to_data(),
        'url': new_url,
    })
    
    vampytest.assert_eq(activity_metadata.assets, new_assets)
    vampytest.assert_eq(activity_metadata.created_at, new_created_at)
    vampytest.assert_eq(activity_metadata.details, new_details)
    vampytest.assert_eq(activity_metadata.flags, new_flags)
    vampytest.assert_eq(activity_metadata.name, new_name)
    vampytest.assert_eq(activity_metadata.party, new_party)
    vampytest.assert_eq(activity_metadata.secrets, new_secrets)
    vampytest.assert_eq(activity_metadata.session_id, new_session_id)
    vampytest.assert_eq(activity_metadata.state, new_state)
    vampytest.assert_eq(activity_metadata.sync_id, new_sync_id)
    vampytest.assert_eq(activity_metadata.timestamps, new_timestamps)
    vampytest.assert_eq(activity_metadata.url, new_url)
    
    vampytest.assert_in('assets', old_attributes)
    vampytest.assert_in('created_at', old_attributes)
    vampytest.assert_in('details', old_attributes)
    vampytest.assert_in('flags', old_attributes)
    vampytest.assert_in('name', old_attributes)
    vampytest.assert_in('party', old_attributes)
    vampytest.assert_in('secrets', old_attributes)
    vampytest.assert_in('session_id', old_attributes)
    vampytest.assert_in('state', old_attributes)
    vampytest.assert_in('sync_id', old_attributes)
    vampytest.assert_in('timestamps', old_attributes)
    vampytest.assert_in('url', old_attributes)
    
    vampytest.assert_eq(old_attributes['assets'], old_assets)
    vampytest.assert_eq(old_attributes['created_at'], old_created_at)
    vampytest.assert_eq(old_attributes['details'], old_details)
    vampytest.assert_eq(old_attributes['flags'], old_flags)
    vampytest.assert_eq(old_attributes['name'], old_name)
    vampytest.assert_eq(old_attributes['party'], old_party)
    vampytest.assert_eq(old_attributes['secrets'], old_secrets)
    vampytest.assert_eq(old_attributes['session_id'], old_session_id)
    vampytest.assert_eq(old_attributes['state'], old_state)
    vampytest.assert_eq(old_attributes['sync_id'], old_sync_id)
    vampytest.assert_eq(old_attributes['timestamps'], old_timestamps)
    vampytest.assert_eq(old_attributes['url'], old_url)
