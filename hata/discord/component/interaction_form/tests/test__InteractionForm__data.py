import vampytest

from ...component import Component, ComponentType

from ..interaction_form import InteractionForm

from .test__InteractionForm__constructor import _check_are_fields_set



def test__InteractionForm__from_data():
    """
    Test whether ``InteractionForm.from_data`` works as intended.
    """
    title = 'important'
    components = [Component(ComponentType.text_input, label = 'chata')]
    custom_id = 'lie'
    
    rows = tuple(Component(ComponentType.row, components = [component]) for component in components)
    
    
    data = {
        'title': title,
        'components': [row.to_data() for row in rows],
        'custom_id': custom_id
    }
    
    interaction_form = InteractionForm.from_data(data)
    _check_are_fields_set(interaction_form)
    
    vampytest.assert_eq(interaction_form.title, title)
    vampytest.assert_eq(interaction_form.components, rows)
    vampytest.assert_eq(interaction_form.custom_id, custom_id)


def test__InteractionForm__to_data():
    """
    Test whether ``InteractionForm.to_data`` works as intended.
    
    Case: include defaults.
    """
    title = 'important'
    components = [Component(ComponentType.text_input, label = 'chata')]
    custom_id = 'lie'
    
    rows = tuple(Component(ComponentType.row, components = [component]) for component in components)
    
    
    interaction_form = InteractionForm(title, components, custom_id)
    
    vampytest.assert_eq(
        interaction_form.to_data(
            defaults = True,
        ),
        {
            'title': title,
            'components': [row.to_data(defaults = True) for row in rows],
            'custom_id': custom_id
        },
    )
