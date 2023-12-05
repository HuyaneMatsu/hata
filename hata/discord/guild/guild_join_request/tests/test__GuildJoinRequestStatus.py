import vampytest

from ..preinstanced import GuildJoinRequestStatus


@vampytest.call_from(GuildJoinRequestStatus.INSTANCES.values())
def test__GuildJoinRequestStatus__instances(instance):
    """
    Tests whether ``GuildJoinRequestStatus`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``GuildJoinRequestStatus``
        The instance to test.
    """
    vampytest.assert_instance(instance, GuildJoinRequestStatus)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, GuildJoinRequestStatus.VALUE_TYPE)
