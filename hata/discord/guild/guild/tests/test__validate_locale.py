import vampytest

from ....localization import Locale

from ..fields import validate_locale


def _iter_options():
    yield (Locale.czech, Locale.czech)
    yield (Locale.czech.value, Locale.czech)
    yield (None, Locale.english_us)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_locale__passing(input_value):
    """
    Validates whether ``validate_locale`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Raises
    ------
    output : ``Locale``
    """
    output = validate_locale(input_value)
    vampytest.assert_instance(output, Locale)
    return output


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_locale__type_error(input_value):
    """
    Validates whether ``validate_locale`` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_locale(input_value)
