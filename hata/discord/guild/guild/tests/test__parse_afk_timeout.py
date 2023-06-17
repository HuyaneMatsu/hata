import vampytest

from ..constants import AFK_TIMEOUT_DEFAULT
from ..fields import parse_afk_timeout


def test__parse_afk_timeout():
    """
    Tests whether ``parse_afk_timeout`` works as intended.
    """
    for input_data, expected_output in (
        ({}, AFK_TIMEOUT_DEFAULT),
        ({'afk_timeout': 60}, 60),
    ):
        output = parse_afk_timeout(input_data)
        vampytest.assert_eq(output, expected_output)
