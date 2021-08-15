__all__ = ()

from ...discord.events.handling_helpers import asynclist, ChunkWaiter
from ...discord.events.core import EVENT_HANDLER_NAME_TO_PARSER_NAMES, DEFAULT_EVENT_HANDLER
from ...discord.core import CLIENTS
from ...discord.client.functionality_helpers import WaitForHandler

SNAPSHOT_TAKERS = {}

# Client.events snapshot functions

IGNORED_EVENT_HANDLER_TYPES = {
    WaitForHandler,
    ChunkWaiter,
}

def should_ignore_event_handler(event_handler):
    """
    Returns whether the given `event_handler` should be ignored from snapshotting.
    
    Parameters
    ----------
    event_handler : `async-callable`
        The respective event handler.
    
    Returns
    -------
    should_ignore : `bool`
    """
    if event_handler is DEFAULT_EVENT_HANDLER:
        return True
    
    if type(event_handler) in IGNORED_EVENT_HANDLER_TYPES:
        return True
    
    return False

EVENT_NAMES = tuple(EVENT_HANDLER_NAME_TO_PARSER_NAMES.keys())

def iterate_event_handler(event_handler):
    """
    Iterates over the given event handler, yielding each valuable handler.
    
    This method is an iterable generator.
    
    Parameters
    ----------
    event_handler : `Any`
        Event handler to iterate trough.
    
    Yields
    ------
    event_handler : `sync-callable`
        Valuable event handler-
    """
    if isinstance(event_handler, asynclist):
        for iterated_event_handler in list.__iter__(event_handler):
            if not should_ignore_event_handler(iterated_event_handler):
                yield iterated_event_handler
    else:
        if not should_ignore_event_handler(event_handler):
            yield event_handler


def take_event_handler_snapshot(client):
    """
    Collects the event handlers of the client.
    
    Parameters
    ----------
    client : ``Client``
        The client, who will be snapshotted.
    
    Returns
    -------
    collected : `dict` of (`str`, `list` of `async-callable`) items
        A multidict storing `event-name`, `event-handler` pairs.
    """
    collected = {}
    
    event_descriptor = client.events
    for event_name in EVENT_NAMES:
        for event_handler in iterate_event_handler(getattr(event_descriptor, event_name)):
            try:
                event_handlers = collected[event_name]
            except KeyError:
                event_handlers = []
                collected[event_name] = event_handlers
            
            event_handlers.append(event_handler)
    
    return collected


def calculate_event_handler_snapshot_difference(client, snapshot_old, snapshot_new):
    """
    Calculates the difference between two event handler snapshot returning the difference.
    
    Parameters
    ----------
    client : ``Client``
        The respective client instance.
    snapshot_old : `dict` of (`str`, `list` of `async-callable`) items
        An old snapshot taken.
    snapshot_new : `dict` of (`str`, `list` of `async-callable`) items
        A new snapshot.
    
    Returns
    -------
    snapshot_difference : `None` or `list` of `tuple` \
            (`str`, (`None` or `list` of `async-callable`), (`None` or `list` of `async-callable`))
        A list of event handler differences in a list of tuples.
        
        The tuple has 3 elements, where the 0th element is the name of the respective event, meanwhile the 1th element
        contains the removed event handlers and the 2th the added ones.
        
        If there is no difference between two snapshots, returns `None`.
    """
    snapshot_difference = []
    
    event_names = {*snapshot_old.keys(), *snapshot_new.keys()}
    
    for event_name in event_names:
        old_handlers = snapshot_old.get(event_name, None)
        new_handlers = snapshot_new.get(event_name, None)
        
        if (old_handlers is not None) and (new_handlers is not None):
            for index in reversed(range(len(old_handlers))):
                handler = old_handlers[index]
                try:
                    new_handlers.remove(handler)
                except ValueError:
                    pass
                else:
                    del old_handlers[index]
            
            if not new_handlers:
                new_handlers = None
            
            if not old_handlers:
                old_handlers = None
        
        if (old_handlers is not None) or (new_handlers is not None):
            snapshot_difference.append((event_name, old_handlers, new_handlers))
    
    if not snapshot_difference:
        snapshot_difference = None
    
    return snapshot_difference


def revert_event_handler_snapshot(client, snapshot_difference):
    """
    Reverts a taken snapshot.
    
    Parameters
    ----------
    client : ``Client``
        The respective client instance.
    snapshot_difference : `list` of `tuple` \
            (`str`, (`None` or `list` of `async-callable`), (`None` or `list` of `async-callable`))
        A list of event handler differences in a list of tuples.
        
        The tuple has 3 elements, where the 0th element is the name of the respective event, meanwhile the 1th element
        contains the removed event handlers and the 2th the added ones.
    """
    event_descriptor = client.events
    for event_handler_name, removed_handlers, added_handlers in snapshot_difference:
        if (added_handlers is not None):
            for handler in added_handlers:
                event_descriptor.remove(handler, name=event_handler_name, count=1)
            
        if (removed_handlers is not None):
            for handler in removed_handlers:
                event_descriptor(handler, name=event_handler_name)


