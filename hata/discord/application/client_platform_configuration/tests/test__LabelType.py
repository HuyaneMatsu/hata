import vampytest

from ..preinstanced import LabelType


@vampytest.call_from(LabelType.INSTANCES.values())
def test__LabelType__instances(instance):
    """
    Tests whether ``LabelType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``LabelType``
        The instance to test.
    """
    vampytest.assert_instance(instance, LabelType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, LabelType.VALUE_TYPE)
