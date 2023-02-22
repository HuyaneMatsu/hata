import vampytest

from ...application_command_permission_overwrite import (
    ApplicationCommandPermissionOverwrite, ApplicationCommandPermissionOverwriteTargetType
)
from ..fields import parse_permission_overwrites


def test__parse_id():
    """
    Tests whether ``parse_id`` works as intended.
    """
    entity_0 = ApplicationCommandPermissionOverwrite(
        allow = True,
        target = (ApplicationCommandPermissionOverwriteTargetType.role, 202302210030),
    )
    entity_1 = ApplicationCommandPermissionOverwrite(
        allow = True,
        target = (ApplicationCommandPermissionOverwriteTargetType.user, 202302210031),
    )
    
    for input_data, expected_output in (
        ({}, None),
        ({'permissions': None}, None),
        ({'permissions': [entity_0.to_data(), entity_1.to_data()]}, (entity_0, entity_1,)),
    ):
        output = parse_permission_overwrites(input_data)
        vampytest.assert_eq(output, expected_output)
