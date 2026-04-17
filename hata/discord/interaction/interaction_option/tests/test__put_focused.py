import vampytest

from ..fields import put_focused


def test__put_focused():
    """
    Tests whether ``put_focused`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'focused': False}),
        (True, False, {'focused': True}),
    ):
        data = put_focused(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
