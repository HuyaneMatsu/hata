import vampytest

from ....guild import Guild

from ...media_item import MediaItem

from ..media_gallery import ComponentMetadataMediaGallery

from .test__ComponentMetadataMediaGallery__constructor import _assert_fields_set


def test__ComponentMetadataMediaGallery__clean_copy():
    """
    Tests whether ``ComponentMetadataMediaGallery.clean_copy`` works as intended.
    """
    guild_id = 202505030020
    guild = Guild.precreate(guild_id)
    
    items = [MediaItem('https://orindance.party/')]
    
    component_metadata = ComponentMetadataMediaGallery(
        items = items,
    )
    copy = component_metadata.clean_copy(guild)
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, component_metadata)
    vampytest.assert_eq(copy, component_metadata)


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


def _iter_options__iter_contents():
    items = [
        MediaItem('https://orindance.party/'),
        MediaItem('https://orindance.party/orin.png'),
    ]
    
    yield (
        {},
        [],
    )
    
    yield (
        {
            'items': items,
        },
        [],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_contents()).returning_last())
def test__ComponentMetadataMediaGallery__iter_contents(keyword_parameters):
    """
    Tests whether ``ComponentMetadataMediaGallery.iter_contents`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `list<str>`
    """
    component_metadata = ComponentMetadataMediaGallery(**keyword_parameters)
    output = [*component_metadata.iter_contents()]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return output
