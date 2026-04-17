import vampytest

from ..fields import parse_type
from ..preinstanced import ApplicationRoleConnectionMetadataType


def _iter_options():
    yield {}, ApplicationRoleConnectionMetadataType.none
    yield (
        {'type': ApplicationRoleConnectionMetadataType.integer_equal.value},
        ApplicationRoleConnectionMetadataType.integer_equal
    )


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
    output : ``ApplicationRoleConnectionMetadataType``
    """
    output = parse_type(input_data)
    vampytest.assert_instance(output, ApplicationRoleConnectionMetadataType)
    return output
