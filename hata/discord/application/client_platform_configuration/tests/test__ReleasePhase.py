import vampytest

from ..preinstanced import ReleasePhase


@vampytest.call_from(ReleasePhase.INSTANCES.values())
def test__ReleasePhase__instances(instance):
    """
    Tests whether ``ReleasePhase`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ReleasePhase``
        The instance to test.
    """
    vampytest.assert_instance(instance, ReleasePhase)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, ReleasePhase.VALUE_TYPE)
