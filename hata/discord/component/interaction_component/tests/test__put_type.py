import vampytest

from ....component import ComponentType

from ..fields import put_type


def _iter_options():
    yield ComponentType.none, False, {'type': ComponentType.none.value}
    yield ComponentType.row, False, {'type': ComponentType.row.value}
    yield ComponentType.none, True, {'type': ComponentType.none.value}
    yield ComponentType.row, True, {'type': ComponentType.row.value}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_type(input_value, defaults):
    """
    Tests whether ``put_type`` is working as intended.
    
    Parameters
    ----------
    input_value : ``ComponentType``
        Input value.
    
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_type(input_value, {}, defaults)
