import vampytest

from ..fields import put_explicit_content_filter_level_into
from ..preinstanced import ApplicationExplicitContentFilterLevel


def _iter_options():
    yield (
        ApplicationExplicitContentFilterLevel.filtered,
        False,
        {'explicit_content_filter': ApplicationExplicitContentFilterLevel.filtered.value},
    )
    yield (
        ApplicationExplicitContentFilterLevel.filtered,
        True,
        {'explicit_content_filter': ApplicationExplicitContentFilterLevel.filtered.value},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_explicit_content_filter_level_into(input_value, defaults):
    """
    Tests whether ``put_explicit_content_filter_level_into`` is working as intended.
    
    Parameters
    ----------
    input_value : ``ApplicationExplicitContentFilterLevel``
        Input value.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_explicit_content_filter_level_into(input_value, {}, defaults)
