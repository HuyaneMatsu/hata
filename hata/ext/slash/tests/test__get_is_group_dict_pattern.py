from re import compile as re_compile

import vampytest

from ..converters import _get_is_group_dict_pattern


def _iter_options__passing():
    yield re_compile('(?P<hey>[a-z]+)_(?P<mister>[a-z]+)'), True
    yield re_compile('([a-z]+)_([a-z]+)'), False
    yield re_compile('[a-z]+_[a-z]+'), False


def _iter_options__value_error():
    yield re_compile('(?P<hey>[a-z]+)_([a-z]+)')


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__get_is_group_dict_pattern(input_value):
    """
    Tests whether ``_get_is_group_dict_pattern`` works as intended.
    
    Parameters
    ----------
    regex_pattern : `re.Pattern`
        Regex pattern to get details of.
    
    Returns
    -------
    output : `bool`
    
    Raises
    ------
    ValueError
    """
    output = _get_is_group_dict_pattern(input_value)
    vampytest.assert_instance(output, bool)
    return output
