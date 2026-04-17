import vampytest

from ...guild_widget_channel import GuildWidgetChannel
from ...guild_widget_user import GuildWidgetUser

from ..guild_widget import GuildWidget


def _assert_fields_set(widget):
    """
    Checks whether every attribute is set of the given guild widget.
    
    Parameters
    ----------
    widget : ``GuildWidget``
        The field to check.
    """
    vampytest.assert_instance(widget, GuildWidget)
    vampytest.assert_instance(widget.approximate_online_count, int)
    vampytest.assert_instance(widget.channels, tuple, nullable = True)
    vampytest.assert_instance(widget.id, int)
    vampytest.assert_instance(widget.invite_url, str, nullable = True)
    vampytest.assert_instance(widget.name, str)
    vampytest.assert_instance(widget.users, tuple, nullable = True)


def test__GuildWidget__new__0():
    """
    Tests whether ``GuildWidget.__new__`` works as intended.
    
    Case: No fields given.
    """
    widget = GuildWidget()
    _assert_fields_set(widget)


def test__GuildWidget__new__1():
    """
    Tests whether ``GuildWidget.__new__`` works as intended.
    
    Case: All fields given.
    """
    approximate_online_count = 123
    channels = [
        GuildWidgetChannel(name = 'Koishi', channel_id = 202305190036),
        GuildWidgetChannel(name = 'Satori', channel_id = 202305190037),
    ]
    guild_id = 202305190014
    invite_url = 'https://orindance.party/'
    name = 'Komeiji'
    users = [
        GuildWidgetUser(name = 'Koishi', user_id = 10),
        GuildWidgetUser(name = 'Satori', user_id = 11),
    ]
    
    widget = GuildWidget(
        approximate_online_count = approximate_online_count,
        channels = channels,
        guild_id = guild_id,
        invite_url = invite_url,
        name = name,
        users = users,
    )
    _assert_fields_set(widget)
    
    vampytest.assert_eq(widget.approximate_online_count, approximate_online_count)
    vampytest.assert_eq(widget.channels, tuple(channels))
    vampytest.assert_eq(widget.id, guild_id)
    vampytest.assert_eq(widget.invite_url, invite_url)
    vampytest.assert_eq(widget.name, name)
    vampytest.assert_eq(widget.users, tuple(users))
