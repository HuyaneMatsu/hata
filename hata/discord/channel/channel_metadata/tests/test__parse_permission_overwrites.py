import vampytest

from ...permission_overwrite import PermissionOverwrite, PermissionOverwriteTargetType

from ..fields import parse_permission_overwrites


def test__parse_permission_overwrites():
    """
    Tests whether ``parse_permission_overwrites`` works as intended.
    """
    permission_overwrite = PermissionOverwrite(202209140016, target_type = PermissionOverwriteTargetType.user)
    
    for input_data, expected_output in (
        ({}, None),
        ({'permission_overwrites': None}, None),
        ({'permission_overwrites': []}, None),
        (
            {'permission_overwrites': [permission_overwrite.to_data(include_internals = True)]},
            {permission_overwrite.target_id: permission_overwrite},
        )
    ):
        output = parse_permission_overwrites(input_data)
        
        vampytest.assert_eq(output, expected_output)
