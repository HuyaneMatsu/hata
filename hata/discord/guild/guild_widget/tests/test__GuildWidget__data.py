import vampytest

from ...guild_widget_channel import GuildWidgetChannel
from ...guild_widget_user import GuildWidgetUser

from ..guild_widget import GuildWidget

from .test__GuildWidget__constructor import _assert_fields_set


def test__GuildWidget__from_data__0():
    """
    Tests whether ``GuildWidget.from_data`` works as intended.
    
    Case: all fields given.
    """
    approximate_online_count = 123
    channels = [
        GuildWidgetChannel(name = 'Koishi', channel_id = 202305190032),
        GuildWidgetChannel(name = 'Satori', channel_id = 202305190033),
    ]
    guild_id = 202305190015
    invite_url = 'https://orindance.party/'
    name = 'Komeiji'
    users = [
        GuildWidgetUser(name = 'Koishi', user_id = 10),
        GuildWidgetUser(name = 'Satori', user_id = 11),
    ]
    
    data = {
        'presence_count': approximate_online_count,
        'channels': [channel.to_data() for channel in channels],
        'id': str(guild_id),
        'instant_invite': invite_url,
        'name': name,
        'members': [user.to_data() for user in users],
    }
    
    widget = GuildWidget.from_data(data)
    _assert_fields_set(widget)
    
    vampytest.assert_eq(widget.approximate_online_count, approximate_online_count)
    vampytest.assert_eq(widget.channels, tuple(channels))
    vampytest.assert_eq(widget.id, guild_id)
    vampytest.assert_eq(widget.invite_url, invite_url)
    vampytest.assert_eq(widget.name, name)
    vampytest.assert_eq(widget.users, tuple(users))


def test__GuildWidget__to_data__0():
    """
    Tests whether ``GuildWidget.to_data`` works as intended.
    
    Case: Include defaults.
    """
    approximate_online_count = 123
    channels = [
        GuildWidgetChannel(name = 'Koishi', channel_id = 202305190034),
        GuildWidgetChannel(name = 'Satori', channel_id = 202305190035),
    ]
    guild_id = 202305190016
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
    
    expected_output = {
        'presence_count': approximate_online_count,
        'channels': [channel.to_data(defaults = True) for channel in channels],
        'id': str(guild_id),
        'instant_invite': invite_url,
        'name': name,
        'members': [user.to_data(defaults = True) for user in users],
    }
    
    vampytest.assert_eq(
        widget.to_data(defaults = True),
        expected_output,
    )
