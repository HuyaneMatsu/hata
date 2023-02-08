import vampytest

from ...webhook_source_guild import WebhookSourceGuild

from ..fields import parse_source_guild


def test__parse_source_guild():
    """
    Tests whether ``parse_source_guild`` works as intended. 
    """
    guild = WebhookSourceGuild(
        guild_id = 202302020007,
        name = 'itori',
    )
    
    for input_data, expected_output in (
        ({}, None),
        ({'source_guild': None}, None),
        ({'source_guild': guild.to_data(defaults = True)}, guild),
    ):
        output = parse_source_guild(input_data)
        vampytest.assert_eq(output, expected_output)
