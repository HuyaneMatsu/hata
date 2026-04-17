import vampytest

from ..preinstanced import InviteTargetType


@vampytest.call_from(InviteTargetType.INSTANCES.values())
def test__InviteTargetType__instances(instance):
    """
    Tests whether ``InviteTargetType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``InviteTargetType``
        The instance to test.
    """
    vampytest.assert_instance(instance, InviteTargetType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, InviteTargetType.VALUE_TYPE)
