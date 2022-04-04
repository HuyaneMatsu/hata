__all__ = ('calculate_snapshot_difference', 'revert_snapshot', 'take_snapshot',)

from ....discord.core import CLIENTS

from .base_snapshot_type import SNAPSHOT_TYPES


def take_snapshot():
    """
    Takes a snapshot of the clients.
    
    Returns
    -------
    snapshots : `list` of ``BaseSnapshotType``
    """
    snapshots = []
    
    for client in CLIENTS.values():
        for snapshot_type in SNAPSHOT_TYPES:
            snapshot = snapshot_type(client)
            snapshots.append(snapshot)
    
    return snapshots


def _build_snapshot_tree(snapshots):
    """
    Builds a tree fro the given snapshot.
    
    Parameters
    ----------
    snapshots : `list` of ``BaseSnapshotType``
        The snapshot to build tree from.
    
    Returns
    -------
    snapshot_tree : `dict` of (``client``, `dict` of (`type`, ``BaseSnapshotType``) items) items
    """
    snapshot_tree = {}
    
    for snapshot in snapshots:
        client = snapshot.client
        if client is None:
            continue
        
        try:
            by_client = snapshot_tree[client]
        except KeyError:
            by_client = {}
            snapshot_tree[client] = by_client
        
        by_client[type(snapshot)] = snapshot
    
    return snapshot_tree


def calculate_snapshot_difference(snapshots_1, snapshots_2):
    """
    Calculates snapshot differences between two snapshots.
    
    Parameters
    ----------
    snapshots_1 : `list` of ``BaseSnapshotType``
        Old taken snapshot.
    snapshots_2 : `list` of ``BaseSnapshotType``
        New taken snapshot.
    
    Returns
    -------
    new_snapshots : `list` of ``BaseSnapshotType``
    """
    tree_1 = _build_snapshot_tree(snapshots_1)
    tree_2 = _build_snapshot_tree(snapshots_2)
    
    new_snapshots = []
    
    for client in {*tree_1.keys(), *tree_2.keys()}:
        try:
            snapshots_by_type_1 = tree_1[client]
        except KeyError:
            continue
        
        try:
            snapshots_by_type_2 = tree_2[client]
        except KeyError:
            continue
        
        for snapshot_type in {*snapshots_by_type_1, *snapshots_by_type_2}:
            try:
                snapshot_1 = snapshots_by_type_1[snapshot_type]
            except KeyError:
                continue
            
            try:
                snapshot_2 = snapshots_by_type_2[snapshot_type]
            except KeyError:
                continue
            
            new_snapshot = snapshot_1 - snapshot_2
            new_snapshots.append(new_snapshot)
    
    return new_snapshots


def revert_snapshot(snapshots):
    """
    Reverts the clients to a previous state based on snapshots.
    
    Parameters
    ----------
    snapshots : `list` of ``BaseSnapshotType``
        DSnapshots to revert
    """
    for snapshot in snapshots:
        if snapshot.is_revertible():
            snapshot.revert()
