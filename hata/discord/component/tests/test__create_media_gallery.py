import vampytest

from ..component import Component, ComponentType
from ..media_item import MediaItem
from ..utils import create_media_gallery


def test__create_media_gallery():
    """
    Tests whether ``create_media_gallery`` works as intended.
    """
    item_0 = MediaItem('https://orindance.party/')
    item_1 = MediaItem('https://www.astil.dev/')
    
    component = create_media_gallery(
        item_0,
        item_1,
    )
    
    vampytest.assert_instance(component, Component)
    vampytest.assert_is(component.type, ComponentType.media_gallery)
    vampytest.assert_eq(component.items, (item_0, item_1))
