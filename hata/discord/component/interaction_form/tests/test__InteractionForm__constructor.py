import vampytest

from ...component import Component, ComponentType

from ..interaction_form import InteractionForm


def _check_are_fields_set(interaction_form):
    """
    Tests whether all attributes are set of the given form.
    
    Parameters
    ----------
    interaction_form : ``InteractionForm``
        The form to check.
    """
    vampytest.assert_instance(interaction_form, InteractionForm)
    vampytest.assert_instance(interaction_form.components, tuple, nullable = True)
    vampytest.assert_instance(interaction_form.custom_id, str, nullable = True)
    vampytest.assert_instance(interaction_form.title, str, nullable = True)


def test__InteractionForm__new__no_fields():
    """
    Test whether ``InteractionForm.__new__`` works as intended.
    
    Case: no fields given.
    """
    title = None
    components = None
    custom_id = None
    
    interaction_form = InteractionForm(title, components, custom_id)
    _check_are_fields_set(interaction_form)


def test__InteractionForm__new__all_fields():
    """
    Test whether ``InteractionForm.__new__`` works as intended.
    
    Case: all fields given.
    """
    title = 'important'
    components = [Component(ComponentType.text_input, placeholder = 'chata')]
    custom_id = 'lie'
    
    interaction_form = InteractionForm(title, components, custom_id)
    _check_are_fields_set(interaction_form)
    
    vampytest.assert_eq(interaction_form.title, title)
    vampytest.assert_eq(
        interaction_form.components,
        (*(Component(ComponentType.label, component = component) for component in components),),
    )
    vampytest.assert_eq(interaction_form.custom_id, custom_id)
