import vampytest

from ..preinstanced import TeamMemberPermission


@vampytest.call_from(TeamMemberPermission.INSTANCES.values())
def test__TeamMemberPermission__instances(instance):
    """
    Tests whether ``TeamMemberPermission`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``TeamMemberPermission``
        The instance to test.
    """
    vampytest.assert_instance(instance, TeamMemberPermission)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, TeamMemberPermission.VALUE_TYPE)
