import vampytest

from ..fields import put_spectate_into


def test__put_spectate_into():
    """
    Tests whether ``put_spectate_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {}),
        ('a', False, {'spectate': 'a'}),
    ):
        data = put_spectate_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
