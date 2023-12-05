import vampytest

from ..preinstanced import OrientationLockState


@vampytest.call_from(OrientationLockState.INSTANCES.values())
def test__OrientationLockState__instances(instance):
    """
    Tests whether ``OrientationLockState`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``OrientationLockState``
        The instance to test.
    """
    vampytest.assert_instance(instance, OrientationLockState)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, OrientationLockState.VALUE_TYPE)
