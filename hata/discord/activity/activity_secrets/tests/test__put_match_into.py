import vampytest

from ..fields import put_match_into


def test__put_match_into():
    """
    Tests whether ``put_match_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {}),
        ('a', False, {'match': 'a'}),
    ):
        data = put_match_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
