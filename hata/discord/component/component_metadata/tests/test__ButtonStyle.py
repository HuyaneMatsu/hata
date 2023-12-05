import vampytest

from ..preinstanced import ButtonStyle


@vampytest.call_from(ButtonStyle.INSTANCES.values())
def test__ButtonStyle__instances(instance):
    """
    Tests whether ``ButtonStyle`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ButtonStyle``
        The instance to test.
    """
    vampytest.assert_instance(instance, ButtonStyle)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, ButtonStyle.VALUE_TYPE)
