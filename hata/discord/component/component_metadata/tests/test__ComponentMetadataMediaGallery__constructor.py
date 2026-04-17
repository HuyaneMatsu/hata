import vampytest

from ...media_item import MediaItem

from ..media_gallery import ComponentMetadataMediaGallery


def _assert_fields_set(component_metadata):
    """
    Checks whether the given component metadata has all it's attributes set.
    
    Parameters
    ----------
    component_metadata : ``ComponentMetadataMediaGallery``
        Component metadata to test.
    """
    vampytest.assert_instance(component_metadata, ComponentMetadataMediaGallery)
    vampytest.assert_instance(component_metadata.items, tuple, nullable = True)


def test__ComponentMetadataMediaGallery__new__no_fields():
    """
    Tests whether ``ComponentMetadataMediaGallery.__new__`` works as intended.
    
    Case: No fields.
    """
    component_metadata = ComponentMetadataMediaGallery()
    _assert_fields_set(component_metadata)


def test__ComponentMetadataMediaGallery__new__all_fields():
    """
    Tests whether ``ComponentMetadataMediaGallery.__new__`` works as intended.
    
    Case: All fields.
    """
    items = [MediaItem('https://orindance.party/')]
    
    component_metadata = ComponentMetadataMediaGallery(
        items = items,
    )
    _assert_fields_set(component_metadata)
    vampytest.assert_eq(component_metadata.items, tuple(items))


def test__ComponentMetadataMediaGallery__from_keyword_parameters__no_fields():
    """
    Tests whether ``ComponentMetadataMediaGallery.from_keyword_parameters`` works as intended.
    
    Case: No fields.
    """
    keyword_parameters = {}
    
    component_metadata = ComponentMetadataMediaGallery.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)


def test__ComponentMetadataMediaGallery__from_keyword_parameters__all_fields():
    """
    Tests whether ``ComponentMetadataMediaGallery.from_keyword_parameters`` works as intended.
    
    Case: All fields.
    """
    items = [MediaItem('https://orindance.party/')]
    
    keyword_parameters = {
        'items': items,
    }
    
    component_metadata = ComponentMetadataMediaGallery.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)
    vampytest.assert_eq(component_metadata.items, tuple(items))
