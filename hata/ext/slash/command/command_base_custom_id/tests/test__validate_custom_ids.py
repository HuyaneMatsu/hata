import vampytest

from re import compile as re_compile

from ..helpers import _validate_custom_ids


def _iter_options__passing():
    string_0 = 'apple'
    string_1 = 'bad'
    
    pattern_0 = re_compile('apples?')
    pattern_1 = re_compile('bads?')
    
    yield string_0, {string_0}
    yield pattern_0, {pattern_0}
    yield [string_0, string_0], {string_0}
    yield [pattern_0, pattern_0], {pattern_0}
    yield [string_0, string_1], {string_0, string_1}
    yield [pattern_0, pattern_1], {pattern_0, pattern_1}
    yield [string_0, pattern_0], {string_0, pattern_0}


def _iter_options__type_error():
    # Invalid type
    yield None
    yield object()


def _iter_options__value_error():
    # At least 1 is required.
    yield []


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_custom_ids(input_value):
    """
    Tests whether ``_validate_custom_ids`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The validate.
    
    Returns
    -------
    output : `set<str | re.Pattern>`
    
    Raises
    ------
    TypeError
    ValueError
    """
    output = _validate_custom_ids(input_value)
    vampytest.assert_instance(output, set)
    return output
