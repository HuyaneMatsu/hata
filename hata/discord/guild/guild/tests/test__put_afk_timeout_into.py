import vampytest

from ..constants import AFK_TIMEOUT_DEFAULT
from ..fields import put_afk_timeout_into


def test__put_afk_timeout_into():
    """
    Tests whether ``put_afk_timeout_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (AFK_TIMEOUT_DEFAULT, False, {'afk_timeout': AFK_TIMEOUT_DEFAULT}),
        (60, False, {'afk_timeout': 60}),
    ):
        data = put_afk_timeout_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
