import vampytest

from ..fields import put_text_small_into


def test__put_text_small_into():
    """
    Tests whether ``put_text_small_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {}),
        ('a', False, {'small_text': 'a'}),
    ):
        data = put_text_small_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
