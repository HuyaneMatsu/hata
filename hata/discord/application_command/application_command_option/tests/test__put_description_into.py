import vampytest

from ..fields import put_description_into


def test__put_description_into():
    """
    Tests whether ``put_description_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        ('', False, {'description': ''}),
        ('a', False, {'description': 'a'}),
    ):
        data = put_description_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
