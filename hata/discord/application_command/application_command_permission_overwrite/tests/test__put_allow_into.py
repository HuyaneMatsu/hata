import vampytest

from ..fields import put_allow_into


def test__put_allow_into():
    """
    Tests whether ``put_allow_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (True, True, {'permission': True}),
        (False, True, {'permission': False}),
        (True, False, {'permission': True}),
        (False, False, {'permission': False}),
    ):
        data = put_allow_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
