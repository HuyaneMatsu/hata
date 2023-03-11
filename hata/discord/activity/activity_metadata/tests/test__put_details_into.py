import vampytest

from ..fields import put_details_into


def test__put_details_into():
    """
    Tests whether ``put_details_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {}),
        ('a', False, {'details': 'a'}),
    ):
        data = put_details_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
