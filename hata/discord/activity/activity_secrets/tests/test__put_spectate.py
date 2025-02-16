import vampytest

from ..fields import put_spectate


def test__put_spectate():
    """
    Tests whether ``put_spectate`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {}),
        ('a', False, {'spectate': 'a'}),
    ):
        data = put_spectate(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
