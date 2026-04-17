import vampytest

from ..fields import put_invite_code


def test__put_invite_code():
    """
    Tests whether ``put_invite_code`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'invite_code': None}),
        ('a', False, {'invite_code': 'a'}),
    ):
        data = put_invite_code(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
