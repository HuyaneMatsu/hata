import vampytest

from ....guild import Guild

from ...component import Component, ComponentType

from ..label import ComponentMetadataLabel

from .test__ComponentMetadataLabel__constructor import _assert_fields_set


def test__ComponentMetadataLabel__clean_copy():
    """
    Tests whether ``ComponentMetadataLabel.clean_copy`` works as intended.
    """
    guild_id = 202505030032
    guild = Guild.precreate(guild_id)
    
    sub_component = Component(ComponentType.text_input, placeholder = 'chata')
    description = 'Makai route'
    label = 'Sariel'
    
    component_metadata = ComponentMetadataLabel(
        component = sub_component,
        description = description,
        label = label,
    )
    copy = component_metadata.clean_copy(guild)
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, component_metadata)
    vampytest.assert_eq(copy, component_metadata)


def test__ComponentMetadataLabel__copy():
    """
    Tests whether ``ComponentMetadataLabel.copy`` works as intended.
    """
    sub_component = Component(ComponentType.text_input, placeholder = 'chata')
    description = 'Makai route'
    label = 'Sariel'
    
    component_metadata = ComponentMetadataLabel(
        component = sub_component,
        description = description,
        label = label,
    )
    copy = component_metadata.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy, component_metadata)
    

def test__ComponentMetadataLabel__copy_with__no_fields():
    """
    Tests whether ``ComponentMetadataLabel.copy_with`` works as intended.
    
    Case: No fields given.
    """
    sub_component = Component(ComponentType.text_input, placeholder = 'chata')
    description = 'Makai route'
    label = 'Sariel'
    
    component_metadata = ComponentMetadataLabel(
        component = sub_component,
        description = description,
        label = label,
    )
    copy = component_metadata.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy, component_metadata)


def test__ComponentMetadataLabel__copy_with__all_fields():
    """
    Tests whether ``ComponentMetadataLabel.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_sub_component = Component(ComponentType.text_input, placeholder = 'chata')
    old_description = 'Makai route'
    old_label = 'Sariel'
    
    new_sub_component = Component(ComponentType.text_input, placeholder = 'chata')
    new_description = 'Jiguku route'
    new_label = 'Konngara'
    
    component_metadata = ComponentMetadataLabel(
        component = old_sub_component,
        description = old_description,
        label = old_label,
    )
    copy = component_metadata.copy_with(
        component = new_sub_component,
        description = new_description,
        label = new_label,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_ne(copy, component_metadata)
    
    vampytest.assert_eq(copy.component, new_sub_component)
    vampytest.assert_eq(copy.description, new_description)
    vampytest.assert_eq(copy.label, new_label)


def test__ComponentMetadataLabel__copy_with_keyword_parameters__no_fields():
    """
    Tests whether ``ComponentMetadataLabel.copy_with_keyword_parameters`` works as intended.
    
    Case: No fields given.
    """
    sub_component = Component(ComponentType.text_input, placeholder = 'chata')
    description = 'Makai route'
    label = 'Sariel'
    
    component_metadata = ComponentMetadataLabel(
        component = sub_component,
        description = description,
        label = label,
    )
    copy = component_metadata.copy_with_keyword_parameters({})
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_eq(copy, component_metadata)


def test__ComponentMetadataLabel__copy_with_keyword_parameters__all_fields():
    """
    Tests whether ``ComponentMetadataLabel.copy_with_keyword_parameters`` works as intended.
    
    Case: All fields given.
    """
    old_sub_component = Component(ComponentType.text_input, placeholder = 'chata')
    old_description = 'Makai route'
    old_label = 'Sariel'
    
    new_sub_component = Component(ComponentType.text_input, placeholder = 'important')
    new_description = 'Jiguku route'
    new_label = 'Konngara'
    
    component_metadata = ComponentMetadataLabel(
        component = old_sub_component,
        description = old_description,
        label = old_label,
    )
    copy = component_metadata.copy_with_keyword_parameters({
        'component': new_sub_component,
        'description': new_description,
        'label': new_label,
    })
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(component_metadata, copy)
    vampytest.assert_ne(copy, component_metadata)
    
    vampytest.assert_eq(copy.component, new_sub_component)
    vampytest.assert_eq(copy.description, new_description)
    vampytest.assert_eq(copy.label, new_label)


def _iter_options__iter_contents():
    sub_component = Component(ComponentType.text_input, placeholder = 'chata')
    description = 'Makai route'
    label = 'Sariel'
    
    yield (
        {},
        [],
    )
    
    yield (
        {
            'component': sub_component,
            'description': description,
            'label': label,
        },
        [],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_contents()).returning_last())
def test__ComponentMetadataLabel__iter_contents(keyword_parameters):
    """
    Tests whether ``ComponentMetadataLabel.iter_contents`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `list<str>`
    """
    component_metadata = ComponentMetadataLabel(**keyword_parameters)
    output = [*component_metadata.iter_contents()]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return output
