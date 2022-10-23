import vampytest

from ...component import Component, ComponentType

from ..interaction_form import InteractionForm


def test__InteractionForm__repr():
    """
    Test whether ``InteractionForm.__repr__`` works as intended.
    """
    title = 'important'
    components = [Component(ComponentType.button, label = 'chata')]
    custom_id = 'lie'
    
    interaction_form = InteractionForm(title, components, custom_id)
    vampytest.assert_instance(repr(interaction_form), str)


def test__InteractionForm__hash():
    """
    Test whether ``InteractionForm.__hash__`` works as intended.
    """
    title = 'important'
    components = [Component(ComponentType.button, label = 'chata')]
    custom_id = 'lie'
    
    interaction_form = InteractionForm(title, components, custom_id)
    vampytest.assert_instance(hash(interaction_form), int)


def test__InteractionForm__eq():
    """
    Test whether ``InteractionForm.__hash__`` works as intended.
    """
    title = 'important'
    components = [Component(ComponentType.button, label = 'chata')]
    custom_id = 'lie'
    
    keyword_parameters = {
        'title': title,
        'components': components,
        'custom_id': custom_id,
    }
    
    interaction_form = InteractionForm(**keyword_parameters)
    vampytest.assert_eq(interaction_form, interaction_form)
    vampytest.assert_ne(interaction_form, object())
    
    for field_name, field_value in (
        ('title', 'fire'),
        ('components', None),
        ('custom_id', 'heart'),
    ):
        test_interaction_form = InteractionForm(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(interaction_form, test_interaction_form)
