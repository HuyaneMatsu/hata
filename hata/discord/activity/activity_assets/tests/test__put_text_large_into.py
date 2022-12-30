import vampytest

from ..fields import put_text_large_into


def test__put_text_large_into():
    """
    Tests whether ``put_text_large_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (None, False, {}),
        ('a', False, {'large_text': 'a'}),
    ):
        data = put_text_large_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
