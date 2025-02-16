import vampytest

from ....permission import Permission

from ..fields import put_required_permissions


def test__put_required_permissions():
    """
    Tests whether ``put_required_permissions`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (Permission(0), False, {'default_member_permissions': None}),
        (Permission(0), True, {'default_member_permissions': None}),
        (Permission(1), False, {'default_member_permissions': '1'}),
    ):
        data = put_required_permissions(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
