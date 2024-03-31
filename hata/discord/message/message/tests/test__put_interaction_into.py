import vampytest

from ...message_interaction import MessageInteraction

from ..fields import put_interaction_into


def _iter_options():
    interaction_id = 202304300004
    interaction = MessageInteraction.precreate(interaction_id, name = 'Orin')
    
    yield None, False, {}
    yield None, True, {'interaction_metadata': None}
    yield interaction, False, {'interaction_metadata': interaction.to_data(include_internals = True)}
    yield interaction, True, {'interaction_metadata': interaction.to_data(defaults = True, include_internals = True)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_interaction_into(input_value, defaults):
    """
    Tests whether ``put_interaction_into`` is working as intended.
    
    Parameters
    ----------
    input_value : `None | MessageInteraction`
        Interaction to serialize.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_interaction_into(input_value, {}, defaults)
