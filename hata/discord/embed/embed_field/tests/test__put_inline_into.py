import vampytest

from ..fields import put_inline_into


def test__put_inline_into():
    """
    Tests whether ``put_inline_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'inline': False}),
        (True, False, {'inline': True}),
    ):
        data = put_inline_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
