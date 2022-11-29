import vampytest

from ..preinstanced import TeamMemberPermission


def test__TeamMemberPermission__name():
    """
    Tests whether ``TeamMemberPermission`` instance names are all strings.
    """
    for instance in TeamMemberPermission.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__TeamMemberPermission__value():
    """
    Tests whether ``TeamMemberPermission`` instance values are all the expected value type.
    """
    for instance in TeamMemberPermission.INSTANCES.values():
        vampytest.assert_instance(instance.value, TeamMemberPermission.VALUE_TYPE)
