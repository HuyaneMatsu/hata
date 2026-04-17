import vampytest

from ..fields import parse_themes
from ..preinstanced import ApplicationTheme


def _iter_options():
    yield (
        {},
        None,
    )
    
    yield (
        {
            'themes': None,
        },
        None,
    )
    
    yield (
        {
            'themes': [],
        },
        None,
    )
    
    yield (
        {
            'themes': [
                ApplicationTheme.business.value,
            ],
        },
        (
            ApplicationTheme.business,
        ),
    )
    yield (
        {
            'themes': [
                ApplicationTheme.business.value,
                ApplicationTheme.action.value
            ],
        },
        (
            ApplicationTheme.action,
            ApplicationTheme.business,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_themes(input_data):
    """
    Tests whether ``parse_themes`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``None | tuple<ApplicationTheme>``
    """
    output = parse_themes(input_data)
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, ApplicationTheme)
    
    return output
