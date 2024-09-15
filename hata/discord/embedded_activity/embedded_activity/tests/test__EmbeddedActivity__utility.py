import vampytest

from ....channel import Channel
from ....client import Client
from ....guild import Guild
from ....user import User

from ...embedded_activity_location import EmbeddedActivityLocation
from ...embedded_activity_user_state import EmbeddedActivityUserState

from ..embedded_activity import EmbeddedActivity

from .test__EmbeddedActivity__constructor import _assert_fields_set


def test__EmbeddedActivity__copy():
    """
    Tests whether ``EmbeddedActivity.copy`` works as intended.
    """
    application_id = 202408020092
    location = EmbeddedActivityLocation(channel_id = 202408020093)
    
    embedded_activity = EmbeddedActivity(
        application_id = application_id,
        location = location,
    )
    
    copy = embedded_activity.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(embedded_activity, copy)
    
    vampytest.assert_eq(embedded_activity, copy)


def test__EmbeddedActivity__copy_with__no_fields():
    """
    Tests whether ``EmbeddedActivity.copy_with`` works as intended.
    
    Case: No fields given.
    """
    application_id = 202408020094
    location = EmbeddedActivityLocation(channel_id = 202408020095)
    
    embedded_activity = EmbeddedActivity(
        application_id = application_id,
        location = location,
    )
    
    copy = embedded_activity.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(embedded_activity, copy)
    
    vampytest.assert_eq(embedded_activity, copy)


