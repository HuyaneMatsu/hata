import vampytest

from ..fields import parse_type
from ..preinstanced import EmbedType


def _iter_options():
    yield {}, EmbedType.rich
    yield {'type': EmbedType.gifv.value}, EmbedType.gifv


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_type(input_data):
    """
    Tests whether ``parse_type`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data.
    
    Returns
    -------
    output : ``EmbedType``
    """
    return parse_type(input_data)
