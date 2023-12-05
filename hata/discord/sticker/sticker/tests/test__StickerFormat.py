import vampytest

from ..preinstanced import StickerFormat


@vampytest.call_from(StickerFormat.INSTANCES.values())
def test__StickerFormat__instances(instance):
    """
    Tests whether ``StickerFormat`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``StickerFormat``
        The instance to test.
    """
    vampytest.assert_instance(instance, StickerFormat)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, StickerFormat.VALUE_TYPE)
