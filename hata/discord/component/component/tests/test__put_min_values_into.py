import vampytest

from ..constants import MIN_VALUES_DEFAULT
from ..fields import put_min_values_into


def test__put_min_values_into():
    """
    Tests whether ``put_min_values_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (MIN_VALUES_DEFAULT, False, {}),
        (MIN_VALUES_DEFAULT, True, {'min_values': MIN_VALUES_DEFAULT}),
        (10, False, {'min_values': 10}),
    ):
        data = put_min_values_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
