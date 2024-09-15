import vampytest

from ..fields import put_hang_type_into
from ..preinstanced import HangType


def _iter_options():
    yield HangType.none, False, {'state': HangType.none.value}
    yield HangType.none, True, {'state': HangType.none.value}
    yield HangType.gaming, False, {'state': HangType.gaming.value}
    yield HangType.gaming, True, {'state': HangType.gaming.value}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_hang_type_into(input_value, defaults):
    """
    Tests whether ``put_hang_type_into`` is working as intended.
    
    Parameters
    ----------
    input_value : ``HangType``
        The value to serialise.
    defaults : `bool`
        Whether values with their default value should be included in the output as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_hang_type_into(input_value, {}, defaults)
