import vampytest

from ...guild_widget_channel import GuildWidgetChannel
from ...guild_widget_user import GuildWidgetUser

from ..guild_widget import GuildWidget


def test__GuildWidget__repr():
    """
    Tests whether ``GuildWidget.__repr__`` works as intended.
    """
    approximate_online_count = 123
    channels = [GuildWidgetChannel(name = 'Koishi'), GuildWidgetChannel(name = 'Satori')]
    guild_id = 202305190017
    invite_url = 'https://orindance.party/'
    name = 'Komeiji'
    users = [GuildWidgetUser(name = 'Koishi'), GuildWidgetUser(name = 'Satori')]
    
    widget = GuildWidget(
        approximate_online_count = approximate_online_count,
        channels = channels,
        guild_id = guild_id,
        invite_url = invite_url,
        name = name,
        users = users,
    )
    
    vampytest.assert_instance(repr(widget), str)


def test__GuildWidget__hash():
    """
    Tests whether ``GuildWidget.__hash__`` works as intended.
    """
    approximate_online_count = 123
    channels = [GuildWidgetChannel(name = 'Koishi'), GuildWidgetChannel(name = 'Satori')]
    guild_id = 202305190018
    invite_url = 'https://orindance.party/'
    name = 'Komeiji'
    users = [GuildWidgetUser(name = 'Koishi'), GuildWidgetUser(name = 'Satori')]
    
    widget = GuildWidget(
        approximate_online_count = approximate_online_count,
        channels = channels,
        guild_id = guild_id,
        invite_url = invite_url,
        name = name,
        users = users,
    )
    
    vampytest.assert_instance(hash(widget), int)


def test__GuildWidget__eq():
    """
    Tests whether ``GuildWidget.__repr__`` works as intended.
    """
    approximate_online_count = 123
    channels = [GuildWidgetChannel(name = 'Koishi'), GuildWidgetChannel(name = 'Satori')]
    guild_id = 202305190019
    invite_url = 'https://orindance.party/'
    name = 'Komeiji'
    users = [GuildWidgetUser(name = 'Koishi'), GuildWidgetUser(name = 'Satori')]
    
    fields = {
        'approximate_online_count': approximate_online_count,
        'channels': channels,
        'guild_id': guild_id,
        'invite_url': invite_url,
        'name': name,
        'users': users,
    }
    
    widget = GuildWidget(**fields)
    
    vampytest.assert_eq(widget, widget)
    vampytest.assert_ne(widget, object())
    
    for field_name, field_value in (
        ('approximate_online_count', 12),
        ('channels', None),
        ('guild_id', 202305190020),
        ('invite_url', None),
        ('name', 'Satori'),
        ('users', None),
    ):
        test_widget = GuildWidget(**{**fields, field_name: field_value})
        vampytest.assert_ne(widget, test_widget)
