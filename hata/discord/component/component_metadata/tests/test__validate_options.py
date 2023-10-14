import vampytest

from ...string_select_option import StringSelectOption

from ..fields import validate_options


def _iter_options():
    option_0 = StringSelectOption('hello')
    option_1 = StringSelectOption('hi')
    
    yield None, None
    yield [], None
    yield [option_0], (option_0,)
    yield [option_0, option_1], (option_0, option_1,)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_options__passing(input_value):
    """
    Tests whether ``validate_options`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `None | tuple<StringSelectOption>`
    """
    return validate_options(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
@vampytest.call_with([13.6])
def test__validate_options__type_error(input_value):
    """
    Tests whether ``validate_options`` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_options(input_value)
