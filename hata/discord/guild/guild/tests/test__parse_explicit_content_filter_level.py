import vampytest

from ..fields import parse_explicit_content_filter_level
from ..preinstanced import ExplicitContentFilterLevel


def _iter_options():
    yield ({}, ExplicitContentFilterLevel.disabled)
    yield ({'explicit_content_filter': ExplicitContentFilterLevel.no_role.value}, ExplicitContentFilterLevel.no_role)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_explicit_content_filter_level(input_data):
    """
    Tests whether ``parse_explicit_content_filter_level`` works as intended.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``ExplicitContentFilterLevel``
    """
    output = parse_explicit_content_filter_level(input_data)
    vampytest.assert_instance(output, ExplicitContentFilterLevel)
    return output
