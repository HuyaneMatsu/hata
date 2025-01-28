import vampytest

from ..preinstanced_meta import _get_direct_type_parent


def _iter_options():
    yield type, (), None
    yield type, (int, str), int
    yield int, (int, str), None


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_direct_type_parent(meta_type, type_parents):
    """
    Tests whether ``_get_direct_type_parent`` works as intended.
    
    Parameters
    ----------
    meta_type : `type`
        The type that is being instantiated.
    
    type_parents : `tuple<type>`
        The type's parents.
    
    Returns
    -------
    output : `None | type`
    """
    output = _get_direct_type_parent(meta_type, type_parents)
    vampytest.assert_instance(output, type, nullable = True)
    return output
