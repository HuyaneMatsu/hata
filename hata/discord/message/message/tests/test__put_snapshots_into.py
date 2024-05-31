import vampytest

from ...message_snapshot import MessageSnapshot

from ..fields import put_snapshots_into


def _iter_options():
    snapshot_0 = MessageSnapshot(content = 'Hell')
    snapshot_1 = MessageSnapshot(content = 'Rose')
    
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'message_snapshots': [],
        },
    )
    
    yield (
        (snapshot_0, snapshot_1),
        False,
        {
            'message_snapshots': [
                snapshot_0.to_data(defaults = False),
                snapshot_1.to_data(defaults = False),
            ],
        },
    )
    
    yield (
        (snapshot_0, snapshot_1),
        True,
        {
            'message_snapshots': [
                snapshot_0.to_data(defaults = True),
                snapshot_1.to_data(defaults = True),
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_snapshots_into(input_value, defaults):
    """
    Tests whether ``put_snapshots_into`` works as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<MessageSnapshot>`
        Value to serialize.
    defaults : `bool`
        Whether values as their defaults should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_snapshots_into(input_value, {}, defaults)
