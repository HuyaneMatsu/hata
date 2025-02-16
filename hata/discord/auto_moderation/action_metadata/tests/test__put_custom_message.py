import vampytest

from ..fields import put_custom_message


def test__put_custom_message():
    """
    Tests whether ``put_custom_message`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {'custom_message': ''}),
        ('', False, {'custom_message': ''}),
        ('a', False, {'custom_message': 'a'}),
    ):
        output = put_custom_message(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
