import vampytest

from ..guild_widget_channel import GuildWidgetChannel


def test__GuildWidgetChannel__repr():
    """
    Tests whether ``GuildWidgetChannel.__repr__`` works as intended.
    """
    channel_id = 202305180003
    name = 'East'
    position = 11
    
    widget_channel = GuildWidgetChannel(
        channel_id = channel_id,
        name = name,
        position = position,
    )
    
    vampytest.assert_instance(repr(widget_channel), str)


def test__GuildWidgetChannel__hash():
    """
    Tests whether ``GuildWidgetChannel.__hash__`` works as intended.
    """
    channel_id = 202305180004
    name = 'East'
    position = 11
    
    widget_channel = GuildWidgetChannel(
        channel_id = channel_id,
        name = name,
        position = position,
    )
    
    vampytest.assert_instance(hash(widget_channel), int)


def test__GuildWidgetChannel__eq():
    """
    Tests whether ``GuildWidgetChannel.__repr__`` works as intended.
    """
    channel_id = 202305180005
    name = 'East'
    position = 11
    
    fields = {
        'channel_id': channel_id,
        'name': name,
        'position': position,
    }
    
    widget_channel = GuildWidgetChannel(**fields)
    
    vampytest.assert_eq(widget_channel, widget_channel)
    vampytest.assert_ne(widget_channel, object())
    
    for field_name, field_value in (
        ('channel_id', 202305180006),
        ('name', 'Far'),
        ('position', 42),
    ):
        test_widget_channel = GuildWidgetChannel(**{**fields, field_name: field_value})
        vampytest.assert_ne(widget_channel, test_widget_channel)


def test__GuildWidgetChannel__sort():
    """
    Tests whether sorting guild widget channels works.
    """
    channel_id_0 = 202305180007
    position_0 = 3
    
    channel_id_1 = 202305180008
    position_1 = 2
    
    channel_id_2 = 202305180009
    position_2 = 2
    
    channel_0 = GuildWidgetChannel(channel_id = channel_id_0, position = position_0)
    channel_1 = GuildWidgetChannel(channel_id = channel_id_1, position = position_1)
    channel_2 = GuildWidgetChannel(channel_id = channel_id_2, position = position_2)
    
    to_sort = [channel_1, channel_0, channel_2]
    to_sort.sort()
    
    vampytest.assert_eq(
        to_sort,
        [channel_1, channel_2, channel_0]
    )
