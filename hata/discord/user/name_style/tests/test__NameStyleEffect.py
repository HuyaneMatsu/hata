import vampytest

from ..preinstanced import NameStyleEffect


@vampytest.call_from(NameStyleEffect.INSTANCES.values())
def test__NameStyleEffect__instances(instance):
    """
    Tests whether ``NameStyleEffect`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``NameStyleEffect``
        The instance to test.
    """
    vampytest.assert_instance(instance, NameStyleEffect)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, NameStyleEffect.VALUE_TYPE)
