import vampytest

from .....discord.message import Message

from ..message import CONVERSION_MESSAGE


def _iter_options__set_validator():
    message = Message.precreate(202405190001)
    
    yield object(), []
    yield None, [None]
    yield message, [message]


@vampytest._(vampytest.call_from(_iter_options__set_validator()).returning_last())
def test__CONVERSION_MESSAGE__set_validator(input_value):
    """
    Tests whether ``CONVERSION_MESSAGE.set_validator`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test.
    
    Returns
    -------
    output : `list<None | Message>`
    """
    return [*CONVERSION_MESSAGE.set_validator(input_value)]
