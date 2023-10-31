import vampytest

from ....channel import Channel

from ..fields import validate_channel_id


def _iter_options__passing():
    channel_id = 202304260005
    
    yield None, 0
    yield 0, 0
    yield channel_id, channel_id
    yield Channel.precreate(channel_id), channel_id
    yield str(channel_id), channel_id


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
def test__validate_channel_id__passing(input_value):
    """
    Tests whether `validate_channel_id` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to get `channel_id` of.
    
    Returns
    -------
    output : `int`
    """
    return validate_channel_id(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_channel_id__type_error(input_value):
    """
    Tests whether `validate_channel_id` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Input value to get `channel_id` of.
    
    Raises
    ------
    TypeError
        The occurred exception.
    """
    validate_channel_id(input_value)


@vampytest.raising(ValueError)
@vampytest.call_with('-1')
@vampytest.call_with('1111111111111111111111')
@vampytest.call_with(-1)
@vampytest.call_with(1111111111111111111111)
def test__validate_channel_id__value_error(input_value):
    """
    Tests whether `validate_channel_id` works as intended.
    
    Case: `ValueError`.
    
    Parameters
    ----------
    input_value : `object`
        Input value to get `channel_id` of.
    
    Raises
    ------
    ValueError
        The occurred exception.
    """
    validate_channel_id(input_value)
