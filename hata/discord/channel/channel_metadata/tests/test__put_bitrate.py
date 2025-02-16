import vampytest

from ..constants import BITRATE_DEFAULT
from ..fields import put_bitrate


def test__put_bitrate():
    """
    Tests whether ``put_bitrate`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (BITRATE_DEFAULT, False, {'bitrate': BITRATE_DEFAULT}),
        (1, False, {'bitrate': 1}),
    ):
        data = put_bitrate(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
