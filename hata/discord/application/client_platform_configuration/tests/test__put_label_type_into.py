import vampytest

from ..fields import put_label_type_into
from ..preinstanced import LabelType


def _iter_options():
    yield LabelType.new, False, {'label_type': LabelType.new.value}
    yield LabelType.new, True, {'label_type': LabelType.new.value}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_label_type_into(input_value, defaults):
    """
    Tests whether ``put_label_type_into`` is working as intended.
    
    Parameters
    ----------
    input_value : ``LabelType``
        Input value.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_label_type_into(input_value, {}, defaults)
