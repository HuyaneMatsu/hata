import vampytest

from ....localization import Locale

from ..fields import validate_description_localizations


def _iter_options():
    yield None, None
    yield {}, None
    yield (
        {
            Locale.dutch: 'aya',
            Locale.greek.value: 'yya',
        },
        {
            Locale.dutch: 'aya',
            Locale.greek: 'yya',
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_description_localizations__passing(input_value):
    """
    Tests whether ``validate_description_localizations`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | dict<Locale, str>`
    """
    return validate_description_localizations(input_value)
