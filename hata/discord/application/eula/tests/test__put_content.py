import vampytest

from ..fields import put_content


def test__put_content():
    """
    Tests whether ``put_content`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {'content': ''}),
        ('a', False, {'content': 'a'}),
    ):
        data = put_content(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
