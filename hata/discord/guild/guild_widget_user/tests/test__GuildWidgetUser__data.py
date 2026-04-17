import vampytest

from ....user import Status

from ..guild_widget_user import GuildWidgetUser

from .test__GuildWidgetUser__constructor import _assert_fields_set


def test__GuildWidgetUser__from_data__0():
    """
    Tests whether ``GuildWidgetUser.from_data`` works as intended.
    
    Case: all fields given.
    """
    activity_name = 'Far'
    avatar_url = 'https://orindance.party/'
    discriminator = 1111
    name = 'East'
    status = Status.idle
    user_id = 69
    
    data = {
        'game': {
            'name': activity_name,
        },
        'avatar_url': avatar_url,
        'discriminator': str(discriminator),
        'username': name,
        'status': status.value,
        'id': str(user_id),
    }
    
    widget_user = GuildWidgetUser.from_data(data)
    _assert_fields_set(widget_user)

    vampytest.assert_eq(widget_user.activity_name, activity_name)
    vampytest.assert_eq(widget_user.avatar_url, avatar_url)
    vampytest.assert_eq(widget_user.discriminator, discriminator)
    vampytest.assert_eq(widget_user.id, user_id)
    vampytest.assert_eq(widget_user.name, name)
    vampytest.assert_is(widget_user.status, status)


def test__GuildWidgetUser__to_data__0():
    """
    Tests whether ``GuildWidgetUser.to_data`` works as intended.
    
    Case: Include defaults.
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
    
    expected_output = {
        'game': {
            'name': activity_name,
        },
        'avatar_url': avatar_url,
        'discriminator': str(discriminator),
        'username': name,
        'status': status.value,
        'id': str(user_id),
    }
    
    vampytest.assert_eq(
        widget_user.to_data(defaults = True),
        expected_output,
    )
