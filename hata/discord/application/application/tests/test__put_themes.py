import vampytest

from ..fields import put_themes
from ..preinstanced import ApplicationTheme


def _iter_options():
    yield (
        None,
        False,
        {
            'themes': [],
        },
    )
    
    yield (
        None,
        True,
        {
            'themes': [],
        },
    )
    
    yield (
        (
            ApplicationTheme.business,
        ),
        False,
        {
            'themes': [
                ApplicationTheme.business.value,
            ],
        },
    )
    
    yield (
        (
            ApplicationTheme.business,
        ),
        True,
        {
            'themes': [
                ApplicationTheme.business.value,
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_themes(input_value, defaults):
    """
    Tests whether ``put_themes`` is working as intended.
    
    Parameters
    ----------
    input_value : ``none | tuple<ApplicationTheme>``
        Value to serialize.
    
    defaults : `bool`
        Whether fields with their default value should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_themes(input_value, {}, defaults)
