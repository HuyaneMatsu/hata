import vampytest

from ..fields import put_mentionable_into


def test__put_mentionable_into():
    """
    Tests whether ``put_mentionable_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'mentionable': False}),
        (True, False, {'mentionable': True}),
    ):
        data = put_mentionable_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
