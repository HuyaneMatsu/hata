import vampytest

from ..preinstanced import StickerType


def test__StickerType__name():
    """
    Tests whether ``StickerType`` instance names are all strings.
    """
    for instance in StickerType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__StickerType__value():
    """
    Tests whether ``StickerType`` instance values are all the expected value type.
    """
    for instance in StickerType.INSTANCES.values():
        vampytest.assert_instance(instance.value, StickerType.VALUE_TYPE)
