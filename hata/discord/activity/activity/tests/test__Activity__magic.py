from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...activity_assets import ActivityAssets
from ...activity_party import ActivityParty
from ...activity_secrets import ActivitySecrets
from ...activity_timestamps import ActivityTimestamps
from ...activity_metadata import ActivityFlag

from ..activity import Activity
from ..preinstanced import ActivityType


def test__Activity__hash():
    """
    Tests whether ``Activity.__hash__`` works as expected.
    """
    name = 'Iceon'
    activity_type = ActivityType.playing
    
    application_id = 202408310000
    assets = ActivityAssets(image_large = 'senya')
    buttons = ['Party', 'Trick']
    created_at = DateTime(2014, 9, 11, tzinfo = TimeZone.utc)
    details = 'vocal'
    flags = ActivityFlag(1)
    activity_id = 202408310001
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
    
    activity = Activity(
        name,
        activity_type = activity_type,
        application_id = application_id,
        assets = assets,
        buttons = buttons,
        created_at = created_at,
        details = details,
        flags = flags,
        activity_id = activity_id,
        party = party,
        secrets = secrets,
        session_id = session_id,
        state = state,
        sync_id = sync_id,
        timestamps = timestamps,
        url = url,
    )
    
    output = hash(activity)
    vampytest.assert_instance(output, int)


def test__Activity__repr():
    """
    Tests whether ``Activity.__repr__`` works as expected.
    """
    name = 'Iceon'
    activity_type = ActivityType.playing
    
    application_id = 202408310002
    assets = ActivityAssets(image_large = 'senya')
    buttons = ['Party', 'Trick']
    created_at = DateTime(2014, 9, 11, tzinfo = TimeZone.utc)
    details = 'vocal'
    flags = ActivityFlag(1)
    activity_id = 202408310004
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
    
    activity = Activity(
        name,
        activity_type = activity_type,
        application_id = application_id,
        assets = assets,
        buttons = buttons,
        created_at = created_at,
        details = details,
        flags = flags,
        activity_id = activity_id,
        party = party,
        secrets = secrets,
        session_id = session_id,
        state = state,
        sync_id = sync_id,
        timestamps = timestamps,
        url = url,
    )
    
    output = repr(activity)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    name = ''
    activity_type = ActivityType.playing
    
    keyword_parameters = {
        'name': name,
        'activity_type': activity_type,
    }
        
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )

    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__Activity__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``Activity.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    activity_0 = Activity(**keyword_parameters_0)
    activity_1 = Activity(**keyword_parameters_1)
    
    output = activity_0 == activity_1
    vampytest.assert_instance(output, bool)
    return output
