# -*- coding: utf-8 -*-
__all__ = ()

from ...backend.utils import KeepType

from ...discord.client_utils import ClientWrapper
from ...discord.parsers import _EventHandlerManagerRouter

from .command import Slasher, SlashCommand


def interactions_getter(manager_router):
    """
    Gets the slash command processer using `Client.slasher` of an ``_EventHandlerManagerRouter``.
    
    Parameters
    ----------
    manager_router : ``_EventHandlerManagerRouter``
        The caller manager router.
    
    Returns
    -------
    handlers : `list` of ``Slasher`` instances
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
        Returns a ``_EventHandlerManagerRouter`` instance, with what slash commands can be added to more clients at the
        same time.
        
        Returns
        -------
        event_handler_manager_router : ``_EventHandlerManagerRouter``
        """
        return _EventHandlerManagerRouter(self, interactions_getter, from_class_constructor)


del KeepType
