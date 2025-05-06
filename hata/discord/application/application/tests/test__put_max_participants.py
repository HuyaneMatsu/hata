import vampytest

from ..constants import MAX_PARTICIPANTS_DEFAULT
from ..fields import put_max_participants


def test__put_max_participants():
    """
    Tests whether ``put_max_participants`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (MAX_PARTICIPANTS_DEFAULT, False, {}),
        (MAX_PARTICIPANTS_DEFAULT, True, {'max_participants': -1}),
        (1, False, {'max_participants': 1}),
    ):
        data = put_max_participants(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
