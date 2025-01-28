import vampytest

from ..preinstanced import AnsiForegroundColor


def _assert_fields_set(ansi_text_decoration):
    """
    Asserts whether every field are set of the given ansi text decoration.
    
    Parameters
    ----------
    ansi_text_decoration : ``AnsiForegroundColor``
        The instance to test.
    """
    vampytest.assert_instance(ansi_text_decoration, AnsiForegroundColor)
    vampytest.assert_instance(ansi_text_decoration.name, str)
    vampytest.assert_instance(ansi_text_decoration.value, AnsiForegroundColor.VALUE_TYPE)


@vampytest.call_from(AnsiForegroundColor.INSTANCES.values())
def test__AnsiForegroundColor__instances(instance):
    """
    Tests whether ``AnsiForegroundColor`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``AnsiForegroundColor``
        The instance to test.
    """
    _assert_fields_set(instance)
