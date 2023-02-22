import vampytest

from ...application_command_permission_overwrite import (
    ApplicationCommandPermissionOverwrite, ApplicationCommandPermissionOverwriteTargetType
)
from ..fields import put_permission_overwrites_into


def test__parse_id():
    """
    Tests whether ``parse_id`` works as intended.
    """
    entity_0 = ApplicationCommandPermissionOverwrite(
        allow = True,
        target = (ApplicationCommandPermissionOverwriteTargetType.role, 202302210032),
    )
    entity_1 = ApplicationCommandPermissionOverwrite(
        allow = True,
        target = (ApplicationCommandPermissionOverwriteTargetType.user, 202302210033),
    )
    
    for input_value, defaults, expected_output in (
        (None, True, {'permissions': []}),
        (
            (entity_0, entity_1,),
            True,
            {'permissions': [entity_0.to_data(defaults = True), entity_1.to_data(defaults = True)]},
        ),
    ):
        output = put_permission_overwrites_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
