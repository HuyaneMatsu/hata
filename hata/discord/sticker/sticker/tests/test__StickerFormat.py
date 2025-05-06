import vampytest

from ..preinstanced import StickerFormat


def _assert_fields_set(sticker_format):
    """
    Asserts whether every field are set of the given sticker format.
    
    Parameters
    ----------
    sticker_format : ``StickerFormat``
        The instance to test.
    """
    vampytest.assert_instance(sticker_format, StickerFormat)
    vampytest.assert_instance(sticker_format.name, str)
    vampytest.assert_instance(sticker_format.value, StickerFormat.VALUE_TYPE)
    vampytest.assert_instance(sticker_format.extension, str)


@vampytest.call_from(StickerFormat.INSTANCES.values())
def test__StickerFormat__instances(instance):
    """
    Tests whether ``StickerFormat`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``StickerFormat``
        The instance to test.
    """
    _assert_fields_set(instance)


def test__StickerFormat__new__min_fields():
    """
    Tests whether ``StickerFormat.__new__`` works as intended.
    
    Case: minimal amount of fields given.
    """
    value = 30
    
    try:
        output = StickerFormat(value)
        _assert_fields_set(output)
        
        vampytest.assert_eq(output.value, value)
        vampytest.assert_eq(output.name, StickerFormat.NAME_DEFAULT)
        vampytest.assert_eq(output.extension, 'png')
        vampytest.assert_is(StickerFormat.INSTANCES.get(value, None), output)
    
    finally:
        try:
            del StickerFormat.INSTANCES[value]
        except KeyError:
            pass
