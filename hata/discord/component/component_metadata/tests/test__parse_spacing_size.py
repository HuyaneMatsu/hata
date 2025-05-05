import vampytest

from ..constants import SEPARATOR_SPACING_SIZE_DEFAULT
from ..fields import parse_spacing_size
from ..preinstanced import SeparatorSpacingSize


def _iter_options():
    yield (
        {},
        SEPARATOR_SPACING_SIZE_DEFAULT,
    )
    
    yield (
        {
            'spacing': None,
        },
        SeparatorSpacingSize.none,
    )
    
    yield (
        {
            'spacing': SEPARATOR_SPACING_SIZE_DEFAULT.value,
        },
        SEPARATOR_SPACING_SIZE_DEFAULT,
    )
    
    yield (
        {
            'spacing': SeparatorSpacingSize.large.value,
        },
        SeparatorSpacingSize.large,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_spacing_size(input_data):
    """
    Tests whether ``parse_spacing_size`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``SeparatorSpacingSize``
    """
    output = parse_spacing_size(input_data)
    vampytest.assert_instance(output, SeparatorSpacingSize)
    return output
