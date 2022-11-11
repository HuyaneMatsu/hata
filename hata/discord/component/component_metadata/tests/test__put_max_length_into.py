import vampytest

from ..constants import MAX_LENGTH_DEFAULT
from ..fields import put_max_length_into


def test__put_max_length_into():
    """
    Tests whether ``put_max_length_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (MAX_LENGTH_DEFAULT, False, {}),
        (MAX_LENGTH_DEFAULT, True, {'max_length': MAX_LENGTH_DEFAULT}),
        (10, False, {'max_length': 10}),
    ):
        data = put_max_length_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
