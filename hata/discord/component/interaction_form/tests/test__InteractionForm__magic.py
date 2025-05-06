import vampytest

from ...component import Component, ComponentType

from ..interaction_form import InteractionForm


def test__InteractionForm__repr():
    """
    Test whether ``InteractionForm.__repr__`` works as intended.
    """
    title = 'important'
    components = [Component(ComponentType.text_input, label = 'chata')]
    custom_id = 'lie'
    
    interaction_form = InteractionForm(title, components, custom_id)
    vampytest.assert_instance(repr(interaction_form), str)


def test__InteractionForm__hash():
    """
    Test whether ``InteractionForm.__hash__`` works as intended.
    """
    title = 'important'
    components = [Component(ComponentType.text_input, label = 'chata')]
    custom_id = 'lie'
    
    interaction_form = InteractionForm(title, components, custom_id)
    vampytest.assert_instance(hash(interaction_form), int)


def _iter_options__eq():
    title = 'important'
    components = [Component(ComponentType.text_input, label = 'chata')]
    custom_id = 'lie'
    
    keyword_parameters = {
        'title': title,
        'components': components,
        'custom_id': custom_id,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'title': 'fire',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'components': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'custom_id': 'heart',
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__InteractionForm__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``InteractionForm.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    interaction_form_0 = InteractionForm(**keyword_parameters_0)
    interaction_form_1 = InteractionForm(**keyword_parameters_1)
    
    output = interaction_form_0 == interaction_form_1
    vampytest.assert_instance(output, bool)
    return output
