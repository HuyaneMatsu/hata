import vampytest

from ..fields import put_enabled_into


def test__put_enabled_into():
    """
    Tests whether ``put_enabled_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (True, False, {}),
        (False, False, {'enabled': False}),
        (True, True, {'enabled': True}),
    ):
        data = put_enabled_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
