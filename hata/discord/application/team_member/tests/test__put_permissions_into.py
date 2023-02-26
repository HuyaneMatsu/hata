import vampytest

from ..fields import put_permissions_into
from ..preinstanced import TeamMemberPermission


def test__put_permissions_into():
    """
    Tests whether ``put_permissions_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (None, True, {'permissions': []}),
        ((TeamMemberPermission.admin, ), False, {'permissions': [TeamMemberPermission.admin.value]}),
    ):
        data = put_permissions_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
