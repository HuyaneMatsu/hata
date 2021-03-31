# -*- coding: utf-8 -*-
__all__ = ()

from ...backend.utils import KeepType

from ...discord.client_utils import ClientWrapper
from ...discord.parsers import _EventHandlerManagerRouter

from .command import CommandProcesser, Command


def commands_getter(manager_router):
    """
    Gets the command processors using `Client.commands` of an ``_EventHandlerManagerRouter``.
    
    Parameters
    ----------
    manager_router : ``_EventHandlerManagerRouter``
        The caller manager router.
    
    Returns
    -------
    handlers : `list` of ``CommandProcesser`` instances
    """
    handlers = []
    for client in manager_router.parent.clients:
        manager = getattr(client, 'commands', None)
        if manager is None:
            continue
        
        handler = manager.parent
        if isinstance(handler, CommandProcesser):
            handlers.append(handler)
    
    return handlers


def from_class_constructor(klass):
    """
    Creates a command from the given class.
    
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
        Returns a ``_EventHandlerManagerRouter`` instance, with what commands can be added to more clients at the same
        time.
        
        Returns
        -------
        event_handler_manager_router : ``_EventHandlerManagerRouter``
        """
        return _EventHandlerManagerRouter(self, commands_getter, from_class_constructor)
