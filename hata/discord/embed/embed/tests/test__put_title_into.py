import vampytest

from ..fields import put_title_into


def test__put_title_into():
    """
    Tests whether ``put_title_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'title': ''}),
        ('a', False, {'title': 'a'}),
    ):
        data = put_title_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
