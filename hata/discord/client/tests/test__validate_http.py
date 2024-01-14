import vampytest
from scarletio.http_client import HTTPClient

from ...core import KOKORO

from ..fields import validate_http


def _iter_options__passing():
    yield None, None
    
    http = HTTPClient(KOKORO)
    yield http, http


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_http(input_value):
    """
    Tests whether `validate_http` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to validate.
    
    Returns
    -------
    output : `None | HTTPClient`
    
    Raises
    ------
    TypeError
    """
    return validate_http(input_value)
