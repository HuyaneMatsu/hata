import vampytest

from ..fields import put_required_into


def test__put_required_into():
    """
    Tests whether ``put_required_into`` is working as intended.
    """
    for input_value, required, expected_output in (
        (True, False, {}),
        (False, False, {'required': False}),
        (True, True, {'required': True}),
    ):
        data = put_required_into(input_value, {}, required)
        vampytest.assert_eq(data, expected_output)
