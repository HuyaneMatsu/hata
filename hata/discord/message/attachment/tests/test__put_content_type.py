import vampytest

from ..fields import put_content_type


def test__put_content_type():
    """
    Tests whether ``put_content_type`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {'content_type': ''}),
        ('a', False, {'content_type': 'a'}),
    ):
        data = put_content_type(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
