import vampytest

from ....permission import Permission

from ..fields import put_permissions


def _iter_options():
    yield (
        Permission(),
        False,
        {
            'permissions': '0',
        },
    )
    
    yield (
        Permission(),
        True,
        {
            'permissions': '0',
        },
    )
    
    yield (
        Permission(1),
        False,
        {
            'permissions': '1',
        },
    )
    
    yield (
        Permission(1),
        True,
        {
            'permissions': '1',
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_permissions(input_value, defaults):
    """
    Tests whether ``put_permissions`` is working as intended.
    
    Parameters
    ----------
    input_value : ``Permission``
        Value to serialize.
    
    defaults : `bool`
        Whether fields as their defaults should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_permissions(input_value, {}, defaults)
