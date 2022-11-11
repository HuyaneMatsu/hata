import vampytest

from ...permission import Permission

from ..fields import put_permissions_into


def test__put_permissions_into():
    """
    Tests whether ``put_permissions_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (Permission(0), False, {'permissions': '0'}),
        (Permission(0), True, {'permissions': '0'}),
        (Permission(1), False, {'permissions': '1'}),
    ):
        data = put_permissions_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
