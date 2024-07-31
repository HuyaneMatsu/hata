import vampytest

from ....activity import Activity, ActivityType
from ....channel import Channel
from ....guild import Guild
from ....user import User

from ..embedded_activity_state import EmbeddedActivityState
from ..key import EmbeddedActivityStateKey

from .test__EmbeddedActivityState__constructor import _assert_fields_set


def test__EmbeddedActivityState__copy():
    """
    Tests whether ``EmbeddedActivityState.copy`` works as intended.
    """
    activity = Activity('tsuki', activity_type = ActivityType.competing, application_id = 202212260099)
    channel_id = 202212260100
    guild_id = 202212260101
    user_ids = [202212260102, 2022122600103]
    
    
    embedded_activity_state = EmbeddedActivityState(
        activity = activity,
        channel_id = channel_id,
        guild_id = guild_id,
        user_ids = user_ids,
    )
    
    copy = embedded_activity_state.copy()
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, embedded_activity_state)
    
    vampytest.assert_eq(copy.activity, activity)
    vampytest.assert_eq(copy.channel_id, channel_id)
    vampytest.assert_eq(copy.guild_id, guild_id)
    vampytest.assert_eq(copy.user_ids, set(user_ids))


def test__EmbeddedActivityState__copy_with__0():
    """
    Tests whether ``EmbeddedActivityState.copy_with`` works as intended.
    
    Case: No fields given.
    """
    activity = Activity('tsuki', activity_type = ActivityType.competing, application_id = 202212260104)
    channel_id = 202212260105
    guild_id = 202212260106
    user_ids = [202212260107, 2022122600108]
    
    
    embedded_activity_state = EmbeddedActivityState(
        activity = activity,
        channel_id = channel_id,
        guild_id = guild_id,
        user_ids = user_ids,
    )
    
    copy = embedded_activity_state.copy_with()
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, embedded_activity_state)
    
    vampytest.assert_eq(copy.activity, activity)
    vampytest.assert_eq(copy.channel_id, channel_id)
    vampytest.assert_eq(copy.guild_id, guild_id)
    vampytest.assert_eq(copy.user_ids, set(user_ids))


def test__EmbeddedActivityState__copy_with__1():
    """
    Tests whether ``EmbeddedActivityState.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_activity = Activity('tsuki', activity_type = ActivityType.competing, application_id = 202212260109)
    old_channel_id = 202212260110
    old_guild_id = 202212260111
    old_user_ids = [202212260112, 2022122600113]
    new_activity = Activity('shiki', activity_type = ActivityType.playing, application_id = 202212260114)
    new_channel_id = 202212260115
    new_guild_id = 202212260116
    new_user_ids = [202212260117]
    
    
    embedded_activity_state = EmbeddedActivityState(
        activity = old_activity,
        channel_id = old_channel_id,
        guild_id = old_guild_id,
        user_ids = old_user_ids,
    )
    
    copy = embedded_activity_state.copy_with(
        activity = new_activity,
        channel_id = new_channel_id,
        guild_id = new_guild_id,
        user_ids = new_user_ids,
        
    )
    _assert_fields_set(copy)
    
    vampytest.assert_is_not(copy, embedded_activity_state)
    
    vampytest.assert_eq(copy.activity, new_activity)
    vampytest.assert_eq(copy.channel_id, new_channel_id)
    vampytest.assert_eq(copy.guild_id, new_guild_id)
    vampytest.assert_eq(copy.user_ids, set(new_user_ids))


def test__EmbeddedActivityState__application_id():
    """
    Tests whether ``EmbeddedActivityState.application_id`` works as intended.
    """
    application_id = 202212260118
    activity = Activity(application_id = application_id)
    
    embedded_activity_state = EmbeddedActivityState(
        activity = activity,
    )
    
    vampytest.assert_eq(embedded_activity_state.application_id, application_id)
    

def test__EmbeddedActivityState__key():
    """
    Tests whether ``EmbeddedActivityState.key`` works as intended.
    """
    application_id = 202212260119
    channel_id = 202212260120
    guild_id = 202212260121
    activity = Activity(application_id = application_id)
    
    embedded_activity_state = EmbeddedActivityState(
        activity = activity,
        channel_id = channel_id,
        guild_id = guild_id,
    )
    vampytest.assert_eq(
        embedded_activity_state.key,
        EmbeddedActivityStateKey(guild_id, channel_id, application_id),
    )


def test__EmbeddedActivityState__guild():
    """
    Tests whether ``EmbeddedActivityState.guild`` works as intended.
    """
    guild_id_0 = 202212260122
    guild_id_1 = 202212260123
    guild_0 = Guild.precreate(guild_id_0)
    
    for input_value, expected_output in (
        (0, None),
        (guild_id_0, guild_0),
        (guild_id_1, None),
    ):
        embedded_activity_state = EmbeddedActivityState(
            guild_id = input_value,
        )
        
        vampytest.assert_is(embedded_activity_state.guild, expected_output)


def test__EmbeddedActivityState__channel():
    """
    Tests whether ``EmbeddedActivityState.channel`` works as intended.
    """
    channel_id = 202212260124
    channel = Channel.precreate(channel_id)
    
    embedded_activity_state = EmbeddedActivityState(
        channel_id = channel_id,
    )
    
    vampytest.assert_is(embedded_activity_state.channel, channel)


def test__EmbeddedActivityState__users():
    """
    Tests whether ``EmbeddedActivityState.users`` works as intended.
    """
    user_id_0 = 202212260125
    user_id_1 = 202212260126
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    
    user_ids = {user_id_0, user_id_1}
    users = {user_0, user_1}
    
    embedded_activity_state = EmbeddedActivityState(
        user_ids = user_ids,
    )
    
    vampytest.assert_eq({*embedded_activity_state.users}, users)
