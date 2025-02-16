import vampytest

from ..fields import put_type
from ..preinstanced import EntitySelectDefaultValueType


def _iter_options():
    yield EntitySelectDefaultValueType.role, False, {'type': EntitySelectDefaultValueType.role.value}
    yield EntitySelectDefaultValueType.role, True, {'type': EntitySelectDefaultValueType.role.value}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_type(input_value, defaults):
    """
    Tests whether ``put_type`` is working as intended.
    
    Parameters
    ----------
    input_value : ``EntitySelectDefaultValueType``
        Input value.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_type(input_value, {}, defaults)
