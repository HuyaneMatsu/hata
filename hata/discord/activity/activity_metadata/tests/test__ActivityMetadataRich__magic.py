from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...activity_assets import ActivityAssets
from ...activity_party import ActivityParty
from ...activity_secrets import ActivitySecrets
from ...activity_timestamps import ActivityTimestamps

from ..flags import ActivityFlag
from ..rich import ActivityMetadataRich


def test__ActivityMetadataRich__repr():
    """
    Tests whether ``ActivityMetadataRich.__repr__`` works as intended.
    """
    application_id = 202209070013
    assets = ActivityAssets(image_large = 'senya')
    buttons = ['Party', 'Trick']
    created_at = DateTime(2014, 9, 11, tzinfo = TimeZone.utc)
    details = 'vocal'
    details_url = 'https://orindance.party/cart'
    flags = ActivityFlag(1)
    activity_id = 202209070014
    name = 'Iceon'
    party = ActivityParty(party_id = 'Kamase-Tora')
    secrets = ActivitySecrets(join = 'deitarabochi')
    session_id = 'Autobahn'
    state = 'plain'
    state_url = 'https://orindance.party/stand'
    sync_id = 'asia'
    timestamps = ActivityTimestamps(
        end = DateTime(2014, 9, 12, tzinfo = TimeZone.utc),
        start = DateTime(2014, 9, 10, tzinfo = TimeZone.utc),
    )
    url = 'https://www.astil.dev/'
    
    activity_metadata = ActivityMetadataRich(
        application_id = application_id,
        assets = assets,
        buttons = buttons,
        created_at = created_at,
        details = details,
        details_url = details_url,
        flags = flags,
        activity_id = activity_id,
        name = name,
        party = party,
        secrets = secrets,
        session_id = session_id,
        state = state,
        state_url = state_url,
        sync_id = sync_id,
        timestamps = timestamps,
        url = url,
    )
    
    output = repr(activity_metadata)
    vampytest.assert_instance(output, str)


def test__ActivityMetadataRich__hash():
    """
    Tests whether ``ActivityMetadataRich.__hash__`` works as intended.
    """
    application_id = 202209070015
    assets = ActivityAssets(image_large = 'senya')
    buttons = ['Party', 'Trick']
    created_at = DateTime(2014, 9, 11, tzinfo = TimeZone.utc)
    details = 'vocal'
    details_url = 'https://orindance.party/cart'
    flags = ActivityFlag(1)
    activity_id = 202209070016
    name = 'Iceon'
    party = ActivityParty(party_id = 'Kamase-Tora')
    secrets = ActivitySecrets(join = 'deitarabochi')
    session_id = 'Autobahn'
    state = 'plain'
    state_url = 'https://orindance.party/stand'
    sync_id = 'asia'
    timestamps = ActivityTimestamps(
        end = DateTime(2014, 9, 12, tzinfo = TimeZone.utc),
        start = DateTime(2014, 9, 10, tzinfo = TimeZone.utc),
    )
    url = 'https://www.astil.dev/'
    
    activity_metadata = ActivityMetadataRich(
        application_id = application_id,
        assets = assets,
        buttons = buttons,
        created_at = created_at,
        details = details,
        details_url = details_url,
        flags = flags,
        activity_id = activity_id,
        name = name,
        party = party,
        secrets = secrets,
        session_id = session_id,
        state = state,
        state_url = state_url,
        sync_id = sync_id,
        timestamps = timestamps,
        url = url,
    )
    
    vampytest.assert_instance(hash(activity_metadata), int)


def _iter_options__eq():
    application_id = 202209070017
    assets = ActivityAssets(image_large = 'senya')
    buttons = ['Party', 'Trick']
    created_at = DateTime(2014, 9, 11, tzinfo = TimeZone.utc)
    details = 'vocal'
    details_url = 'https://orindance.party/cart'
    flags = ActivityFlag(1)
    activity_id = 202209070018
    name = 'Iceon'
    party = ActivityParty(party_id = 'Kamase-Tora')
    secrets = ActivitySecrets(join = 'deitarabochi')
    session_id = 'Autobahn'
    state = 'plain'
    state_url = 'https://orindance.party/stand'
    sync_id = 'asia'
    timestamps = ActivityTimestamps(
        end = DateTime(2014, 9, 12, tzinfo = TimeZone.utc),
        start = DateTime(2014, 9, 10, tzinfo = TimeZone.utc),
    )
    url = 'https://www.astil.dev/'

    keyword_parameters = {
        'application_id': application_id,
        'assets': assets,
        'buttons': buttons,
        'created_at': created_at,
        'details': details,
        'details_url': details_url,
        'flags': flags,
        'activity_id': activity_id,
        'name': name,
        'party': party,
        'secrets': secrets,
        'session_id': session_id,
        'state': state,
        'state_url': state_url,
        'sync_id': sync_id,
        'timestamps': timestamps,
        'url': url,
    }
    
    yield (
        {},
        {},
        True,
    )
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'application_id': 0,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'assets': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'buttons': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'created_at': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'details': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'details_url': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'flags': ActivityFlag(2),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'activity_id': 0,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'name': '',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'party': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'secrets': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'session_id': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'state': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'state_url': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'sync_id': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'timestamps': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'url': None,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__ActivityMetadataRich__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ActivityMetadataRich.__eq__`` works as intended.
    
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
    activity_metadata_0 = ActivityMetadataRich(**keyword_parameters_0)
    activity_metadata_1 = ActivityMetadataRich(**keyword_parameters_1)
    
    output = activity_metadata_0 == activity_metadata_1
    vampytest.assert_instance(output, bool)
    return output
