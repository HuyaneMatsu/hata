import vampytest

from ..fields import put_focused_into


def test__put_focused_into():
    """
    Tests whether ``put_focused_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'focused': False}),
        (True, False, {'focused': True}),
    ):
        data = put_focused_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
