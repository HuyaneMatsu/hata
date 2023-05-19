import vampytest

from ....user import Status

from ..guild_widget_user import GuildWidgetUser


def test__GuildWidgetUser__repr():
    """
    Tests whether ``GuildWidgetUser.__repr__`` works as intended.
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
    
    vampytest.assert_instance(repr(widget_user), str)


def test__GuildWidgetUser__hash():
    """
    Tests whether ``GuildWidgetUser.__hash__`` works as intended.
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
    
    vampytest.assert_instance(hash(widget_user), int)


def test__GuildWidgetUser__eq():
    """
    Tests whether ``GuildWidgetUser.__repr__`` works as intended.
    """
    activity_name = 'Far'
    avatar_url = 'https://orindance.party/'
    discriminator = 1111
    name = 'East'
    status = Status.idle
    user_id = 69
    
    fields = {
        'activity_name': activity_name,
        'avatar_url': avatar_url,
        'discriminator': discriminator,
        'name': name,
        'status': status,
        'user_id': user_id,
    }
    
    widget_user = GuildWidgetUser(**fields)
    
    vampytest.assert_eq(widget_user, widget_user)
    vampytest.assert_ne(widget_user, object())
    
    for field_name, field_value in (
        ('activity_name', 'Blood'),
        ('avatar_url', 'https://www.astil.dev/'),
        ('discriminator', 420),
        ('name', 'Remilia'),
        ('status', Status.dnd),
        ('user_id', 1),
    ):
        test_widget_user = GuildWidgetUser(**{**fields, field_name: field_value})
        vampytest.assert_ne(widget_user, test_widget_user)