def test__EmbeddedActivity__copy_with__all_fields():
    """
    Tests whether ``EmbeddedActivity.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_application_id = 202408020096
    old_location = EmbeddedActivityLocation(channel_id = 202408020097)
    
    new_application_id = 202408020098
    new_location = EmbeddedActivityLocation(channel_id = 202408020099)
    
    embedded_activity = EmbeddedActivity(
        application_id = old_application_id,
        location = old_location,
    )
    
    copy = embedded_activity.copy_with(
        application_id = new_application_id,
        location = new_location,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(embedded_activity, copy)
    
    vampytest.assert_ne(embedded_activity, copy)
    
    vampytest.assert_eq(copy.application_id, new_application_id)
    vampytest.assert_eq(copy.location, new_location)


def _iter_options__guild():
    guild_id = 0
    guild = None
    
    yield 202408020102, guild_id, [guild], guild
    
    guild_id = 202408020100
    guild = None
    
    yield 202408020103, guild_id, [guild], guild
    
    guild_id = 202408020101
    guild = Guild.precreate(guild_id)
    
    yield 202408020104, guild_id, [guild], guild


@vampytest._(vampytest.call_from(_iter_options__guild()).returning_last())
def test__EmbeddedActivity__guild(embedded_activity_id, guild_id, extra):
    """
    Tests whether ``EmbeddedActivity.guild`` works as intended.
    
    Parameters
    ----------
    embedded_activity_id : `int`
        Identifier to create instance with.
    guild_id : `int`
        Identifier to create instance with.
    extra : `list<object>`
        Additional objects to keep in cache.
    
    Returns
    -------
    output : `None | Guild`
    """
    embedded_activity = EmbeddedActivity.precreate(
        embedded_activity_id,
        guild_id = guild_id,
    )
    output = embedded_activity.guild
    vampytest.assert_instance(output, Guild, nullable = True)
    return output
    

def _iter_options__channel_id():
    channel_id = 0
    
    yield 202408020105, None, channel_id
    
    channel_id = 0
    
    yield 202408020106, EmbeddedActivityLocation(), channel_id
    
    channel_id = 202408020107
    
    yield 202408020108, EmbeddedActivityLocation(channel_id = channel_id), channel_id


@vampytest._(vampytest.call_from(_iter_options__channel_id()).returning_last())
def test__EmbeddedActivity__channel_id(embedded_activity_id, location):
    """
    Tests whether ``EmbeddedActivity.channel_id`` works as intended.
    
    Parameters
    ----------
    embedded_activity_id : `int`
        Identifier to create instance with.
    location : `None | EmbeddedActivityLocation`
        Location to create the embedded activity with.
    
    Returns
    -------
    channel_id : `int`
    """
    embedded_activity = EmbeddedActivity.precreate(
        embedded_activity_id,
        location = location,
    )
    output = embedded_activity.channel_id
    vampytest.assert_instance(output, int)
    return output


def _iter_options__channel():
    channel_id = 0
    channel = None
    
    yield 202408020109, None, [channel], channel
    
    channel_id = 0
    channel = None
    
    yield 202408020110, EmbeddedActivityLocation(), [channel], channel
    
    channel_id = 202408020111
    channel = Channel.precreate(channel_id)
    
    yield 202408020112, EmbeddedActivityLocation(channel_id = channel_id), [channel], channel


@vampytest._(vampytest.call_from(_iter_options__channel()).returning_last())
def test__EmbeddedActivity__channel(embedded_activity_id, location, extra):
    """
    Tests whether ``EmbeddedActivity.channel`` works as intended.
    
    Parameters
    ----------
    embedded_activity_id : `int`
        Identifier to create instance with.
    location : `None | EmbeddedActivityLocation`
        Location to create the embedded activity with.
    extra : `list<object>`
        Additional objects to keep in cache.
    
    Returns
    -------
    output : `None | Channel`
    """
    embedded_activity = EmbeddedActivity.precreate(
        embedded_activity_id,
        location = location,
    )
    output = embedded_activity.channel
    vampytest.assert_instance(output, Channel, nullable = True)
    return output


def _iter_options__user_user_states():
    user_state_0 =  EmbeddedActivityUserState(user = User.precreate(202408020113))
    user_state_1 = EmbeddedActivityUserState(user = User.precreate(202408020114))
    
    
    yield 202408020115, None, set()
    yield 202408020116, [user_state_0], {user_state_0}
    yield 202408020116, [user_state_0, user_state_1], {user_state_0, user_state_1}
    

@vampytest._(vampytest.call_from(_iter_options__user_user_states()).returning_last())
def test__EmbeddedActivity__iter_user_states(embedded_activity_id, user_states):
    """
    Tests whether ``EmbeddedActivity.iter_user_states`` works as intended.
    
    Parameters
    ----------
    embedded_activity_id : `int`
        Identifier to create instance with.
    user_states : `None | list<EmbeddedActivityUserState>`
        User states to create the activity with.
    
    Returns
    -------
    output : `set<EmbeddedActivityUserState>`.
    """
    embedded_activity = EmbeddedActivity.precreate(
        embedded_activity_id,
        user_states = user_states,
    )
    return {*embedded_activity.iter_user_states()}


def _iter_options__user_users():
    user_0 = User.precreate(202408020117)
    user_1 = User.precreate(202408020118)
    
    user_state_0 =  EmbeddedActivityUserState(user = user_0)
    user_state_1 = EmbeddedActivityUserState(user = user_1)
    
    
    yield 202408020119, None, set()
    yield 202408020120, [user_state_0], {user_0}
    yield 202408020121, [user_state_0, user_state_1], {user_0, user_1}


@vampytest._(vampytest.call_from(_iter_options__user_users()).returning_last())
def test__EmbeddedActivity__iter_users(embedded_activity_id, user_states):
    """
    Tests whether ``EmbeddedActivity.iter_users`` works as intended.
    
    Parameters
    ----------
    embedded_activity_id : `int`
        Identifier to create instance with.
    user_states : `None | list<ClientUserBase>`
        User states to create the activity with.
    
    Returns
    -------
    output : `set<ClientUserBase>`.
    """
    embedded_activity = EmbeddedActivity.precreate(
        embedded_activity_id,
        user_states = user_states,
    )
    return {*embedded_activity.iter_users()}


def test__EmbeddedActivity__partial__created_with_new():
    """
    Tests whether ``EmbeddedActivity.partial`` works as intended.
    
    Case: partial created with `.__new__`.
    """
    embedded_activity = EmbeddedActivity()
    
    partial = embedded_activity.partial
    vampytest.assert_instance(partial, bool)
    vampytest.assert_true(partial)


def test__EmbeddedActivity__partial__created_with_precreate():
    """
    Tests whether ``EmbeddedActivity.partial`` works as intended.
    
    Case: partial created with `.precreate`
    """
    embedded_activity_id = 202408020122
    
    embedded_activity = EmbeddedActivity.precreate(embedded_activity_id)
    
    partial = embedded_activity.partial
    vampytest.assert_instance(partial, bool)
    vampytest.assert_true(partial)


def test__EmbeddedActivity__partial__non_partial_guild():
    """
    Tests whether ``EmbeddedActivity.partial`` works as intended.
    
    Case: non-partial guild.
    """
    client_id = 202408020123
    embedded_activity_id = 202408020124
    guild_id = 202408020125

    client = Client(
        token = 'token_' + str(client_id),
    )
    
    try:
        embedded_activity = EmbeddedActivity.precreate(embedded_activity_id, guild_id = guild_id)
        guild = Guild.precreate(guild_id, embedded_activities = [embedded_activity])
        guild.clients.append(client)
        
        partial = embedded_activity.partial
        vampytest.assert_instance(partial, bool)
        vampytest.assert_false(partial)
    
    # Cleanup
    finally:
        client._delete()
        client = None


def test__EmbeddedActivity__partial__partial_guild():
    """
    Tests whether ``EmbeddedActivity.partial`` works as intended.
    
    Case: partial guild.
    """
    embedded_activity_id = 202408020126
    guild_id = 202408020127
    
    embedded_activity = EmbeddedActivity.precreate(embedded_activity_id, guild_id = guild_id)
    guild = Guild.precreate(guild_id, embedded_activities = [embedded_activity])
    
    partial = embedded_activity.partial
    vampytest.assert_instance(partial, bool)
    vampytest.assert_true(partial)
