import vampytest

from ..preinstanced_meta import _inherit_hash_function


class TestType():
    def __hash__(self):
        return 0


def _iter_options():
    hash_function = lambda self: 1
    
    yield (
        {},
        None,
        {},
    )
    
    yield (
        {
            '__hash__': hash_function,
        },
        None,
        {
            '__hash__': hash_function,
        },
    )
    
    yield (
        {},
        TestType,
        {
            '__hash__': TestType.__hash__,
        },
    )
    
    yield (
        {
            '__hash__': hash_function,
        },
        TestType,
        {
            '__hash__': hash_function,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__inherit_hash_function(type_attributes, type_parent):
    """
    Inherits the parent's hash method of the parent type if required.
    
    Parameters
    ----------
    type_attributes : `dict<str, object>`
        The type attributes of the created type.
    
    type_parent : `None | type`
        Parent type.
    """
    type_attributes = type_attributes.copy()
    _inherit_hash_function(type_attributes, type_parent)
    return type_attributes
