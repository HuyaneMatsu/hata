import vampytest

from ..preinstanced import InviteAllowedUserIdsStatusStatus


@vampytest.call_from(InviteAllowedUserIdsStatusStatus.INSTANCES.values())
def test__InviteAllowedUserIdsStatusStatus__instances(instance):
    """
    Tests whether ``InviteAllowedUserIdsStatusStatus`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``InviteAllowedUserIdsStatusStatus``
        The instance to test.
    """
    vampytest.assert_instance(instance, InviteAllowedUserIdsStatusStatus)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, InviteAllowedUserIdsStatusStatus.VALUE_TYPE)
