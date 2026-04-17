import vampytest

from ..slotted_meta import _inherit_hash


def _iter_options():
    class Parent():
        def __hash__(self):
            return 0
    
    # no hash
    yield (
        None,
        {},
        {},
    )
    
    # we have hash
    yield (
        None,
        {
            '__hash__' : object.__hash__,
        },
        {
            '__hash__' : object.__hash__,
        },
    )
    
    # parent + no hash
    yield (
        Parent,
        {},
        {
            '__hash__': Parent.__hash__,
        },
    )
    
    # parent + we have hash
    yield (
        Parent,
        {
            '__hash__' : object.__hash__,
        },
        {
            '__hash__' : object.__hash__,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__inherit_hash(direct_parent, type_attributes):
    """
    Tests whether ``_inherit_hash`` works as intended.
    
    Parameters
    ----------
    direct_parent : `None | type`
        The direct parent of the respective type.
    
    type_attributes : `dict<str, object>`
        The type attributes of the created type.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    type_attributes = type_attributes.copy()
    _inherit_hash(direct_parent, type_attributes)
    return type_attributes
