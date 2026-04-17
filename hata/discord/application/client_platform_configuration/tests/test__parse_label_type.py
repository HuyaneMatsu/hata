import vampytest

from ..fields import parse_label_type
from ..preinstanced import LabelType


def _iter_options():
    yield {}, LabelType.none
    yield {'label_type': LabelType.new.value}, LabelType.new


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_label_type(input_data):
    """
    Tests whether ``parse_label_type`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data.
    
    Returns
    -------
    output : ``LabelType``
    """
    output = parse_label_type(input_data)
    vampytest.assert_instance(output, LabelType)
    return output
