import vampytest

from ....permission import Permission

from ..fields import put_application_permissions_into


def test__put_application_permissions_into():
    """
    Tests whether ``put_application_permissions_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (Permission(0), False, {'app_permissions': '0'}),
        (Permission(0), True, {'app_permissions': '0'}),
        (Permission(1), False, {'app_permissions': '1'}),
    ):
        data = put_application_permissions_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
