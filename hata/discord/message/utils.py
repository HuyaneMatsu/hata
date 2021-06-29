__all__ = ()

from ..core import INTERACTION_EVENT_RESPONSE_WAITERS, INTERACTION_EVENT_MESSAGE_WAITERS

def try_resolve_interaction_message(message, interaction):
    """
    Tries to resolve an interaction's message if not yet resolved.
    
    Parameters
    ----------
    message : ``Message``
        Received message.
    interaction : ``MessageInteraction`` or ``InteractionEvent``
        Received message interaction.
    """
    try:
        interaction_event = INTERACTION_EVENT_RESPONSE_WAITERS.pop(interaction.id)
    except KeyError:
        pass
    else:
        interaction_event.message = message
        
        try:
            waiter = INTERACTION_EVENT_MESSAGE_WAITERS[interaction_event]
        except KeyError:
            pass
        else:
            waiter.set_result_if_pending(None)
