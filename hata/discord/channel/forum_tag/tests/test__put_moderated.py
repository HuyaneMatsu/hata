import vampytest

from ..fields import put_moderated


def test__put_moderated():
    """
    Tests whether ``put_moderated`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'moderated': False}),
        (True, False, {'moderated': True}),
    ):
        data = put_moderated(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
