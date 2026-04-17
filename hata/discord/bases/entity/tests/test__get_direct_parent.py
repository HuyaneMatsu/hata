import vampytest

from ..slotted_meta import _get_direct_parent


def _iter_options__passing():
    yield (type, 'miau', (), None)
    yield (type, 'miau', (int, ), int)


def _iter_options__runtime_error():
    yield (type, 'miau', (int, int))


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__runtime_error()).raising(RuntimeError))
def test__get_direct_parent(meta_type, type_name, type_parents):
    """
    Tests whether ``_get_direct_parent`` works as intended.
    
    Parameters
    ----------
    type_name : `str`
        The created type's name.
    
    type_parents : `tuple<type>`
        The parent types of the creates type.
    
    type_attributes : `dict<str, object>`
        The type attributes of the created type.
    
    Returns
    -------
    output : `None | type`
    
    Raises
    ------
    RuntimeError
    """
    output = _get_direct_parent(meta_type, type_name, type_parents)
    vampytest.assert_instance(output, type, nullable = True)
    return output
