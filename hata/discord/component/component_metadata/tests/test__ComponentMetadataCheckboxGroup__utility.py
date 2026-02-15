import vampytest

from ....guild import Guild

from ...checkbox_group_option import CheckboxGroupOption

from ..checkbox_group import ComponentMetadataCheckboxGroup

from .test__ComponentMetadataCheckboxGroup__constructor import _assert_fields_set


def test__ComponentMetadataCheckboxGroup__clean_copy():
    """
    Tests whether ``ComponentMetadataCheckboxGroup.clean_copy`` works as intended.
    """
    guild_id = 202505030030
    guild = Guild.precreate(guild_id)
    
    custom_id = 'oriental'
    max_values = 10
    min_values = 9
    options = [CheckboxGroupOption('yume')]
    required = True
    
    component_metadata = ComponentMetadataCheckboxGroup(
        custom_id = custom_id,
        max_values = max_values,
        min_values = min_values,
        options = options,
        required = required,
    )
    copy = component_metadata.clean_copy(guild)
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, component_metadata)
    vampytest.assert_eq(copy, component_metadata)


def test__ComponentMetadataCheckboxGroup__copy():
    """
    Tests whether ``ComponentMetadataCheckboxGroup.copy`` works as intended.
    """
    custom_id = 'oriental'
    max_values = 10
    min_values = 9
    options = [CheckboxGroupOption('yume')]
    required = True
    
    component_metadata = ComponentMetadataCheckboxGroup(
        custom_id = custom_id,
        max_values = max_values,
        min_values = min_values,
        options = options,
        required = required,
    )
    copy = component_metadata.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, component_metadata)
    vampytest.assert_eq(copy, component_metadata)


def test__ComponentMetadataCheckboxGroup__copy_with__no_fields():
    """
    Tests whether ``ComponentMetadataCheckboxGroup.copy_with`` works as intended.
    
    Case: No fields.
    """
    custom_id = 'oriental'
    max_values = 10
    min_values = 9
    options = [CheckboxGroupOption('yume')]
    required = True
    
    component_metadata = ComponentMetadataCheckboxGroup(
        custom_id = custom_id,
        max_values = max_values,
        min_values = min_values,
        options = options,
        required = required,
    )
    copy = component_metadata.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, component_metadata)
    vampytest.assert_eq(copy, component_metadata)


def test__ComponentMetadataCheckboxGroup__copy_with__all_fields():
    """
    Tests whether ``ComponentMetadataCheckboxGroup.copy_with`` works as intended.
    
    Case: All fields.
    """
    old_custom_id = 'oriental'
    old_max_values = 10
    old_min_values = 9
    old_options = [CheckboxGroupOption('yume')]
    old_required = True
    
    new_custom_id = 'uta'
    new_max_values = 11
    new_min_values = 8
    new_options = [CheckboxGroupOption('shinjite'), CheckboxGroupOption('boku')]
    new_required = False
    
    component_metadata = ComponentMetadataCheckboxGroup(
        custom_id = old_custom_id,
        max_values = old_max_values,
        min_values = old_min_values,
        options = old_options,
        required = old_required,
    )
    copy = component_metadata.copy_with(
        custom_id = new_custom_id,
        max_values = new_max_values,
        min_values = new_min_values,
        options = new_options,
        required = new_required,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy.custom_id, new_custom_id)
    vampytest.assert_eq(copy.max_values, new_max_values)
    vampytest.assert_eq(copy.min_values, new_min_values)
    vampytest.assert_eq(copy.options, tuple(new_options))
    vampytest.assert_eq(copy.required, new_required)


def test__ComponentMetadataCheckboxGroup__copy_with_keyword_parameters__no_fields():
    """
    Tests whether ``ComponentMetadataCheckboxGroup.copy_with_keyword_parameters`` works as intended.
    
    Case: No fields.
    """
    custom_id = 'oriental'
    max_values = 10
    min_values = 9
    options = [CheckboxGroupOption('yume')]
    required = True
    
    component_metadata = ComponentMetadataCheckboxGroup(
        custom_id = custom_id,
        max_values = max_values,
        min_values = min_values,
        options = options,
        required = required,
    )
    copy = component_metadata.copy_with_keyword_parameters({})
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, component_metadata)
    vampytest.assert_eq(copy, component_metadata)


def test__ComponentMetadataCheckboxGroup__copy_with_keyword_parameters__all_fields():
    """
    Tests whether ``ComponentMetadataCheckboxGroup.copy_with_keyword_parameters`` works as intended.
    
    Case: All fields.
    """
    old_custom_id = 'oriental'
    old_max_values = 10
    old_min_values = 9
    old_options = [CheckboxGroupOption('yume')]
    old_required = True
    
    new_custom_id = 'uta'
    new_max_values = 11
    new_min_values = 8
    new_options = [CheckboxGroupOption('shinjite'), CheckboxGroupOption('boku')]
    new_required = False
    
    component_metadata = ComponentMetadataCheckboxGroup(
        custom_id = old_custom_id,
        max_values = old_max_values,
        min_values = old_min_values,
        options = old_options,
        required = old_required,
    )
    copy = component_metadata.copy_with_keyword_parameters({
        'custom_id': new_custom_id,
        'max_values': new_max_values,
        'min_values': new_min_values,
        'options': new_options,
        'required': new_required,
    })
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy.custom_id, new_custom_id)
    vampytest.assert_eq(copy.max_values, new_max_values)
    vampytest.assert_eq(copy.min_values, new_min_values)
    vampytest.assert_eq(copy.options, tuple(new_options))
    vampytest.assert_eq(copy.required, new_required)


def _iter_options__iter_contents():
    custom_id = 'oriental'
    max_values = 10
    min_values = 9
    options = [CheckboxGroupOption('yume')]
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
            'options': options,
            'required': required,
        },
        [],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_contents()).returning_last())
def test__ComponentMetadataCheckboxGroup__iter_contents(keyword_parameters):
    """
    Tests whether ``ComponentMetadataCheckboxGroup.iter_contents`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `list<str>`
    """
    component_metadata = ComponentMetadataCheckboxGroup(**keyword_parameters)
    output = [*component_metadata.iter_contents()]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return output
