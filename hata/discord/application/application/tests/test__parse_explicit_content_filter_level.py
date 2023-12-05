import vampytest

from ..fields import parse_explicit_content_filter_level
from ..preinstanced import ApplicationExplicitContentFilterLevel


def _iter_options():
    yield {}, ApplicationExplicitContentFilterLevel.none
    yield (
        {'explicit_content_filter': ApplicationExplicitContentFilterLevel.filtered.value},
        ApplicationExplicitContentFilterLevel.filtered,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_explicit_content_filter_level(input_data):
    """
    Tests whether ``parse_explicit_content_filter_level`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data.
    
    Returns
    -------
    output : ``ApplicationExplicitContentFilterLevel``
    """
    output = parse_explicit_content_filter_level(input_data)
    vampytest.assert_instance(output, ApplicationExplicitContentFilterLevel)
    return output
