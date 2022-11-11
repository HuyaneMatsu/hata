import vampytest

from ..fields import parse_guild_id


def test__parse_guild_id():
    """
    Tests whether ``parse_guild_id`` works as intended.
    """
    for input_data, expected_output in (
        ({}, 0),
        ({'guild_id': None}, 0),
        ({'guild_id': '1'}, 1),
    ):
        output = parse_guild_id(input_data)
        vampytest.assert_eq(output, expected_output)
