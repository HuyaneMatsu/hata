import vampytest

from ...media_item import MediaItem

from ..media_gallery import ComponentMetadataMediaGallery

from .test__ComponentMetadataMediaGallery__constructor import _assert_fields_set


def test__ComponentMetadataMediaGallery__copy():
    """
    Tests whether ``ComponentMetadataMediaGallery.copy`` works as intended.
    """
    items = [MediaItem('https://orindance.party/')]
    
    component_metadata = ComponentMetadataMediaGallery(
        items = items,
    )
    copy = component_metadata.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(component_metadata, copy)


def test__ComponentMetadataMediaGallery__copy_with__no_fields():
    """
    Tests whether ``ComponentMetadataMediaGallery.copy_with`` works as intended.
    
    Case: no fields.
    """
    items = [MediaItem('https://orindance.party/')]
    
    component_metadata = ComponentMetadataMediaGallery(
        items = items,
    )
    copy = component_metadata.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(component_metadata, copy)


def test__ComponentMetadataMediaGallery__copy_with__all_fields():
    """
    Tests whether ``ComponentMetadataMediaGallery.copy_with`` works as intended.
    
    Case: all fields.
    """
    old_items = [MediaItem('https://orindance.party/')]
    
    new_items = [MediaItem('https://www.astil.dev/')]
    
    component_metadata = ComponentMetadataMediaGallery(
        items = old_items,
    )
    copy = component_metadata.copy_with(
        items = new_items,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy.items, tuple(new_items))


def test__ComponentMetadataMediaGallery__copy_with_keyword_parameters__no_fields():
    """
    Tests whether ``ComponentMetadataMediaGallery.copy_with_keyword_parameters`` works as intended.
    
    Case: no fields.
    """
    items = [MediaItem('https://orindance.party/')]
    
    component_metadata = ComponentMetadataMediaGallery(
        items = items,
    )
    copy = component_metadata.copy_with_keyword_parameters({})
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(component_metadata, copy)


def test__ComponentMetadataMediaGallery__copy_with_keyword_parameters__all_fields():
    """
    Tests whether ``ComponentMetadataMediaGallery.copy_with_keyword_parameters`` works as intended.
    
    Case: all fields.
    """
    old_items = [MediaItem('https://orindance.party/')]
    
    new_items = [MediaItem('https://www.astil.dev/')]
    
    component_metadata = ComponentMetadataMediaGallery(
        items = old_items,
    )
    copy = component_metadata.copy_with_keyword_parameters({
        'items': new_items,
    })
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy.items, tuple(new_items))
