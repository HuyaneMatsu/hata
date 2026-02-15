import vampytest

from ....guild import Guild

from ..checkbox import ComponentMetadataCheckbox

from .test__ComponentMetadataCheckbox__constructor import _assert_fields_set


def test__ComponentMetadataCheckbox__clean_copy():
    """
    Tests whether ``ComponentMetadataCheckbox.clean_copy`` works as intended.
    """
    guild_id = 202505030030
    guild = Guild.precreate(guild_id)
    
    custom_id = 'oriental'
    default = True
    
    component_metadata = ComponentMetadataCheckbox(
        custom_id = custom_id,
        default = default,
    )
    copy = component_metadata.clean_copy(guild)
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, component_metadata)
    vampytest.assert_eq(copy, component_metadata)


def test__ComponentMetadataCheckbox__copy():
    """
    Tests whether ``ComponentMetadataCheckbox.copy`` works as intended.
    """
    custom_id = 'oriental'
    default = True
    
    component_metadata = ComponentMetadataCheckbox(
        custom_id = custom_id,
        default = default,
    )
    copy = component_metadata.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, component_metadata)
    vampytest.assert_eq(copy, component_metadata)


def test__ComponentMetadataCheckbox__copy_with__no_fields():
    """
    Tests whether ``ComponentMetadataCheckbox.copy_with`` works as intended.
    
    Case: No fields.
    """
    custom_id = 'oriental'
    default = True
    
    component_metadata = ComponentMetadataCheckbox(
        custom_id = custom_id,
        default = default,
    )
    copy = component_metadata.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, component_metadata)
    vampytest.assert_eq(copy, component_metadata)


def test__ComponentMetadataCheckbox__copy_with__all_fields():
    """
    Tests whether ``ComponentMetadataCheckbox.copy_with`` works as intended.
    
    Case: All fields.
    """
    old_custom_id = 'oriental'
    old_default = True
    
    new_custom_id = 'uta'
    new_default = False
    
    component_metadata = ComponentMetadataCheckbox(
        custom_id = old_custom_id,
        default = old_default,
    )
    copy = component_metadata.copy_with(
        custom_id = new_custom_id,
        default = new_default,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy.custom_id, new_custom_id)
    vampytest.assert_eq(copy.default, new_default)


def test__ComponentMetadataCheckbox__copy_with_keyword_parameters__no_fields():
    """
    Tests whether ``ComponentMetadataCheckbox.copy_with_keyword_parameters`` works as intended.
    
    Case: No fields.
    """
    custom_id = 'oriental'
    default = True
    
    component_metadata = ComponentMetadataCheckbox(
        custom_id = custom_id,
        default = default,
    )
    copy = component_metadata.copy_with_keyword_parameters({})
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, component_metadata)
    vampytest.assert_eq(copy, component_metadata)


def test__ComponentMetadataCheckbox__copy_with_keyword_parameters__all_fields():
    """
    Tests whether ``ComponentMetadataCheckbox.copy_with_keyword_parameters`` works as intended.
    
    Case: All fields.
    """
    old_custom_id = 'oriental'
    old_default = True
    
    new_custom_id = 'uta'
    new_default = False
    
    component_metadata = ComponentMetadataCheckbox(
        custom_id = old_custom_id,
        default = old_default,
    )
    copy = component_metadata.copy_with_keyword_parameters({
        'custom_id': new_custom_id,
        'default': new_default,
    })
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy.custom_id, new_custom_id)
    vampytest.assert_eq(copy.default, new_default)


def _iter_options__iter_contents():
    custom_id = 'oriental'
    default = True
    
    yield (
        {},
        [],
    )
    
    yield (
        {
            'custom_id': custom_id,
            'default': default,
        },
        [],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_contents()).returning_last())
def test__ComponentMetadataCheckbox__iter_contents(keyword_parameters):
    """
    Tests whether ``ComponentMetadataCheckbox.iter_contents`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `list<str>`
    """
    component_metadata = ComponentMetadataCheckbox(**keyword_parameters)
    output = [*component_metadata.iter_contents()]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return output
