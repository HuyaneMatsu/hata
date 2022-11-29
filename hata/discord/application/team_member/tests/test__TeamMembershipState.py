import vampytest

from ..preinstanced import TeamMembershipState


def test__TeamMembershipState__name():
    """
    Tests whether ``TeamMembershipState`` instance names are all strings.
    """
    for instance in TeamMembershipState.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__TeamMembershipState__value():
    """
    Tests whether ``TeamMembershipState`` instance values are all the expected value type.
    """
    for instance in TeamMembershipState.INSTANCES.values():
        vampytest.assert_instance(instance.value, TeamMembershipState.VALUE_TYPE)
