import vampytest

from ..fields import put_moderated_into


def test__put_moderated_into():
    """
    Tests whether ``put_moderated_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'moderated': False}),
        (True, False, {'moderated': True}),
    ):
        data = put_moderated_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
