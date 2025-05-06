import vampytest

from ..fields import put_allow


def test__put_allow():
    """
    Tests whether ``put_allow`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (True, True, {'permission': True}),
        (False, True, {'permission': False}),
        (True, False, {'permission': True}),
        (False, False, {'permission': False}),
    ):
        data = put_allow(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
