import vampytest

from ...webhook_source_guild import WebhookSourceGuild

from ..fields import put_source_guild


def test__put_source_guild():
    """
    Tests whether ``put_source_guild`` works as intended.
    """
    guild = WebhookSourceGuild(
        guild_id = 202302020009,
        name = 'itori',
    )
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'source_guild': None}),
        (guild, False, {'source_guild': guild.to_data(defaults = False)}),
        (guild, True, {'source_guild': guild.to_data(defaults = True)}),
    ):
        data = put_source_guild(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
