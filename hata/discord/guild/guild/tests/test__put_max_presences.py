import vampytest

from ..fields import put_max_presences


def test__put_max_presences():
    """
    Tests whether ``put_max_presences`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (0, False, {'max_presences': 0}),
        (0, True, {'max_presences': 0}),
        (1, False, {'max_presences': 1}),
        (1, True, {'max_presences': 1}),
    ):
        data = put_max_presences(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
