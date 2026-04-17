import vampytest

from ...message_snapshot import MessageSnapshot

from ..fields import validate_snapshots


def _iter_options__passing():
    snapshot_0 = MessageSnapshot(content = 'Hell')
    snapshot_1 = MessageSnapshot(content = 'Rose')
    
    yield None, None
    yield [], None
    yield [snapshot_0], (snapshot_0,)
    yield [snapshot_0, snapshot_1], (snapshot_0, snapshot_1)


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_snapshots(input_value):
    """
    Tests whether ``validate_snapshots`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | tuple<MessageSnapshot>`
    
    Raises
    ------
    TypeError
    """
    output = validate_snapshots(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output   
