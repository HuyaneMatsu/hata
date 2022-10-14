import vampytest

from ..fields import put_show_activity_into


def test__put_show_activity_into():
    """
    Tests whether ``put_show_activity_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'show_activity': False}),
        (True, False, {'show_activity': True}),
    ):
        data = put_show_activity_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
