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


def test__InteractionForm__new__0():
    """
    Test whether ``InteractionForm.__new__`` works as intended.
    
    Case: empty.
    """
    title = None
    components = None
    custom_id = None
    
    interaction_form = InteractionForm(title, components, custom_id)
    _check_are_fields_set(interaction_form)


def test__InteractionForm__new__1():
    """
    Test whether ``InteractionForm.__new__`` works as intended.
    
    Case: Stuff it full.
    """
    title = 'important'
    components = [Component(ComponentType.button, label = 'chata')]
    custom_id = 'lie'
    
    rows = tuple(Component(ComponentType.row, components = [component]) for component in components)
    
    interaction_form = InteractionForm(title, components, custom_id)
    _check_are_fields_set(interaction_form)
    
    vampytest.assert_eq(interaction_form.title, title)
    vampytest.assert_eq(interaction_form.components, rows)
    vampytest.assert_eq(interaction_form.custom_id, custom_id)
