import vampytest

from ...media_item import MediaItem

from ..media_gallery import ComponentMetadataMediaGallery

from .test__ComponentMetadataMediaGallery__constructor import _assert_fields_set


def test__ComponentMetadataMediaGallery__from_data():
    """
    Tests whether ``ComponentMetadataMediaGallery.from_data`` works as intended.
    """
    items = [MediaItem('https://orindance.party/')]
    
    data = {
        'items': [component.to_data() for component in items]
    }
    
    component_metadata = ComponentMetadataMediaGallery.from_data(data)
    _assert_fields_set(component_metadata)
    vampytest.assert_eq(component_metadata.items, tuple(items))


def test__ComponentMetadataMediaGallery__to_data():
    """
    Tests whether ``ComponentMetadataMediaGallery.to_data`` works as intended.
    
    Case: include defaults.
    """
    items = [MediaItem('https://orindance.party/')]
    
    component_metadata = ComponentMetadataMediaGallery(
        items = items,
    )
    
    vampytest.assert_eq(
        component_metadata.to_data(
            defaults = True,
        ),
        {
            'items': [component.to_data(defaults = True) for component in items]
        },
    )
