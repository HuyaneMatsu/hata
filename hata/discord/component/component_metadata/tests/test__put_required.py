import vampytest

from ..fields import put_required


def test__put_required():
    """
    Tests whether ``put_required`` is working as intended.
    """
    for input_value, required, expected_output in (
        (True, False, {}),
        (False, False, {'required': False}),
        (True, True, {'required': True}),
    ):
        data = put_required(input_value, {}, required)
        vampytest.assert_eq(data, expected_output)
