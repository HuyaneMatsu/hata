import vampytest

from ....user import Status

from ..guild_widget_user import GuildWidgetUser

from .test__GuildWidgetUser__constructor import _assert_fields_set


def test__GuildWidgetUser__copy():
    """
    Tests whether ``GuildWidgetUser.copy`` works as intended.
    """
    activity_name = 'Far'
    avatar_url = 'https://orindance.party/'
    discriminator = 1111
    name = 'East'
    status = Status.idle
    user_id = 69
    
    widget_user = GuildWidgetUser(
        activity_name = activity_name,
        avatar_url = avatar_url,
        discriminator = discriminator,
        name = name,
        status = status,
        user_id = user_id,
    )
    
    copy = widget_user.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(widget_user, copy)

    vampytest.assert_eq(widget_user, copy)


def test__GuildWidgetUser__copy_with__0():
    """
    Tests whether ``GuildWidgetUser.copy_with`` works as intended.
    
    Case: no fields given.
    """
    activity_name = 'Far'
    avatar_url = 'https://orindance.party/'
    discriminator = 1111
    name = 'East'
    status = Status.idle
    user_id = 69
    
    widget_user = GuildWidgetUser(
        activity_name = activity_name,
        avatar_url = avatar_url,
        discriminator = discriminator,
        name = name,
        status = status,
        user_id = user_id,
    )
    
    copy = widget_user.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(widget_user, copy)

    vampytest.assert_eq(widget_user, copy)


def test__GuildWidgetUser__copy_with__1():
    """
    Tests whether ``GuildWidgetUser.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_activity_name = 'Far'
    old_avatar_url = 'https://orindance.party/'
    old_discriminator = 1111
    old_name = 'East'
    old_status = Status.idle
    old_user_id = 69
    
    new_activity_name = 'Blood'
    new_avatar_url = 'https://www.astil.dev/'
    new_discriminator = 1112
    new_name = 'Remilia'
    new_status = Status.dnd
    new_user_id = 20
    
    widget_user = GuildWidgetUser(
        activity_name = old_activity_name,
        avatar_url = old_avatar_url,
        discriminator = old_discriminator,
        name = old_name,
        status = old_status,
        user_id = old_user_id,
    )
    
    copy = widget_user.copy_with(
        activity_name = new_activity_name,
        avatar_url = new_avatar_url,
        discriminator = new_discriminator,
        name = new_name,
        status = new_status,
        user_id = new_user_id,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(widget_user, copy)

    vampytest.assert_ne(widget_user, copy)

    vampytest.assert_eq(copy.activity_name, new_activity_name)
    vampytest.assert_eq(copy.avatar_url, new_avatar_url)
    vampytest.assert_eq(copy.discriminator, new_discriminator)
    vampytest.assert_eq(copy.id, new_user_id)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_is(copy.status, new_status)
