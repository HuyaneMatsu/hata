import vampytest

from ....permission import Permission

from ..fields import put_user_permissions


def _iter_options():
    yield (
        Permission(),
        False,
        {},
    )
    
    yield (
        Permission(),
        True,
        {
            'is_nickname_changeable': False,
        },
    )
    
    yield (
        Permission().update_by_keys(
            change_nickname = True,
        ),
        False,
        {
            'is_nickname_changeable': True,
        },
    )
    
    yield (
        Permission().update_by_keys(
            change_nickname = True,
        ),
        True,
        {
            'is_nickname_changeable': True,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_user_permissions(input_value, defaults):
    """
    Tests whether ``put_user_permissions`` is working as intended.
    
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
    return put_user_permissions(input_value, {}, defaults)
