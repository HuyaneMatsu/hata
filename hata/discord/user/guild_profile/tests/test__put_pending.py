import vampytest

from ..fields import put_pending


def test__put_pending():
    """
    Tests whether ``put_pending`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'pending': False}),
        (True, False, {'pending': True}),
    ):
        data = put_pending(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
