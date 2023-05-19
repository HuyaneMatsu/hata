import vampytest

from ....user import Status

from ..guild_widget_user import GuildWidgetUser


def _assert_fields_set(widget_user):
    """
    Checks whether every attribute is set of the given guild widget user.
    
    Parameters
    ----------
    widget_user : ``GuildWidgetUser``
        The field to check.
    """
    vampytest.assert_instance(widget_user, GuildWidgetUser)
    vampytest.assert_instance(widget_user.activity_name, str, nullable = True)
    vampytest.assert_instance(widget_user.avatar_url, str, nullable = True)
    vampytest.assert_instance(widget_user.discriminator, int)
    vampytest.assert_instance(widget_user.id, int)
    vampytest.assert_instance(widget_user.name, str)
    vampytest.assert_instance(widget_user.status, Status)


def test__GuildWidgetUser__new__0():
    """
    Tests whether ``GuildWidgetUser.__new__`` works as intended.
    
    Case: No fields given.
    """
    widget_user = GuildWidgetUser()
    _assert_fields_set(widget_user)


def test__GuildWidgetUser__new__1():
    """
    Tests whether ``GuildWidgetUser.__new__`` works as intended.
    
    Case: All fields given.
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
    _assert_fields_set(widget_user)

    vampytest.assert_eq(widget_user.activity_name, activity_name)
    vampytest.assert_eq(widget_user.avatar_url, avatar_url)
    vampytest.assert_eq(widget_user.discriminator, discriminator)
    vampytest.assert_eq(widget_user.id, user_id)
    vampytest.assert_eq(widget_user.name, name)
    vampytest.assert_is(widget_user.status, status)
