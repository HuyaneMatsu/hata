import vampytest

from ....role import Role

from ..fields import put_roles_and_role_datas_into


def iter_options():
    role_id = 202306290003
    role_name = 'Koishi'
    
    role = Role.precreate(
        role_id,
        name = role_name,
    )
    
    yield None, True, {'roles': []}
    yield None, False, {'roles': []}
    yield [role], True, {'roles': [role.to_data(defaults = True, include_internals = True)]}
    yield [role], False, {'roles': [role.to_data(defaults = False, include_internals = True)]}
    yield [{'name': role_name}], True, {'roles': [{'name': role_name}]}
    yield (
        [role, {'name': role_name}],
        True,
        {'roles': [role.to_data(defaults = True, include_internals = True), {'name': role_name}]},
    )
    

@vampytest._(vampytest.call_from(iter_options()).returning_last())
def test__put_roles_and_role_datas_into(input_value, defaults):
    """
    Tests whether ``put_roles_and_role_datas_into`` works as intended.
    
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
    return put_roles_and_role_datas_into(input_value, {}, defaults)
