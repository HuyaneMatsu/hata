import vampytest

from ..preinstanced import PremiumType


@vampytest.call_from(PremiumType.INSTANCES.values())
def test__PremiumType__instances(instance):
    """
    Tests whether ``PremiumType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``PremiumType``
        The instance to test.
    """
    vampytest.assert_instance(instance, PremiumType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, PremiumType.VALUE_TYPE)
