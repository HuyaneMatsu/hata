import vampytest

from ..fields import put_single_select


def test__put_single_select():
    """
    Tests whether ``put_single_select`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {'single_select': False}),
        (False, True, {'single_select': False}),
        (True, False, {'single_select': True}),
    ):
        data = put_single_select(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
