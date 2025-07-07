import vampytest

from ..fields import parse_access_type
from ..preinstanced import SKUAccessType


def _iter_options():
    yield (
        {},
        SKUAccessType.none,
    )
    
    yield (
        {
            'access_type': None,
        },
        SKUAccessType.none,
    )
    
    yield (
        {
            'access_type': SKUAccessType.full.value,
        },
        SKUAccessType.full,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_access_type(input_data):
    """
    Tests whether ``parse_access_type`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data.
    
    Returns
    -------
    output : ``SKUAccessType``
    """
    output = parse_access_type(input_data)
    vampytest.assert_instance(output, SKUAccessType)
    return output
