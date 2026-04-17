import vampytest

from ..fields import put_default


def test__put_default():
    """
    Tests whether ``put_default`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'default': False}),
        (True, False, {'default': True}),
    ):
        data = put_default(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
