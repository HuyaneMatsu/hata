import vampytest

from ..fields import put_nick


def test__put_nick():
    """
    Tests whether ``put_nick`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {}),
        ('a', False, {'nick': 'a'}),
    ):
        data = put_nick(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
