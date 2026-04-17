import vampytest

from ..fields import validate_type
from ..preinstanced import WebhookType


def _iter_options__passing():
    yield None, WebhookType.none
    yield WebhookType.server, WebhookType.server
    yield WebhookType.server.value, WebhookType.server


def _iter_options__type_error():
    yield 12.6
    yield ''


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_type(input_value):
    """
    Tests whether ``validate_type`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value.
    
    Returns
    -------
    output : ``WebhookType``
        
    Raises
    ------
    TypeError
    """
    output = validate_type(input_value)
    vampytest.assert_instance(output, WebhookType)
    return output
