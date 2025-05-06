import vampytest

from ..fields import put_type
from ..preinstanced import MessageActivityType


def _iter_options():
    yield MessageActivityType.join, False, {'type': MessageActivityType.join.value}
    yield MessageActivityType.join, True, {'type': MessageActivityType.join.value}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_type(input_value, defaults):
    """
    Tests whether ``put_type`` is working as intended.
    
    Parameters
    ----------
    input_value : ``MessageActivityType``
        Input value.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_type(input_value, {}, defaults)
