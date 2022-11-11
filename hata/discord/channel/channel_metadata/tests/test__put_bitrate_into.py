import vampytest

from ..constants import BITRATE_DEFAULT
from ..fields import put_bitrate_into


def test__put_bitrate_into():
    """
    Tests whether ``put_bitrate_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (BITRATE_DEFAULT, False, {'bitrate': BITRATE_DEFAULT}),
        (1, False, {'bitrate': 1}),
    ):
        data = put_bitrate_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
