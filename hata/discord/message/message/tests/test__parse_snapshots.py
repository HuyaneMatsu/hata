import vampytest

from ...message_snapshot import MessageSnapshot

from ..fields import parse_snapshots


def _iter_options():
    snapshot_0 = MessageSnapshot(content = 'Hell')
    snapshot_1 = MessageSnapshot(content = 'Rose')
    
    yield (
        {},
        None,
    )
    
    yield (
        {'message_snapshots': None},
        None,
    )
    
    yield (
        {'message_snapshots': [snapshot_0.to_data()]},
        (snapshot_0,),
    )
    
    yield (
        {'message_snapshots': [snapshot_0.to_data(), snapshot_1.to_data()]},
        (snapshot_0, snapshot_1),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_snapshots(input_data):
    """
    Tests whether ``parse_snapshots`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | tuple<MessageSnapshot>`
    """
    output = parse_snapshots(input_data)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output
