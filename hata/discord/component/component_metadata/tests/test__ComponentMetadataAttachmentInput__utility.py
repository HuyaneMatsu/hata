import vampytest

from ....guild import Guild

from ..attachment_input import ComponentMetadataAttachmentInput

from .test__ComponentMetadataAttachmentInput__constructor import _assert_fields_set


def test__ComponentMetadataAttachmentInput__clean_copy():
    """
    Tests whether ``ComponentMetadataAttachmentInput.clean_copy`` works as intended.
    """
    guild_id = 202505030028
    guild = Guild.precreate(guild_id)
    
    custom_id = 'oriental'
    max_values = 10
    min_values = 9
    required = True
    
    component_metadata = ComponentMetadataAttachmentInput(
        custom_id = custom_id,
        max_values = max_values,
        min_values = min_values,
        required = required,
    )
    copy = component_metadata.clean_copy(guild)
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, component_metadata)
    vampytest.assert_eq(copy, component_metadata)


def test__ComponentMetadataAttachmentInput__copy():
    """
    Tests whether ``ComponentMetadataAttachmentInput.copy`` works as intended.
    """
    custom_id = 'oriental'
    max_values = 10
    min_values = 9
    required = True
    
    component_metadata = ComponentMetadataAttachmentInput(
        custom_id = custom_id,
        max_values = max_values,
        min_values = min_values,
        required = required,
    )
    copy = component_metadata.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, component_metadata)
    vampytest.assert_eq(copy, component_metadata)


def test__ComponentMetadataAttachmentInput__copy_with__no_fields():
    """
    Tests whether ``ComponentMetadataAttachmentInput.copy_with`` works as intended.
    
    Case: No fields.
    """
    custom_id = 'oriental'
    max_values = 10
    min_values = 9
    required = True
    
    component_metadata = ComponentMetadataAttachmentInput(
        custom_id = custom_id,
        max_values = max_values,
        min_values = min_values,
        required = required,
    )
    copy = component_metadata.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, component_metadata)
    vampytest.assert_eq(copy, component_metadata)


def test__ComponentMetadataAttachmentInput__copy_with__1():
    """
    Tests whether ``ComponentMetadataAttachmentInput.copy_with`` works as intended.
    
    Case: All fields.
    """
    old_custom_id = 'oriental'
    old_max_values = 10
    old_min_values = 9
    old_required = True
    
    new_custom_id = 'uta'
    new_max_values = 11
    new_min_values = 8
    new_required = False
    
    component_metadata = ComponentMetadataAttachmentInput(
        custom_id = old_custom_id,
        max_values = old_max_values,
        min_values = old_min_values,
        required = old_required,
    )
    copy = component_metadata.copy_with(
        custom_id = new_custom_id,
        max_values = new_max_values,
        min_values = new_min_values,
        required = new_required,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, component_metadata)
    vampytest.assert_eq(copy.custom_id, new_custom_id)
    vampytest.assert_eq(copy.max_values, new_max_values)
    vampytest.assert_eq(copy.min_values, new_min_values)
    vampytest.assert_eq(copy.required, new_required)


def test__ComponentMetadataAttachmentInput__copy_with_keyword_parameters__no_fields():
    """
    Tests whether ``ComponentMetadataAttachmentInput.copy_with_keyword_parameters`` works as intended.
    
    Case: No fields.
    """
    custom_id = 'oriental'
    max_values = 10
    min_values = 9
    required = True
    
    component_metadata = ComponentMetadataAttachmentInput(
        custom_id = custom_id,
        max_values = max_values,
        min_values = min_values,
        required = required,
    )
    copy = component_metadata.copy_with_keyword_parameters({})
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, component_metadata)
    vampytest.assert_eq(copy, component_metadata)


def test__ComponentMetadataAttachmentInput__copy_with_keyword_parameters__all_fields():
    """
    Tests whether ``ComponentMetadataAttachmentInput.copy_with_keyword_parameters`` works as intended.
    
    Case: All fields.
    """
    old_custom_id = 'oriental'
    old_max_values = 10
    old_min_values = 9
    old_required = True
    
    new_custom_id = 'uta'
    new_max_values = 11
    new_min_values = 8
    new_required = False
    
    component_metadata = ComponentMetadataAttachmentInput(
        custom_id = old_custom_id,
        max_values = old_max_values,
        min_values = old_min_values,
        required = old_required,
    )
    copy = component_metadata.copy_with_keyword_parameters({
        'custom_id': new_custom_id,
        'max_values': new_max_values,
        'min_values': new_min_values,
        'required': new_required,
    })
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, component_metadata)
    vampytest.assert_eq(copy.custom_id, new_custom_id)
    vampytest.assert_eq(copy.max_values, new_max_values)
    vampytest.assert_eq(copy.min_values, new_min_values)
    vampytest.assert_eq(copy.required, new_required)


def _iter_options__iter_contents():
    custom_id = 'oriental'
    max_values = 10
    min_values = 9
    required = True
    
    yield (
        {},
        [],
    )
    
    yield (
        {
            'custom_id': custom_id,
            'max_values': max_values,
            'min_values': min_values,
            'required': required,
        },
        [],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_contents()).returning_last())
def test__ComponentMetadataAttachmentInput__iter_contents(keyword_parameters):
    """
    Tests whether ``ComponentMetadataAttachmentInput.iter_contents`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `list<str>`
    """
    component_metadata = ComponentMetadataAttachmentInput(**keyword_parameters)
    output = [*component_metadata.iter_contents()]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return output
