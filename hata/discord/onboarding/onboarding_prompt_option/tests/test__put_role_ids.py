import vampytest

from ..fields import put_role_ids


def _iter_options():
    role_id = 202303030007
    
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'role_ids': [],
        },
    )
    
    yield (
        (role_id,),
        False,
        {
            'role_ids': [
                str(role_id),
            ]
        },
    )
    
    yield (
        (role_id,),
        True,
        {
            'role_ids': [
                str(role_id),
            ]
        },
    )
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_role_ids(input_value, defaults):
    """
    Tests whether ``put_role_ids`` is working as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<int>`
        Role identifiers to serialize.
    
    defaults : `bool`
        Whether fields with their default values should be included.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_role_ids(input_value, {}, defaults)
