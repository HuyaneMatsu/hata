import vampytest

from ...guild import Guild
from ...guild_widget_channel import GuildWidgetChannel
from ...guild_widget_user import GuildWidgetUser

from ..guild_widget import GuildWidget

from .test__GuildWidget__constructor import _assert_fields_set


def test__GuildWidget__copy():
    """
    Tests whether ``GuildWidget.copy`` works as intended.
    """
    approximate_online_count = 123
    channels = [GuildWidgetChannel(name = 'Koishi'), GuildWidgetChannel(name = 'Satori')]
    guild_id = 202305190021
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
    
    copy = widget.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(widget, copy)

    vampytest.assert_eq(widget, copy)


def test__GuildWidget__copy_with__0():
    """
    Tests whether ``GuildWidget.copy_with`` works as intended.
    
    Case: no fields given.
    """
    approximate_online_count = 123
    channels = [GuildWidgetChannel(name = 'Koishi'), GuildWidgetChannel(name = 'Satori')]
    guild_id = 202305190022
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
    
    copy = widget.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(widget, copy)

    vampytest.assert_eq(widget, copy)


def test__GuildWidget__copy_with__1():
    """
    Tests whether ``GuildWidget.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_approximate_online_count = 123
    old_channels = [GuildWidgetChannel(name = 'Koishi'), GuildWidgetChannel(name = 'Satori')]
    old_guild_id = 202305190023
    old_invite_url = 'https://orindance.party/'
    old_name = 'Komeiji'
    old_users = [GuildWidgetUser(name = 'Koishi'), GuildWidgetUser(name = 'Satori')]
    
    new_approximate_online_count = 11111
    new_channels = [
        GuildWidgetChannel(name = 'Orin', channel_id = 202305190028),
        GuildWidgetChannel(name = 'Okuu', channel_id = 202305190029),
    ]
    new_guild_id = 202305190024
    new_invite_url = 'https://www.astil.dev/'
    new_name = 'Cute'
    new_users = [
        GuildWidgetUser(name = 'Orin', user_id = 10),
        GuildWidgetUser(name = 'Okuu', user_id = 11),
    ]
    
    widget = GuildWidget(
        approximate_online_count = old_approximate_online_count,
        channels = old_channels,
        guild_id = old_guild_id,
        invite_url = old_invite_url,
        name = old_name,
        users = old_users,
    )
    
    copy = widget.copy_with(
        approximate_online_count = new_approximate_online_count,
        channels = new_channels,
        guild_id = new_guild_id,
        invite_url = new_invite_url,
        name = new_name,
        users = new_users,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(widget, copy)

    vampytest.assert_ne(widget, copy)

    vampytest.assert_eq(copy.approximate_online_count, new_approximate_online_count)
    vampytest.assert_eq(copy.channels, tuple(new_channels))
    vampytest.assert_eq(copy.id, new_guild_id)
    vampytest.assert_eq(copy.invite_url, new_invite_url)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.users, tuple(new_users))


def test__GuildWidget__json_url():
    """
    Tests whether ``GuildWidget.json_url`` works as intended.
    """
    guild_widget = GuildWidget()
    
    output = guild_widget.json_url
    
    vampytest.assert_instance(output, str)


def test__GuildWidget__guild():
    """
    Tests whether ``GuildWidget.guild`` works as intended.
    """
    guild_id = 202305190025
    name = 'Koishi'
    
    guild_widget = GuildWidget(
        guild_id = guild_id,
        name = name,
    )
    
    output = guild_widget.guild
    
    vampytest.assert_instance(output, Guild)
    vampytest.assert_eq(output.id, guild_id)
    vampytest.assert_eq(output.name, name)


def test__GuildWidget__iter_channels():
    """
    Tests whether ``GuildWidget.iter_channels`` works as intended.
    """
    channel_0 = GuildWidgetChannel(name = 'Koishi', channel_id = 202305190026)
    channel_1 = GuildWidgetChannel(name = 'Satori', channel_id = 202305190027)
    
    for input_value, expected_output in (
        (None, []),
        ([channel_0], [channel_0]),
        ([channel_0, channel_1], [channel_0, channel_1]),
    ):
        guild_widget = GuildWidget(channels = input_value)
        output = [*guild_widget.iter_channels()]
        
        vampytest.assert_eq(output, expected_output)


def test__GuildWidget__iter_users():
    """
    Tests whether ``GuildWidget.iter_users`` works as intended.
    """
    user_0 = GuildWidgetUser(name = 'Koishi', user_id = 1)
    user_1 = GuildWidgetUser(name = 'Satori', user_id = 2)
    
    for input_value, expected_output in (
        (None, []),
        ([user_0], [user_0]),
        ([user_0, user_1], [user_0, user_1]),
    ):
        guild_widget = GuildWidget(users = input_value)
        output = [*guild_widget.iter_users()]
        
        vampytest.assert_eq(output, expected_output)
