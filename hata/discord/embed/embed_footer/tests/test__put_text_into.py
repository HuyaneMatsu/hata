import vampytest

from ..fields import put_text_into


def test__put_text_into():
    """
    Tests whether ``put_text_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (None, False, {'text': ''}),
        ('', False, {'text': ''}),
        ('a', False, {'text': 'a'}),
    ):
        data = put_text_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
