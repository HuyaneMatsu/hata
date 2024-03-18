from functools import partial as partial_func

import vampytest

from ..constants import (
    CONVERSION_KIND_FIELD, CONVERSION_KIND_KEYWORD, CONVERSION_KIND_NONE, CONVERSION_KIND_POSITIONAL
)
from ..descriptor import _select_setter


def _test_attribute_requester(options, attribute_name):
    try:
        return options[attribute_name]
    except KeyError:
        raise RuntimeError from None


def _iter_options__passing():
    setter_default = lambda *p: None
    setter_field = lambda *p: None
    setter_positional = lambda *p: None
    setter_keyword = lambda *p: None
    
    options = {
        '_setter_none': setter_default,
        '_setter_field': setter_field,
        '_setter_positional': setter_positional,
        '_setter_keyword': setter_keyword,
    }
    
    attribute_requester = partial_func(_test_attribute_requester, options)
    
    yield CONVERSION_KIND_NONE, attribute_requester, setter_default
    yield CONVERSION_KIND_FIELD, attribute_requester, setter_field
    yield CONVERSION_KIND_POSITIONAL, attribute_requester, setter_positional
    yield CONVERSION_KIND_KEYWORD, attribute_requester, setter_keyword


def _iter_options__runtime_error():
    attribute_requester = partial_func(_test_attribute_requester, {})
    
    yield CONVERSION_KIND_POSITIONAL, attribute_requester
    yield -1, attribute_requester


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__runtime_error()).raising(RuntimeError))
def test__select_setter(kind, attribute_requester):
    """
    Tests whether ``kind`` works as intended.
    
    Parameters
    ----------
    kind : `int`
        Conversion kind to select setter for.
    attribute_requester : `callable`
        Function allowing to request type attribute before the type is created.
    
    Returns
    -------
    setter : `FunctionType`
    
    Raises
    ------
    RuntimeError
    """
    return _select_setter(kind, attribute_requester)
