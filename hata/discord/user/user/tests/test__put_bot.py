import vampytest

from ..fields import put_bot


def test__put_bot():
    """
    Tests whether ``put_bot`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {'bot': False}),
        (False, True, {'bot': False}),
        (True, False, {'bot': True}),
    ):
        data = put_bot(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
