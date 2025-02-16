import vampytest

from ..fields import put_required


def test__put_required():
    """
    Tests whether ``put_required`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'required': False}),
        (True, False, {'required': True}),
    ):
        data = put_required(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
