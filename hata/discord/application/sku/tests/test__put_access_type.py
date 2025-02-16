import vampytest

from ..fields import put_access_type
from ..preinstanced import SKUAccessType


def _iter_options():
    yield SKUAccessType.full, False, {'access_type': SKUAccessType.full.value}
    yield SKUAccessType.full, True, {'access_type': SKUAccessType.full.value}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_access_type(input_value, defaults):
    """
    Tests whether ``put_access_type`` is working as intended.
    
    Parameters
    ----------
    input_value : ``SKUAccessType``
        Input value.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_access_type(input_value, {}, defaults)
