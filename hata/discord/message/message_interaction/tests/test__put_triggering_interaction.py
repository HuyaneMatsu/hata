import vampytest

from ...message_interaction import MessageInteraction

from ..fields import put_triggering_interaction


def _iter_options():
    interaction_id = 202403260001
    interaction = MessageInteraction.precreate(interaction_id, name = 'Orin')
    
    yield None, False, False, {}
    yield None, False, True, {}
    yield None, True, False, {'triggering_interaction_metadata': None}
    yield None, True, True, {'triggering_interaction_metadata': None}
    yield interaction, False, False, {'triggering_interaction_metadata': interaction.to_data()}
    yield interaction, False, True, {'triggering_interaction_metadata': interaction.to_data(include_internals = True)}
    yield (
        interaction,
        True,
        False,
        {'triggering_interaction_metadata': interaction.to_data(defaults = True)},
    )
    yield (
        interaction,
        True,
        True,
        {'triggering_interaction_metadata': interaction.to_data(defaults = True, include_internals = True)},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_triggering_interaction(input_value, defaults, include_internals):
    """
    Tests whether ``put_triggering_interaction`` is working as intended.
    
    Parameters
    ----------
    input_value : `None | MessageInteraction`
        Interaction to serialize.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    include_internals : `bool`
        Whether internals should be included.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_triggering_interaction(input_value, {}, defaults, include_internals = include_internals)
