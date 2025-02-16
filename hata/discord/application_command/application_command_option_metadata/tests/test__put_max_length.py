import vampytest

from ..constants import MAX_LENGTH_DEFAULT, MAX_LENGTH_MAX
from ..fields import put_max_length


def test__put_max_length():
    """
    Tests whether ``put_max_length`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (
            MAX_LENGTH_DEFAULT,
            False,
            {'max_length': MAX_LENGTH_MAX},
        ), (
            MAX_LENGTH_MAX,
            False,
            {'max_length': MAX_LENGTH_MAX},
        ), (
            10,
            False,
            {'max_length': 10},
        ),
    ):
        data = put_max_length(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
