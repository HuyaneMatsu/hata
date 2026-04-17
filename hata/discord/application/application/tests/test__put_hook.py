import vampytest

from ..fields import put_hook


def test__put_hook():
    """
    Tests whether ``put_hook`` works as intended.
    """
    for input_, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'hook': False}),
        (True, False, {'hook': True}),
    ):
        data = put_hook(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
