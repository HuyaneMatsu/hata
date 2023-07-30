import vampytest

from ....channel import Channel

from ..fields import validate_channel


def _iter_options():
    channel_id = 202211010012
    channel = Channel.precreate(channel_id)
    yield channel, channel


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_channel__passing(input_value):
    """
    Tests whether `validate_channel` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : ``Channel``
        The channel to validate.
    
    Returns
    -------
    output : ``Channel``
    """
    return validate_channel(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_channel__type_error(input_value):
    """
    Tests whether `validate_channel` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Value to pass.
    
    Raises
    ------
    TypeError
    """
    validate_channel(input_value)
