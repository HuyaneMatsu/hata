from datetime import datetime as DateTime

import vampytest

from ...emoji import Emoji

from ..activity import Activity
from ..fields import ActivityAssets, ActivityParty, ActivitySecrets, ActivityTimestamps
from ..flags import ActivityFlag
from ..preinstanced import ActivityType


def test__Activity__new__0():
    """
    Tests whether ``Activity.__new__`` works as expected.
    
    Case: Creating rich activity.
    """
    name = 'Iceon'
    activity_type = ActivityType.game
    
    application_id = 202209070019
    assets = ActivityAssets(image_large = 'senya')
    created_at = DateTime(2014, 9, 11)
    details = 'vocal'
    flags = ActivityFlag(1)
    activity_id = 202209070020
    party = ActivityParty(party_id = 'Kamase-Tora')
    secrets = ActivitySecrets(join = 'deitarabochi')
    session_id = 'Autobahn'
    state = 'plain'
    sync_id = 'asia'
    timestamps = ActivityTimestamps(end = DateTime(2014, 9, 12), start = DateTime(2014, 9, 10))
    url = 'https://www.astil.dev/'
    
    activity = Activity(
        name,
        activity_type = activity_type,
        application_id = application_id,
        assets = assets,
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
    
    vampytest.assert_instance(activity, Activity)
    
    vampytest.assert_is(activity.type, activity_type)
    vampytest.assert_eq(activity.application_id, application_id)
    vampytest.assert_eq(activity.assets, assets)
    vampytest.assert_eq(activity.created_at, created_at)
    vampytest.assert_eq(activity.details, details)
    vampytest.assert_eq(activity.flags, flags)
    vampytest.assert_eq(activity.id, activity_id)
    vampytest.assert_eq(activity.name, name)
    vampytest.assert_eq(activity.party, party)
    vampytest.assert_eq(activity.secrets, secrets)
    vampytest.assert_eq(activity.session_id, session_id)
    vampytest.assert_eq(activity.state, state)
    vampytest.assert_eq(activity.sync_id, sync_id)
    vampytest.assert_eq(activity.timestamps, timestamps)
    vampytest.assert_eq(activity.url, url)
    
    vampytest.assert_instance(activity.emoji, Emoji, nullable=True)


def test__Activity__new__1():
    """
    Tests whether ``Activity.__new__`` works as expected.
    
    Case: Creating custom activity.
    """
    name = 'Keine'
    activity_type = ActivityType.custom
    
    with vampytest.assert_raises(TypeError):
        Activity(name, activity_type = activity_type)
