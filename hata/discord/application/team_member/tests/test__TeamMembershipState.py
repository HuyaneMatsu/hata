import vampytest

from ..preinstanced import TeamMembershipState


@vampytest.call_from(TeamMembershipState.INSTANCES.values())
def test__TeamMembershipState__instances(instance):
    """
    Tests whether ``TeamMembershipState`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``TeamMembershipState``
        The instance to test.
    """
    vampytest.assert_instance(instance, TeamMembershipState)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, TeamMembershipState.VALUE_TYPE)
