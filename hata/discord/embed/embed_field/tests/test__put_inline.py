import vampytest

from ..fields import put_inline


def test__put_inline():
    """
    Tests whether ``put_inline`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'inline': False}),
        (True, False, {'inline': True}),
    ):
        data = put_inline(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
