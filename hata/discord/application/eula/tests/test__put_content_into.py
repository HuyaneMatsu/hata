import vampytest

from ..fields import put_content_into


def test__put_content_into():
    """
    Tests whether ``put_content_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {'content': ''}),
        ('a', False, {'content': 'a'}),
    ):
        data = put_content_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
