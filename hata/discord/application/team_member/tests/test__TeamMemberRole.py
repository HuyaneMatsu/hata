import vampytest

from ..preinstanced import TeamMemberRole


def test__TeamMemberRole__name():
    """
    Tests whether ``TeamMemberRole`` instance names are all strings.
    """
    for instance in TeamMemberRole.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__TeamMemberRole__value():
    """
    Tests whether ``TeamMemberRole`` instance values are all the expected value type.
    """
    for instance in TeamMemberRole.INSTANCES.values():
        vampytest.assert_instance(instance.value, TeamMemberRole.VALUE_TYPE)
