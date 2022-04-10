__all__ = ()

from scarletio import KeepType

from ...discord.client.utils import ClientWrapper
from ...discord.events.handling_helpers import _EventHandlerManagerRouter

from .command import Command
from .command_processor import CommandProcessor


def commands_getter(manager_router):
    """
    Gets the command processor using `Client.command_processor` of an ``_EventHandlerManagerRouter``.
    
    Parameters
    ----------
    manager_router : ``_EventHandlerManagerRouter``
        The caller manager router.
    
    Returns
    -------
    handlers : `list` of ``CommandProcessor``
    """
    handlers = []
    for client in manager_router.parent.clients:
        manager = getattr(client, 'commands', None)
        if manager is None:
            continue
        
        handler = manager.parent
        if isinstance(handler, CommandProcessor):
            handlers.append(handler)
    
    return handlers


def from_class_constructor(klass):
    """
    Creates a command from the given class.
    
    Parameters
    ----------
    klass : `type`
        The class to create a slash command from.
    
    Returns
    -------
    self : ``Command``, ``Router``
    
    Raises
    ------
    BaseException
        Any exception raised by the respective ``Command`` constructor.
    """
    return Command.from_class(klass)


@KeepType(ClientWrapper)
class ClientWrapper:
    
    @property
    def commands(self):
        """
        Returns a ``_EventHandlerManagerRouter``, with what commands can be added to more clients at the
        same time.
        
        Returns
        -------
        event_handler_manager_router : ``_EventHandlerManagerRouter``
        """
        return _EventHandlerManagerRouter(self, commands_getter, from_class_constructor)
