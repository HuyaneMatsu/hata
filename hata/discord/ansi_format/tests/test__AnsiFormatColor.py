import vampytest

from ...color import Color

from ..preinstanced import AnsiBackgroundColor


def _assert_fields_set(ansi_background_color):
    """
    Asserts whether every field are set of the given ansi background color.
    
    Parameters
    ----------
    ansi_background_color : ``AnsiBackgroundColor``
        The instance to test.
    """
    vampytest.assert_instance(ansi_background_color, AnsiBackgroundColor)
    vampytest.assert_instance(ansi_background_color.name, str)
    vampytest.assert_instance(ansi_background_color.value, AnsiBackgroundColor.VALUE_TYPE)
    vampytest.assert_instance(ansi_background_color.color, Color)
    vampytest.assert_instance(ansi_background_color.color_name, str)


@vampytest.call_from(AnsiBackgroundColor.INSTANCES.values())
def test__AnsiBackgroundColor__instances(instance):
    """
    Tests whether ``AnsiBackgroundColor`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``AnsiBackgroundColor``
        The instance to test.
    """
    _assert_fields_set(instance)


def test__AnsiBackgroundColor__new__min_fields():
    """
    Tests whether ``AnsiBackgroundColor.__new__`` works as intended.
    
    Case: minimal amount of fields given.
    """
    value = 50
    
    try:
        output = AnsiBackgroundColor(value)
        _assert_fields_set(output)
        
        vampytest.assert_eq(output.value, value)
        vampytest.assert_eq(output.name, AnsiBackgroundColor.NAME_DEFAULT)
        vampytest.assert_eq(output.color, Color())
        vampytest.assert_eq(output.color_name, AnsiBackgroundColor.NAME_DEFAULT)
        vampytest.assert_is(AnsiBackgroundColor.INSTANCES.get(value, None), output)
    
    finally:
        try:
            del AnsiBackgroundColor.INSTANCES[value]
        except KeyError:
            pass
