import vampytest

from ..constants import MAX_VALUES_DEFAULT
from ..fields import put_max_values


def test__put_max_values():
    """
    Tests whether ``put_max_values`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (MAX_VALUES_DEFAULT, False, {}),
        (MAX_VALUES_DEFAULT, True, {'max_values': MAX_VALUES_DEFAULT}),
        (10, False, {'max_values': 10}),
    ):
        data = put_max_values(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
