import vampytest

from ..fields import put_launcher_into


def test__put_launcher_into():
    """
    Tests whether ``put_launcher_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'is_launcher': False}),
        (True, False, {'is_launcher': True}),
    ):
        data = put_launcher_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
