import vampytest

from ..fields import put_type
from ..preinstanced import ApplicationRoleConnectionMetadataType


def _iter_options():
    yield (
        ApplicationRoleConnectionMetadataType.integer_equal,
        False,
        {'type': ApplicationRoleConnectionMetadataType.integer_equal.value},
    )
    yield (
        ApplicationRoleConnectionMetadataType.integer_equal,
        True,
        {'type': ApplicationRoleConnectionMetadataType.integer_equal.value},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_type(input_value, defaults):
    """
    Tests whether ``put_type`` is working as intended.
    
    Parameters
    ----------
    input_value : ``ApplicationRoleConnectionMetadataType``
        Input value.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_type(input_value, {}, defaults)
