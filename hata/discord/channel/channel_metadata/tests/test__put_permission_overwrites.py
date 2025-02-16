import vampytest

from ...permission_overwrite import PermissionOverwrite, PermissionOverwriteTargetType

from ..fields import put_permission_overwrites


def test__put_permission_overwrites():
    """
    Tests whether ``put_permission_overwrites`` works as intended.
    """
    permission_overwrite = PermissionOverwrite(202209140017, target_type = PermissionOverwriteTargetType.user)
    
    for input_value, defaults, expected_output in (
        (None, False, {'permission_overwrites': []}),
        (
            {permission_overwrite.target_id: permission_overwrite},
            False,
            {'permission_overwrites': [permission_overwrite.to_data(include_internals = True)]}
        ),
    ):
        data = put_permission_overwrites(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
