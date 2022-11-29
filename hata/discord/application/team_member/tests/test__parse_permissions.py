import vampytest

from ..fields import parse_permissions
from ..preinstanced import TeamMemberPermission

def test__parse_permissions():
    """
    Tests whether ``parse_permissions`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'permissions': None}, None),
        ({'permissions': []}, None),
        ({'permissions': [TeamMemberPermission.admin.value]}, (TeamMemberPermission.admin, )),
    ):
        output = parse_permissions(input_data)
        vampytest.assert_eq(output, expected_output)
