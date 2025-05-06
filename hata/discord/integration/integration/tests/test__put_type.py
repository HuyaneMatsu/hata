import vampytest

from ..fields import put_type
from ..preinstanced import IntegrationType


def _iter_options():
    yield IntegrationType.discord, False, {'type': IntegrationType.discord.value}
    yield IntegrationType.discord, True, {'type': IntegrationType.discord.value}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_type(input_value, defaults):
    """
    Tests whether ``put_type`` is working as intended.
    
    Parameters
    ----------
    input_value : ``IntegrationType``
        Input value.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_type(input_value, {}, defaults)
