import vampytest

from ..preinstanced import StickerType


@vampytest.call_from(StickerType.INSTANCES.values())
def test__StickerType__instances(instance):
    """
    Tests whether ``StickerType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``StickerType``
        The instance to test.
    """
    vampytest.assert_instance(instance, StickerType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, StickerType.VALUE_TYPE)
