import vampytest

from ...http import DiscordApiClient

from ..fields import validate_api


def _iter_options__passing():
    yield None, None
    
    api = DiscordApiClient(False, 'koishi')
    yield api, api


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_api(input_value):
    """
    Tests whether `validate_api` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to validate.
    
    Returns
    -------
    output : `None | DiscordApiClient`
    
    Raises
    ------
    TypeError
    """
    return validate_api(input_value)
