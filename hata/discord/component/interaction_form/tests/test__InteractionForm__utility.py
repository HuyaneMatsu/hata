import vampytest

from ...component import Component, ComponentType

from ..interaction_form import InteractionForm

from .test__InteractionForm__constructor import _check_are_fields_set


def test__InteractionForm__copy():
    """
    Test whether ``InteractionForm.copy`` works as intended.
    """
    title = 'important'
    components = [Component(ComponentType.text_input, label = 'chata')]
    custom_id = 'lie'
    
    rows = tuple(Component(ComponentType.row, components = [component]) for component in components)
    
    interaction_form = InteractionForm(title, components, custom_id)
    copy = interaction_form.copy()
    
    _check_are_fields_set(copy)
    vampytest.assert_is_not(interaction_form, copy)
    vampytest.assert_eq(copy.title, title)
    vampytest.assert_eq(copy.components, rows)
    vampytest.assert_eq(copy.custom_id, custom_id)


def test__InteractionForm__copy_with__no_fields():
    """
    Test whether ``InteractionForm.copy_with`` works as intended.
    
    Case: no fields given.
    """
    title = 'important'
    components = [Component(ComponentType.text_input, label = 'chata')]
    custom_id = 'lie'
    
    rows = tuple(Component(ComponentType.row, components = [component]) for component in components)
    
    interaction_form = InteractionForm(title, components, custom_id)
    copy = interaction_form.copy_with()
    
    _check_are_fields_set(copy)
    vampytest.assert_is_not(interaction_form, copy)
    vampytest.assert_eq(copy.title, title)
    vampytest.assert_eq(copy.components, rows)
    vampytest.assert_eq(copy.custom_id, custom_id)


def test__InteractionForm__copy_with__all_fields():
    """
    Test whether ``InteractionForm.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_title = 'important'
    old_components = [Component(ComponentType.text_input, label = 'chata')]
    old_custom_id = 'lie'
    
    new_title = 'fire'
    new_components = [Component(ComponentType.text_input, label = 'in my')]
    new_custom_id = 'heart'
    
    rows = tuple(Component(ComponentType.row, components = [component]) for component in new_components)
    
    interaction_form = InteractionForm(old_title, old_components, old_custom_id)
    copy = interaction_form.copy_with(title = new_title, components = new_components, custom_id = new_custom_id)
    
    _check_are_fields_set(copy)
    vampytest.assert_is_not(interaction_form, copy)
    vampytest.assert_eq(copy.title, new_title)
    vampytest.assert_eq(copy.components, rows)
    vampytest.assert_eq(copy.custom_id, new_custom_id)


def _iter_options__iter_components():
    component_0 = Component(ComponentType.row, components = [Component(ComponentType.text_input, label = 'chata')])
    component_1 = Component(ComponentType.row, components = [Component(ComponentType.text_input, label = 'izna')])
    
    yield None, []
    yield [component_0], [component_0]
    yield [component_0, component_1], [component_0, component_1]


@vampytest._(vampytest.call_from(_iter_options__iter_components()).returning_last())
def test__InteractionForm__iter_components(input_value):
    """
    Tests whether ``InteractionForm.iter_components`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<Component>`
        Value to create the form with.
    
    Returns
    -------
    output : `list<Component>`
    """
    interaction_form = InteractionForm(None, input_value)
    return [*interaction_form.iter_components()]
