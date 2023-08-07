import vampytest

from ..fields import put_type_into
from ..preinstanced import ApplicationType


def _iter_options():
    yield ApplicationType.none, False, {'type': None}
    yield ApplicationType.none, True, {'type': None}
    yield ApplicationType.game, False, {'type': ApplicationType.game.value}
    yield ApplicationType.game, True, {'type': ApplicationType.game.value}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_type_into(input_value, defaults):
    """
    Tests whether ``put_type_into`` is working as intended.
    
    Parameters
    ----------
    input_value : ``ApplicationType``
        Input value.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_type_into(input_value, {}, defaults)
