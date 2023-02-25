import vampytest

from ..fields import put_autocomplete_into


def test__put_autocomplete_into():
    """
    Tests whether ``put_autocomplete_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'autocomplete': False}),
        (True, False, {'autocomplete': True}),
    ):
        data = put_autocomplete_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
