import vampytest

from ...webhook_source_guild import WebhookSourceGuild

from ..fields import validate_source_guild


def test__validate_source_guild__0():
    """
    Tests whether `validate_source_guild` works as intended.
    
    Case: passing.
    """
    guild = WebhookSourceGuild(
        guild_id = 202302020011,
        name = 'itori',
    )
    
    for input_value, expected_output in (
        (None, None),
        (guild, guild),
    ):
        output = validate_source_guild(input_value)
        vampytest.assert_is(output, expected_output)


def test__validate_source_guild__1():
    """
    Tests whether `validate_source_guild` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        'a',
    ):
        with vampytest.assert_raises(TypeError):
            validate_source_guild(input_value)
