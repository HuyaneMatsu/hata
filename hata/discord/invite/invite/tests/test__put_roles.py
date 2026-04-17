import vampytest

from ....role import Role

from ..fields import put_roles, create_partial_role_data


def _iter_options():
    role_id = 202604040040
    role_name = 'Mamizou'
    
    role = Role.precreate(
        role_id,
        name = role_name,
    )
    
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'roles': [],
        },
    )
    
    yield (
        (
            role,
        ),
        False,
        {
            'roles': [
                create_partial_role_data(role),
            ],
        },
    )
    
    yield (
        (
            role,
        ),
        True,
        {
            'roles': [
                create_partial_role_data(role),
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_roles(input_value, defaults):
    """
    Tests whether ``put_roles`` works as intended.
    
    Parameters
    ----------
    input_value : ``None | tuple<Role>``
        Input value to serialise.
    
    defaults : `bool`
        Whether fields as their defaults should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_roles(input_value, {}, defaults)
