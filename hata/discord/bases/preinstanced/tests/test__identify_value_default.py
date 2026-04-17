import vampytest

from ..preinstanced_meta import _identify_value_type


class TestTypeNone():
    __slots__ = ()
    VALUE_DEFAULT = None
    VALUE_TYPE = type(None)


class TestTypeInt():
    __slots__ = ()
    VALUE_DEFAULT = 0
    VALUE_TYPE = int


def _iter_options__passing():
    yield None, True, ..., type(None)
    yield None, True, int, int
    yield None, True, str, str
    
    yield None, False, int, int
    yield None, False, str, str
    
    yield TestTypeNone, True, ..., type(None)
    yield TestTypeNone, True, int, int
    yield TestTypeNone, True, str, str
    
    yield TestTypeNone, False, int, int
    yield TestTypeNone, False, str, str
    
    yield TestTypeInt, True, ..., int
    yield TestTypeInt, True, int, int
    
    yield TestTypeInt, False, ..., int
    yield TestTypeInt, False, int, int


def _iter_options__runtime_error():
    yield None, False, ...
    yield TestTypeNone, False, ...


def _iter_options__type_error():
    yield TestTypeInt, True, str
    yield TestTypeInt, False, str
    
    yield None, True, object
    yield None, False, object
    yield TestTypeNone, True, object
    yield TestTypeNone, False, object
    yield TestTypeInt, True, object
    yield TestTypeInt, False, object


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__runtime_error()).raising(RuntimeError))
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__identify_value_type(type_parent, base_type, value_type):
    """
    Tests whether ``_identify_value_type`` works as intended.
    
    Parameters
    ----------
    type_parent : `None | type`
        Parent type.
    
    base_type : `bool`
        Whether the currently created type is a base type.
    
    value_type : `type | ...`
        The passed value type.
    
    Returns
    -------
    output : `int | str`
    
    Raises
    ------
    RuntimeError
    TypeError
    """
    output = _identify_value_type(type_parent, base_type, value_type)
    vampytest.assert_instance(output, type)
    return output
