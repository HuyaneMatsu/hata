__all__ = ()

from functools import partial as partial_func

from ....discord.message import Message
from ....discord.interaction import InteractionEvent, create_auto_custom_id
from ....discord.core import BUILTIN_EMOJIS

EMOJI_LEFT_2 = BUILTIN_EMOJIS['track_previous']
EMOJI_LEFT = BUILTIN_EMOJIS['arrow_backward']
EMOJI_RIGHT = BUILTIN_EMOJIS['arrow_forward']
EMOJI_RIGHT_2 = BUILTIN_EMOJIS['track_next']
EMOJI_CANCEL = BUILTIN_EMOJIS['x']


CUSTOM_ID_CANCEL = create_auto_custom_id()

def default_check(user, event):
    """
    Default check returned by ``get_auto_check`` wrapped into a partial function.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user who received the source event.
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    should_process : `bool`
        Whether the menu should process the received interaction.
    """
    if (event.user is user):
        return True
    
    if event.user_permissions.can_manage_messages and (event.interaction.custom_id == CUSTOM_ID_CANCEL):
        return True
    
    return False


def get_auto_check(event):
    """
    If check is not given by the user, tries to auto create one.
    
    Parameters
    ----------
    event : ``InteractionEvent``, ``Message``, `Any`
        Event passed to the constructor.
    
    Returns
    -------
    check : `None` or `functools.partial`
    """
    if isinstance(event, InteractionEvent):
        user = event.user
    elif isinstance(event, Message):
        interaction = event.interaction
        if interaction is None:
            user = None
        else:
            user = interaction.user
    else:
        user = None
    
    if user is None:
        check = None
    else:
        check = partial_func(default_check, event.user)
    
    return check


def top_level_check(self, event):
    """
    Top level check for menus with `.user_check` attribute.
    
    Parameters
    ----------
    self : ``Menu``
        The respective menu instance.
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    should_process : `bool`
        Whether the menu should process the received interaction.
    """
    check = self.user_check
    if check is None:
        should_process = True
    else:
        should_process = check(event)
    
    return should_process


def top_level_get_timeout(self):
    """
    Top level function for menus with `.timeout` attribute.
    
    Attributes
    ----------
    self : `Menu``
        The respective menu instance.
    
    Returns
    -------
    timeout : `float`
    """
    return self.timeout