# Register snapshot taker
SNAPSHOT_TAKERS['client.events'] = (
    take_event_handler_snapshot,
    calculate_event_handler_snapshot_difference,
    revert_event_handler_snapshot,
)


# General snapshot functions

def take_snapshot():
    """
    Takes a snapshot of the clients.
    
    Returns
    -------
    snapshot : `list` of `tuple` (``Client``, `list` of `tuple` (`str`, `Any`))
        A taken snapshot. Each element of the generated list contains a `client`, `client-snapshot` pair, where
        the `client-snapshot` is a list containing `snapshot-type-name`, `type-specific-snapshot` pairs.
    """
    snapshot = []
    for client in CLIENTS.values():
        client_snapshot = []
        snapshot.append((client, client_snapshot))
        
        for snapshot_type_name, (snapshot_taker, difference_calculator, reverter) in SNAPSHOT_TAKERS.items():
            sub_snapshot = snapshot_taker(client)
            
            client_snapshot.append((snapshot_type_name, sub_snapshot))
    
    return snapshot


def calculate_snapshot_difference(snapshot_old, snapshot_new):
    """
    Calculates snapshot differences between two snapshots.
    
    Parameters
    ----------
    snapshot_old : `list` of `tuple` (``Client``, `list` of `tuple` (`str`, `Any`))
        Old taken snapshot.
    snapshot_new : `list` of `tuple` (``Client``, `list` of `tuple` (`str`, `Any`))
        New taken snapshot.
    
    Returns
    -------
    snapshot_difference : `list` of `tuple` (``Client``, `list` of `tuple` (`str`, `Any`))
        The difference between two snapshots. Each element of the generated list contains a `client`,
        `client-snapshot-difference` pair, where the `client-snapshot-difference` is a dictionary containing
        `snapshot-type-name`, `type-specific-snapshot-difference` pairs.
    """
    # First check client difference. We will ignore clients which weren't present before or after.
    snapshot_clients_interception = set(e[0] for e in snapshot_old)&set(e[0] for e in snapshot_new)
    
    # Place snapshots next to each other depending on clients.
    parallel_snapshots = []
    for present_client in snapshot_clients_interception:
        for client, client_snapshot in snapshot_old:
            if present_client is client:
                client_snapshot_old = client_snapshot
                break
        
        for client, client_snapshot in snapshot_new:
            if present_client is client:
                client_snapshot_new = client_snapshot
                break
        
        parallel_snapshots.append((present_client, client_snapshot_old, client_snapshot_new))
    
    snapshot_difference = []
    
    for client, client_snapshot_old, client_snapshot_new in parallel_snapshots:
        client_snapshot_difference = None
        
        # Collect snapshot type names, which are present.
        snapshot_types_name_interception = set(e[0] for e in client_snapshot_old)&set(e[0] for e in client_snapshot_new)
        
        client_snapshot_old = dict(client_snapshot_old)
        client_snapshot_new = dict(client_snapshot_new)
        
        for snapshot_type_name in snapshot_types_name_interception:
            type_specific_snapshot_old = client_snapshot_old[snapshot_type_name]
            type_specific_snapshot_new = client_snapshot_new[snapshot_type_name]
            snapshot_taker, difference_calculator, reverter = SNAPSHOT_TAKERS[snapshot_type_name]
            
            snapshot_type_specific_difference = \
                difference_calculator(client, type_specific_snapshot_old, type_specific_snapshot_new)
            
            # `difference_calculator` might return `None`
            if (snapshot_type_specific_difference is not None):
                if (client_snapshot_difference is None):
                    client_snapshot_difference = []
                
                client_snapshot_difference.append((snapshot_type_name, snapshot_type_specific_difference))
        
        if (client_snapshot_difference is not None):
            snapshot_difference.append((client, client_snapshot_difference))
    
    return snapshot_difference


def revert_snapshot(snapshot_difference):
    """
    Reverts the clients to a previous state based on snapshots.
    
    Parameters
    ----------
    snapshot_difference : `list` of `tuple` (``Client``, `list` of `tuple` (`str`, `Any`))
        Difference between 2 snapshot.
    """
    for client, client_snapshot_difference in snapshot_difference:
        for snapshot_type_name, snapshot_type_specific_difference in client_snapshot_difference:
            snapshot_taker, difference_calculator, reverter = SNAPSHOT_TAKERS[snapshot_type_name]
            reverter(client, snapshot_type_specific_difference)
