import vampytest

from ..fields import put_mentionable


def test__put_mentionable():
    """
    Tests whether ``put_mentionable`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'mentionable': False}),
        (True, False, {'mentionable': True}),
    ):
        data = put_mentionable(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
