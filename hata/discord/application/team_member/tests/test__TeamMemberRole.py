import vampytest

from ..preinstanced import TeamMemberRole


@vampytest.call_from(TeamMemberRole.INSTANCES.values())
def test__TeamMemberRole__instances(instance):
    """
    Tests whether ``TeamMemberRole`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``TeamMemberRole``
        The instance to test.
    """
    vampytest.assert_instance(instance, TeamMemberRole)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, TeamMemberRole.VALUE_TYPE)
