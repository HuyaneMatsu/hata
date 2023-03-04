import vampytest

from ..fields import put_required_into


def test__put_required_into():
    """
    Tests whether ``put_required_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {'required': False}),
        (False, True, {'required': False}),
        (True, False, {'required': True}),
    ):
        data = put_required_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
