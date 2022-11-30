__all__ = ()

from scarletio import include

from ..core import INTERACTION_EVENT_MESSAGE_WAITERS, INTERACTION_EVENT_RESPONSE_WAITERS


Message = include('Message')

def try_resolve_interaction_message(message, interaction):
    """
    Tries to resolve an interaction's message if not yet resolved.
    
    Parameters
    ----------
    message : ``Message``
        Received message.
    interaction : ``MessageInteraction``, ``InteractionEvent``
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


def process_message_chunk(message_datas, channel):
    """
    Called with the response data after requesting older messages of a channel. It checks whether we can chain
    the messages to the channel's history. If we can it chains them and removes the length limitation too if
    needed.
    
    Parameters
    ----------
    message_datas : `list` of (`dict` of (`str`, `Any`) items) elements
        A list of message's data received from Discord.
    channel : ``Channel``, `None`
        The channels to which the messages are bound to if any.
    
    Returns
    -------
    received : `list` of ``Message`` objects
    """
    received = []
    index = 0
    limit = len(message_datas)
    
    if index != limit:
        if channel is None:
            for message_data in message_datas:
                message = Message.from_data(message_data)
                received.append(message)
        else:
            message_data = message_datas[index]
            index += 1
            message, exists = channel._create_find_message(message_data, False)
            received.append(message)
            
            if exists:
                while True:
                    if index == limit:
                        break
                    
                    message_data = message_datas[index]
                    index += 1
                    message, exists = channel._create_find_message(message_data, True)
                    received.append(message)
                    
                    if exists:
                        continue
                    
                    while True:
                        if index == limit:
                            break
                        
                        message_data = message_datas[index]
                        index += 1
                        message = channel._create_old_message(message_data)
                        received.append(message)
                        continue
                    
                    break
            else:
                while True:
                    if index == limit:
                        break
                    
                    message_data = message_datas[index]
                    index += 1
                    message = Message.from_data(message_data)
                    received.append(message)
                    continue
    
    return received

