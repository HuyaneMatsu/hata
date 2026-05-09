import vampytest

from ..preinstanced import NameStyleFont


def _assert_fields_set(sticker_format):
    """
    Asserts whether every field are set of the given sticker format.
    
    Parameters
    ----------
    sticker_format : ``NameStyleFont``
        The instance to test.
    """
    vampytest.assert_instance(sticker_format, NameStyleFont)
    vampytest.assert_instance(sticker_format.name, str)
    vampytest.assert_instance(sticker_format.value, NameStyleFont.VALUE_TYPE)
    vampytest.assert_instance(sticker_format.display_name, str)
    vampytest.assert_instance(sticker_format.font_name, str)


@vampytest.call_from(NameStyleFont.INSTANCES.values())
def test__NameStyleFont__instances(instance):
    """
    Tests whether ``NameStyleFont`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``NameStyleFont``
        The instance to test.
    """
    _assert_fields_set(instance)


def test__NameStyleFont__new__min_fields():
    """
    Tests whether ``NameStyleFont.__new__`` works as intended.
    
    Case: minimal amount of fields given.
    """
    value = 30
    
    try:
        output = NameStyleFont(value)
        _assert_fields_set(output)
        
        vampytest.assert_eq(output.value, value)
        vampytest.assert_eq(output.name, NameStyleFont.NAME_DEFAULT)
        vampytest.assert_eq(output.display_name, '')
        vampytest.assert_eq(output.font_name, '')
        vampytest.assert_is(NameStyleFont.INSTANCES.get(value, None), output)
    
    finally:
        try:
            del NameStyleFont.INSTANCES[value]
        except KeyError:
            pass
