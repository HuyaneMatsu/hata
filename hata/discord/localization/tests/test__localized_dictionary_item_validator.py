import vampytest

from ..helpers import localized_dictionary_item_validator
from ..preinstanced import Locale


def _iter_options__passing():
    yield (
        (Locale.greek, 'miau'),
        'mister',
        (Locale.greek, 'miau'),
    )
    
    yield (
        ('orin', 'miau'),
        'mister',
        (Locale('orin'), 'miau'),
    )


def _iter_options__type_error():
    yield (
        (12, 'miau'),
        'mister',
    )
    
    yield (
        ('orin', 12),
        'mister',
    )


def _iter_options__value_error():
    yield (
        ('', 'miau'),
        'mister',
    )
    
    yield (
        ('orin', ''),
        'mister',
    )


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__localized_dictionary_item_validator(item, parameter_name):
    """
    Tests whether ``localized_dictionary_item_validator`` works as intended.
    
    Parameters
    ----------
    key : (Locale | str, str)
        An item representing a `locale` - `str` pair.
    
    parameter_name : `str`
        The parameter's name to raise exception with.
    
    Returns
    -------
    output : `(Locale, str)`
    
    Raises
    ------
    TypeError
    ValueError
    """
    output = localized_dictionary_item_validator(item, parameter_name)
    
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    vampytest.assert_instance(output[0], Locale)
    vampytest.assert_instance(output[1], str)
    
    return output
