import vampytest

from ..preinstanced import StickerFormat


def test__StickerFormat__name():
    """
    Tests whether ``StickerFormat`` instance names are all strings.
    """
    for instance in StickerFormat.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__StickerFormat__value():
    """
    Tests whether ``StickerFormat`` instance values are all the expected value type.
    """
    for instance in StickerFormat.INSTANCES.values():
        vampytest.assert_instance(instance.value, StickerFormat.VALUE_TYPE)
