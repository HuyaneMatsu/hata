import vampytest

from ...message_interaction import MessageInteraction

from ..fields import parse_interaction


def _iter_options():
    interaction_id = 202304300003
    interaction = MessageInteraction.precreate(interaction_id, name = 'orin')
    
    yield {}, None
    yield {'interaction_metadata': None}, None
    yield {'interaction_metadata': interaction.to_data(include_internals = True)}, interaction
    yield {'interaction': None}, None
    yield {'interaction': interaction.to_data(include_internals = True)}, interaction


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_interaction(input_data):
    """
    Tests whether ``parse_interaction`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    interaction : `None | MessageInteraction`
    """
    return parse_interaction(input_data)
