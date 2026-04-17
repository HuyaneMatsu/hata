import vampytest

from ....role import Role

from ..fields import put_roles


def _iter_options():
    role_id = 202211050017
    role_name = 'Faker'
    
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
            'roles': {},
        },
    )
    
    yield (
        {
            role_id: role,
        },
        False,
        {
            'roles': {
                str(role_id): role.to_data(defaults = False, include_internals = True),
            },
        },
    )
    
    yield (
        {
            role_id: role,
        },
        True,
        {
            'roles': {
                str(role_id): role.to_data(defaults = True, include_internals = True),
            },
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_roles(input_value, defaults):
    """
    Tests whether ``put_roles`` works as intended.
    
    Parameters
    ----------
    input_value : ``dict<int, Role>``
        Input value to serialise.
    
    defaults : `bool`
        Whether fields as their defaults should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_roles(input_value, {}, defaults)
