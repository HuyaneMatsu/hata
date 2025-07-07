import vampytest

from ....localization import Locale

from ..fields import validate_name_localizations


def _iter_options__passing():
    yield (
        None,
        None,
    )
    
    yield (
        {},
        None,
    )
    
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


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
def test__validate_name_localizations(input_value):
    """
    Tests whether ``validate_name_localizations`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        value to validate.
    
    Returns
    -------
    output : ``None | dict<Locale, str>``
    """
    output = validate_name_localizations(input_value)
    vampytest.assert_instance(output, dict, nullable = True)
    
    if (output is not None):
        for key, value in output.items():
            vampytest.assert_instance(key, Locale)
            vampytest.assert_instance(value, str)
    
    return output
