import vampytest

from ..preinstanced import TextInputStyle


@vampytest.call_from(TextInputStyle.INSTANCES.values())
def test__TextInputStyle__instances(instance):
    """
    Tests whether ``TextInputStyle`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``TextInputStyle``
        The instance to test.
    """
    vampytest.assert_instance(instance, TextInputStyle)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, TextInputStyle.VALUE_TYPE)
