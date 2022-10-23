import vampytest

from ..constants import MAX_VALUES_DEFAULT
from ..fields import put_max_values_into


def test__put_max_values_into():
    """
    Tests whether ``put_max_values_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (MAX_VALUES_DEFAULT, False, {}),
        (MAX_VALUES_DEFAULT, True, {'max_values': MAX_VALUES_DEFAULT}),
        (10, False, {'max_values': 10}),
    ):
        data = put_max_values_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
