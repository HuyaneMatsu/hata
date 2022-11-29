import vampytest

from ..fields import validate_permissions
from ..preinstanced import TeamMemberPermission


def test__validate_permissions__0():
    """
    Tests whether `validate_permissions` works as intended.
    
    Case: passing.
    """
    for input_permissions, expected_output in (
        (None, None),
        ([], None),
        ([TeamMemberPermission.admin], (TeamMemberPermission.admin,)),
        ([TeamMemberPermission.admin.value], (TeamMemberPermission.admin, )),
    ):
        output = validate_permissions(input_permissions)
        vampytest.assert_eq(output, expected_output)


def test__validate_permissions__1():
    """
    Tests whether `validate_permissions` works as intended.
    
    Case: `TypeError`.
    """
    for input_permissions in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_permissions(input_permissions)
