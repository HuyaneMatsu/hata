import vampytest

from ..preinstanced import GuildJoinRequestStatus


def test__GuildJoinRequestStatus__name():
    """
    Tests whether ``GuildJoinRequestStatus`` instance names are all strings.
    """
    for instance in GuildJoinRequestStatus.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__GuildJoinRequestStatus__value():
    """
    Tests whether ``GuildJoinRequestStatus`` instance values are all the expected value type.
    """
    for instance in GuildJoinRequestStatus.INSTANCES.values():
        vampytest.assert_instance(instance.value, GuildJoinRequestStatus.VALUE_TYPE)
