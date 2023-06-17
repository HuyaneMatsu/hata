import vampytest

from ....role import Role

from ..fields import put_roles_into


def iter_options():
    role_id = 202306100007
    role_name = 'Koishi'
    
    role = Role.precreate(
        role_id,
        name = role_name,
    )
    
    yield {}, True, {'roles': []}
    yield {role_id: role}, True, {'roles': [role.to_data(defaults = True, include_internals = True)]}


@vampytest._(vampytest.call_from(iter_options()).returning_last())
def test__put_roles_into(input_value, defaults):
    """
    Tests whether ``put_roles_into`` works as intended.
    
    Parameters
    ----------
    input_value : `dict<int, Role>`
        Input value to serialise.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_roles_into(input_value, {}, defaults)
