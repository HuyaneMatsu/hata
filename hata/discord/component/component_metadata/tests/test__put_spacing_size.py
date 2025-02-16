import vampytest

from ..constants import SEPARATOR_SPACING_SIZE_DEFAULT
from ..fields import put_spacing_size
from ..preinstanced import SeparatorSpacingSize


def _iter_options():
    yield SEPARATOR_SPACING_SIZE_DEFAULT, False, {'spacing': SEPARATOR_SPACING_SIZE_DEFAULT.value}
    yield SEPARATOR_SPACING_SIZE_DEFAULT, True, {'spacing': SEPARATOR_SPACING_SIZE_DEFAULT.value}
    yield SeparatorSpacingSize.large, False, {'spacing': SeparatorSpacingSize.large.value}
    yield SeparatorSpacingSize.large, True, {'spacing': SeparatorSpacingSize.large.value}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_spacing_size(input_value, defaults):
    """
    Tests whether ``put_spacing_size`` is working as intended.
    
    Parameters
    ----------
    input_value : ``SeparatorSpacingSize``
        The value to serialise.
    defaults : `bool`
        Whether values with their default value should be included in the output as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_spacing_size(input_value, {}, defaults)
