import vampytest

from ..constants import MIN_LENGTH_DEFAULT
from ..fields import put_min_length


def test__put_min_length():
    """
    Tests whether ``put_min_length`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (MIN_LENGTH_DEFAULT, False, {}),
        (MIN_LENGTH_DEFAULT, True, {'min_length': MIN_LENGTH_DEFAULT}),
        (10, False, {'min_length': 10}),
    ):
        data = put_min_length(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
