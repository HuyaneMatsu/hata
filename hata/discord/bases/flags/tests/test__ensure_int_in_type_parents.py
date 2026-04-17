import vampytest

from ..flag_meta import _ensure_int_in_type_parents


def _iter_options():
    yield (), (int,)
    yield (object,), (int, object)
    yield (int, object), (int, object)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__ensure_int_in_type_parents(parent_types):
    """
    Tests whether ``_ensure_int_in_type_parents`` works as intended.
    
    Parameters
    ----------
    type_parents : `tuple<type>`
        Parent types.
    
    Returns
    -------
    output : `tuple<type>`
    """
    output = _ensure_int_in_type_parents(parent_types)
    vampytest.assert_instance(output, tuple)
    for element in output:
        vampytest.assert_instance(element, type)
    return output
