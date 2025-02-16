import vampytest

from ..fields import put_text_large


def test__put_text_large():
    """
    Tests whether ``put_text_large`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {}),
        ('a', False, {'large_text': 'a'}),
    ):
        data = put_text_large(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
