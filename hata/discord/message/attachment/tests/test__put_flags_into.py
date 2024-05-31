import vampytest

from ..fields import put_flags_into
from ..flags import AttachmentFlag


def _iter_options():
    yield AttachmentFlag(0), False, {}
    yield AttachmentFlag(0), True, {'flags': 0}
    yield AttachmentFlag(1), False, {'flags': 1}
    yield AttachmentFlag(1), True, {'flags': 1}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_flags_into(input_value, defaults):
    """
    Tests whether ``put_flags_into`` is working as intended.
    
    Parameters
    ----------
    input_value : ``AttachmentFlag``
        The value to serialise.
    defaults : `bool`
        Whether fields of their default value should be included in the output.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_flags_into(input_value, {}, defaults)
