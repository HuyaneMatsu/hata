import vampytest

from ...message_snapshot import MessageSnapshot

from ..fields import put_snapshots


def _iter_options():
    snapshot_0 = MessageSnapshot(content = 'Hell')
    snapshot_1 = MessageSnapshot(content = 'Rose')
    
    yield (
        None,
        False,
        0,
        {},
    )
    
    yield (
        None,
        True,
        0,
        {
            'message_snapshots': [],
        },
    )
    
    yield (
        (snapshot_0, snapshot_1),
        False,
        0,
        {
            'message_snapshots': [
                snapshot_0.to_data(defaults = False, guild_id = 0),
                snapshot_1.to_data(defaults = False, guild_id = 0),
            ],
        },
    )
    
    yield (
        (snapshot_0, snapshot_1),
        True,
        0,
        {
            'message_snapshots': [
                snapshot_0.to_data(defaults = True, guild_id = 0),
                snapshot_1.to_data(defaults = True, guild_id = 0),
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_snapshots(input_value, defaults, guild_id):
    """
    Tests whether ``put_snapshots`` works as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<MessageSnapshot>`
        Value to serialize.
    defaults : `bool`
        Whether values as their defaults should be included as well.
    guild_id : `int`
        Respective guild's identifier.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_snapshots(input_value, {}, defaults, guild_id = guild_id)
