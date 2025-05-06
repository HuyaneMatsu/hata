import vampytest

from ...color import Color

from ..preinstanced import AnsiForegroundColor


def _assert_fields_set(ansi_foreground_color):
    """
    Asserts whether every field are set of the given ansi foreground color.
    
    Parameters
    ----------
    ansi_foreground_color : ``AnsiForegroundColor``
        The instance to test.
    """
    vampytest.assert_instance(ansi_foreground_color, AnsiForegroundColor)
    vampytest.assert_instance(ansi_foreground_color.name, str)
    vampytest.assert_instance(ansi_foreground_color.value, AnsiForegroundColor.VALUE_TYPE)
    vampytest.assert_instance(ansi_foreground_color.color, Color)
    vampytest.assert_instance(ansi_foreground_color.color_name, str)


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


def test__AnsiForegroundColor__new__min_fields():
    """
    Tests whether ``AnsiForegroundColor.__new__`` works as intended.
    
    Case: minimal amount of fields given.
    """
    value = 50
    
    try:
        output = AnsiForegroundColor(value)
        _assert_fields_set(output)
        
        vampytest.assert_eq(output.value, value)
        vampytest.assert_eq(output.name, AnsiForegroundColor.NAME_DEFAULT)
        vampytest.assert_eq(output.color, Color())
        vampytest.assert_eq(output.color_name, AnsiForegroundColor.NAME_DEFAULT)
        vampytest.assert_is(AnsiForegroundColor.INSTANCES.get(value, None), output)
    
    finally:
        try:
            del AnsiForegroundColor.INSTANCES[value]
        except KeyError:
            pass
