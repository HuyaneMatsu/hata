import vampytest

from ....permission import Permission

from ..fields import put_required_permissions


def _iter_options():
    yield (
        Permission(),
        False,
        {
            'default_member_permissions': None,
        },
    )
    
    yield (
        Permission(),
        True,
        {
            'default_member_permissions': None,
        },
    )
    
    yield (
        Permission(1),
        False,
        {
            'default_member_permissions': '1',
        },
    )
    
    yield (
        Permission(1),
        True,
        {
            'default_member_permissions': '1',
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_required_permissions(input_value, defaults):
    """
    Tests whether ``put_required_permissions`` is working as intended.
    
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
    return put_required_permissions(input_value, {}, defaults)
