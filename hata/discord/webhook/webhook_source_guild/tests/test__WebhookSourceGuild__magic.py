import vampytest

from ....bases import Icon, IconType

from ..guild import WebhookSourceGuild


def test__WebhookSourceGuild__repr():
    """
    Tests whether ``WebhookSourceGuild.__repr__`` works as intended.
    """
    guild_id = 202302010016
    icon = Icon(IconType.static, 12)
    name = 'senya'
    
    guild = WebhookSourceGuild(
        guild_id = guild_id,
        icon = icon,
        name = name,
    )
    vampytest.assert_instance(repr(guild), str)


def test__WebhookSourceGuild__hash():
    """
    Tests whether ``WebhookSourceGuild.__hash__`` works as intended.
    """
    guild_id = 202302010017
    icon = Icon(IconType.static, 12)
    name = 'senya'
    
    guild = WebhookSourceGuild(
        guild_id = guild_id,
        icon = icon,
        name = name,
    )
    vampytest.assert_instance(hash(guild), int)


def test__WebhookSourceGuild__eq():
    """
    Tests whether ``WebhookSourceGuild.__eq__`` works as intended.
    """
    guild_id = 202302010018
    icon = Icon(IconType.static, 12)
    name = 'senya'
    
    keyword_parameters = {
        'guild_id': guild_id,
        'icon': icon,
        'name': name,
    }
    
    guild = WebhookSourceGuild(**keyword_parameters)
    vampytest.assert_eq(guild, guild)
    vampytest.assert_ne(guild, object())
    
    for field_name, field_value in (
        ('guild_id', 202302010019),
        ('icon', Icon(IconType.animated, 14)),
        ('name', 'yuuka'),
    ):
        test_guild = WebhookSourceGuild(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(guild, test_guild)
