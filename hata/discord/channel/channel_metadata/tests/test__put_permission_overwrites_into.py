import vampytest

from ...permission_overwrite import PermissionOverwrite, PermissionOverwriteTargetType

from ..fields import put_permission_overwrites_into


def test__put_permission_overwrites_into():
    """
    Tests whether ``put_permission_overwrites_into`` works as intended.
    """
    permission_overwrite = PermissionOverwrite(202209140017, target_type = PermissionOverwriteTargetType.user)
    
    for input_value, defaults, expected_output in (
        ({}, False, {'permission_overwrites': []}),
        (
            {permission_overwrite.target_id: permission_overwrite},
            False,
            {'permission_overwrites': [permission_overwrite.to_data(include_internals = True)]}
        ),
    ):
        data = put_permission_overwrites_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
