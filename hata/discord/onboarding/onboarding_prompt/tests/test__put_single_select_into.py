import vampytest

from ..fields import put_single_select_into


def test__put_single_select_into():
    """
    Tests whether ``put_single_select_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {'single_select': False}),
        (False, True, {'single_select': False}),
        (True, False, {'single_select': True}),
    ):
        data = put_single_select_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
