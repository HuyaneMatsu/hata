import vampytest

from ..helpers import get_localized_length
from ..preinstanced import Locale


def _iter_options():
    value_0 = 'hi'
    value_1 = 'hoi'
    value_2 = 'halo'
    
    yield (
        None,
        None,
        0,
    )
    
    yield (
        value_2,
        {
            Locale.thai: value_0,
            Locale.czech: value_1,
        },
        max(
            len(value) for value in (value_0, value_1, value_2)
        ),
    )
    
    yield (
        value_0,
        {
            Locale.thai: value_2,
            Locale.czech: value_1,
        },
        max(
            len(value) for value in (value_0, value_1, value_2)
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_localized_length(value, value_localizations):
    """
    Tests whether ``get_localized_length`` works as intended.
    
    Parameters
    ----------
    value : `None | str`
        The default value.
    
    value_localizations : ``None | dict<Locale, str>``
        Localizations of the value.
    
    Returns
    -------
    length : `int`
    """
    output = get_localized_length(value, value_localizations)
    vampytest.assert_instance(output, int)
    return output
