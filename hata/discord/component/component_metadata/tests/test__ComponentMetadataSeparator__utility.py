import vampytest

from ....guild import Guild

from ..preinstanced import SeparatorSpacingSize
from ..separator import ComponentMetadataSeparator

from .test__ComponentMetadataSeparator__constructor import _assert_fields_set


def test__ComponentMetadataSeparator__clean_copy():
    """
    Tests whether ``ComponentMetadataSeparator.clean_copy`` works as intended.
    """
    guild_id = 202505030029
    guild = Guild.precreate(guild_id)
    
    divider = False
    spacing_size = SeparatorSpacingSize.large
    
    component_metadata = ComponentMetadataSeparator(
        divider = divider,
        spacing_size = spacing_size,
    )
    copy = component_metadata.clean_copy(guild)
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, component_metadata)
    vampytest.assert_eq(copy, component_metadata)


def test__ComponentMetadataSeparator__copy():
    """
    Tests whether ``ComponentMetadataSeparator.copy`` works as intended.
    """
    divider = False
    spacing_size = SeparatorSpacingSize.large
    
    component_metadata = ComponentMetadataSeparator(
        divider = divider,
        spacing_size = spacing_size,
    )
    copy = component_metadata.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(component_metadata, copy)


def test__ComponentMetadataSeparator__copy_with__no_fields():
    """
    Tests whether ``ComponentMetadataSeparator.copy_with`` works as intended.
    
    Case: no fields.
    """
    divider = False
    spacing_size = SeparatorSpacingSize.large
    
    component_metadata = ComponentMetadataSeparator(
        divider = divider,
        spacing_size = spacing_size,
    )
    copy = component_metadata.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(component_metadata, copy)


def test__ComponentMetadataSeparator__copy_with__all_fields():
    """
    Tests whether ``ComponentMetadataSeparator.copy_with`` works as intended.
    
    Case: all fields.
    """
    old_divider = False
    old_spacing_size = SeparatorSpacingSize.large
    
    new_divider = True
    new_spacing_size = SeparatorSpacingSize.small
    
    component_metadata = ComponentMetadataSeparator(
        divider = old_divider,
        spacing_size = old_spacing_size,
    )
    copy = component_metadata.copy_with(
        divider = new_divider,
        spacing_size = new_spacing_size,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy.divider, new_divider)
    vampytest.assert_is(copy.spacing_size, new_spacing_size)


def test__ComponentMetadataSeparator__copy_with_keyword_parameters__no_fields():
    """
    Tests whether ``ComponentMetadataSeparator.copy_with_keyword_parameters`` works as intended.
    
    Case: no fields.
    """
    divider = False
    spacing_size = SeparatorSpacingSize.large
    
    component_metadata = ComponentMetadataSeparator(
        divider = divider,
        spacing_size = spacing_size,
    )
    copy = component_metadata.copy_with_keyword_parameters({})
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(component_metadata, copy)


def test__ComponentMetadataSeparator__copy_with_keyword_parameters__all_fields():
    """
    Tests whether ``ComponentMetadataSeparator.copy_with_keyword_parameters`` works as intended.
    
    Case: all fields.
    """
    old_divider = False
    old_spacing_size = SeparatorSpacingSize.large
    
    new_divider = True
    new_spacing_size = SeparatorSpacingSize.small
    
    component_metadata = ComponentMetadataSeparator(
        divider = old_divider,
        spacing_size = old_spacing_size,
    )
    copy = component_metadata.copy_with_keyword_parameters({
        'divider': new_divider,
        'spacing_size': new_spacing_size,
    })
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy.divider, new_divider)
    vampytest.assert_is(copy.spacing_size, new_spacing_size)


def _iter_options__iter_contents():
    divider = False
    spacing_size = SeparatorSpacingSize.large
    
    yield (
        {},
        [],
    )
    
    yield (
        {
            'divider': divider,
            'spacing_size': spacing_size,
        },
        [],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_contents()).returning_last())
def test__ComponentMetadataSeparator__iter_contents(keyword_parameters):
    """
    Tests whether ``ComponentMetadataSeparator.iter_contents`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `list<str>`
    """
    component_metadata = ComponentMetadataSeparator(**keyword_parameters)
    output = [*component_metadata.iter_contents()]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return output
