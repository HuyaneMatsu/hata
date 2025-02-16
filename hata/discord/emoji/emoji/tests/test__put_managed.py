import vampytest

from ..fields import put_managed


def test__put_managed():
    """
    Tests whether ``put_managed`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'managed': False}),
        (True, False, {'managed': True}),
    ):
        data = put_managed(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
