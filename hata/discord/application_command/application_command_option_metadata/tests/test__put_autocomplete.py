import vampytest

from ..fields import put_autocomplete


def test__put_autocomplete():
    """
    Tests whether ``put_autocomplete`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'autocomplete': False}),
        (True, False, {'autocomplete': True}),
    ):
        data = put_autocomplete(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
