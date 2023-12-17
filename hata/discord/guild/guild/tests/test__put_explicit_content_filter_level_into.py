import vampytest

from ..fields import put_explicit_content_filter_level_into
from ..preinstanced import ExplicitContentFilterLevel


def _iter_options():
    yield (
        ExplicitContentFilterLevel.no_role,
        False,
        {'explicit_content_filter': ExplicitContentFilterLevel.no_role.value},
    )
    yield (
        ExplicitContentFilterLevel.no_role,
        True,
        {'explicit_content_filter': ExplicitContentFilterLevel.no_role.value},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_explicit_content_filter_level_into(input_value, defaults):
    """
    Tests whether ``put_explicit_content_filter_level_into`` works as intended.
    
    Parameters
    ----------
    input_value : ``ExplicitContentFilterLevel``
        The value to serialize.
    defaults : `bool`
        Whether fields with their values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_explicit_content_filter_level_into(input_value, {}, defaults)
