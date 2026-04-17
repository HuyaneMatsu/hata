import vampytest

from ..preinstanced import InviteType


@vampytest.call_from(InviteType.INSTANCES.values())
def test__InviteType__instances(instance):
    """
    Tests whether ``InviteType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``InviteType``
        The instance to test.
    """
    vampytest.assert_instance(instance, InviteType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, InviteType.VALUE_TYPE)
