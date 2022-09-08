from datetime import datetime as DateTime

import vampytest

from ...emoji import Emoji, create_partial_emoji_data
from ...utils import datetime_to_millisecond_unix_time

from .. import Activity, ActivityAssets, ActivityFlag, ActivityParty, ActivitySecrets, ActivityTimestamps, ActivityType


def iter_activity_datas_by_type():
    name = 'Iceon'
    application_id = 202209070021
    assets = ActivityAssets(image_large = 'senya')
    created_at = DateTime(2014, 9, 11)
    details = 'vocal'
    flags = ActivityFlag(1)
    id_ = 202209070022
    party = ActivityParty(id_ = 'Kamase-Tora')
    secrets = ActivitySecrets(join = 'deitarabochi')
    session_id = 'Autobahn'
    state = 'plain'
    sync_id = 'asia'
    timestamps = ActivityTimestamps(end = DateTime(2014, 9, 12), start = DateTime(2014, 9, 10))
    url = 'https://www.astil.dev/'
    emoji = Emoji.precreate(202209070023, name = 'Princess')
    
    data = {
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
        'emoji': create_partial_emoji_data(emoji)
    }
    
    for type_ in ActivityType.INSTANCES.values():
        yield {**data, 'type': type_.value}


def test__Activity__hash():
    """
    Tests whether ``Activity.__hash__`` works as expected.
    """
    for data in iter_activity_datas_by_type():
        activity = Activity.from_data(data)
        vampytest.assert_instance(hash(activity), int)

def test__Activity__repr():
    """
    Tests whether ``Activity.__repr__`` works as expected.
    """
    for data in iter_activity_datas_by_type():
        activity = Activity.from_data(data)
        vampytest.assert_instance(repr(activity), str)


def test__Activity__eq():
    """
    Tests whether ``Activity.__eq__`` works as expected.
    """
    name = ''
    type_ = ActivityType.game
    
    keyword_parameters = {
        'name': name,
        'type_': type_,
    }
    
    activity = Activity(**keyword_parameters)
    
    vampytest.assert_eq(activity, activity)
    vampytest.assert_ne(activity, object())
    
    for filed_name, field_value in (
        ('name', 'Nue'),
        ('type_', ActivityType.unknown),
    ):
        other_activity = Activity(**{**keyword_parameters, filed_name: field_value})
        
        vampytest.assert_ne(activity, other_activity)
