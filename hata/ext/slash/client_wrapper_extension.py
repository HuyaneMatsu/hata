__all__ = ()

from scarletio import KeepType

from ...discord.client.utils import ClientWrapper
from ...discord.events.handling_helpers import _EventHandlerManagerRouter

from .command import SlashCommand
from .slasher import Slasher


def interactions_getter(manager_router):
    """
    Gets the slash command processor using `Client.slasher` of an ``_EventHandlerManagerRouter``.
    
    Parameters
    ----------
    manager_router : ``_EventHandlerManagerRouter``
        The caller manager router.
    
    Returns
    -------
    handlers : `list` of ``Slasher``
    """
    handlers = []
    for client in manager_router.parent.clients:
        manager = getattr(client, 'interactions', None)
        if manager is None:
            continue
        
        handler = manager.parent
        if isinstance(handler, Slasher):
            handlers.append(handler)
    
    return handlers


def from_class_constructor(klass):
    """
    Creates a slash command from the given class.
    
    Parameters
    ----------
    klass : `type`
        The class to create a slash command from.
    
    Returns
    -------
    self : ``SlashCommand``, ``Router``
    
    Raises
    ------
    BaseException
        Any exception raised by the respective ``SlashCommand`` constructor.
    """
    return SlashCommand.from_class(klass)


@KeepType(ClientWrapper)
class ClientWrapper:
    
    @property
    def interactions(self):
        """
        Returns a ``_EventHandlerManagerRouter``, with what slash commands can be added to more clients at the
        same time.
        
        Returns
        -------
        event_handler_manager_router : ``_EventHandlerManagerRouter``
        """
        return _EventHandlerManagerRouter(self, interactions_getter, from_class_constructor)

