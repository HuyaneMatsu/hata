import vampytest

from ..fields import put_match


def test__put_match():
    """
    Tests whether ``put_match`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {}),
        ('a', False, {'match': 'a'}),
    ):
        data = put_match(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
