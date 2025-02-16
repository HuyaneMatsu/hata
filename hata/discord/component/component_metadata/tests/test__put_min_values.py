import vampytest

from ..constants import MIN_VALUES_DEFAULT
from ..fields import put_min_values


def test__put_min_values():
    """
    Tests whether ``put_min_values`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (MIN_VALUES_DEFAULT, False, {}),
        (MIN_VALUES_DEFAULT, True, {'min_values': MIN_VALUES_DEFAULT}),
        (10, False, {'min_values': 10}),
    ):
        data = put_min_values(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
