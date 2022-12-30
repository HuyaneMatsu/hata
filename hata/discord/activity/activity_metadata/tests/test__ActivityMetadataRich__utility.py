from datetime import datetime as DateTime

import vampytest

from ....utils import datetime_to_millisecond_unix_time

from ...activity_assets import ActivityAssets
from ...activity_party import ActivityParty
from ...activity_secrets import ActivitySecrets
from ...activity_timestamps import ActivityTimestamps

from ..flags import ActivityFlag
from ..rich import ActivityMetadataRich

from .test__ActivityMetadataRich__constructor import _assert_fields_set


def test__ActivityMetadataRich__copy():
    """
    Tests whether ``ActivityMetadataRich.copy`` works as intended.
    """
    application_id = 202212300005
    assets = ActivityAssets(image_large = 'senya')
    created_at = DateTime(2014, 9, 11)
    details = 'vocal'
    flags = ActivityFlag(1)
    activity_id = 202212300006
    name = 'Iceon'
    party = ActivityParty(party_id = 'Kamase-Tora')
    secrets = ActivitySecrets(join = 'deitarabochi')
    session_id = 'Autobahn'
    state = 'plain'
    sync_id = 'asia'
    timestamps = ActivityTimestamps(end = DateTime(2014, 9, 12), start = DateTime(2014, 9, 10))
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
    activity_metadata = ActivityMetadataRich(keyword_parameters)
    
    copy = activity_metadata.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, activity_metadata)
    
    vampytest.assert_eq(copy, activity_metadata)


def test__ActivityMetadataRich__copy_with__0():
    """
    Tests whether ``ActivityMetadataRich.copy_with`` works as intended.
    
    Case: No fields given.
    """
    application_id = 202212300007
    assets = ActivityAssets(image_large = 'senya')
    created_at = DateTime(2014, 9, 11)
    details = 'vocal'
    flags = ActivityFlag(1)
    activity_id = 202212300008
    name = 'Iceon'
    party = ActivityParty(party_id = 'Kamase-Tora')
    secrets = ActivitySecrets(join = 'deitarabochi')
    session_id = 'Autobahn'
    state = 'plain'
    sync_id = 'asia'
    timestamps = ActivityTimestamps(end = DateTime(2014, 9, 12), start = DateTime(2014, 9, 10))
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
    activity_metadata = ActivityMetadataRich(keyword_parameters)
    
    keyword_parameters = {}
    copy = activity_metadata.copy_with(keyword_parameters)
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, activity_metadata)
    
    vampytest.assert_eq(copy, activity_metadata)


def test__ActivityMetadataRich__copy_with__1():
    """
    Tests whether ``ActivityMetadataRich.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_application_id = 202212300009
    new_application_id = 202212300010
    old_assets = ActivityAssets(image_large = 'senya')
    new_assets = ActivityAssets(image_small='merami')
    old_created_at = DateTime(2014, 9, 11)
    new_created_at = DateTime(2012, 9, 11)
    old_details = 'vocal'
    new_details = 'pop'
    old_flags = ActivityFlag(1)
    new_flags = ActivityFlag(2)
    old_activity_id = 202212300011
    new_activity_id = 202212300012
    old_name = 'Iceon'
    new_name = 'Worldly'
    old_party = ActivityParty(party_id = 'Kamase-Tora')
    new_party = ActivityParty(max_ = 12, size = 6)
    old_secrets = ActivitySecrets(join = 'deitarabochi')
    new_secrets = ActivitySecrets(join = 'Flower')
    old_session_id = 'Autobahn'
    new_session_id = 'flower'
    old_state = 'plain'
    new_state = 'land'
    old_sync_id = 'asia'
    new_sync_id = 'past'
    old_timestamps = ActivityTimestamps(end = DateTime(2014, 9, 12), start = DateTime(2014, 9, 10))
    new_timestamps = ActivityTimestamps(end = DateTime(2012, 9, 12), start = DateTime(2012, 9, 10))
    old_url = 'https://www.astil.dev/'
    new_url = 'https://www.astil.dev/project/hata/'
    
    keyword_parameters = {
        'application_id': old_application_id,
        'assets': old_assets,
        'created_at': old_created_at,
        'details': old_details,
        'flags': old_flags,
        'activity_id': old_activity_id,
        'name': old_name,
        'party': old_party,
        'secrets': old_secrets,
        'session_id': old_session_id,
        'state': old_state,
        'sync_id': old_sync_id,
        'timestamps': old_timestamps,
        'url': old_url,
    }
    activity_metadata = ActivityMetadataRich(keyword_parameters)
    
    keyword_parameters = {
        'application_id': new_application_id,
        'assets': new_assets,
        'created_at': new_created_at,
        'details': new_details,
        'flags': new_flags,
        'activity_id': new_activity_id,
        'name': new_name,
        'party': new_party,
        'secrets': new_secrets,
        'session_id': new_session_id,
        'state': new_state,
        'sync_id': new_sync_id,
        'timestamps': new_timestamps,
        'url': new_url,
    }
    copy = activity_metadata.copy_with(keyword_parameters)
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, activity_metadata)
    
    vampytest.assert_eq(copy.application_id, new_application_id)
    vampytest.assert_eq(copy.assets, new_assets)
    vampytest.assert_eq(copy.created_at, new_created_at)
    vampytest.assert_eq(copy.details, new_details)
    vampytest.assert_eq(copy.flags, new_flags)
    vampytest.assert_eq(copy.id, new_activity_id)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.party, new_party)
    vampytest.assert_eq(copy.secrets, new_secrets)
    vampytest.assert_eq(copy.session_id, new_session_id)
    vampytest.assert_eq(copy.state, new_state)
    vampytest.assert_eq(copy.sync_id, new_sync_id)
    vampytest.assert_eq(copy.timestamps, new_timestamps)
    vampytest.assert_eq(copy.url, new_url)
