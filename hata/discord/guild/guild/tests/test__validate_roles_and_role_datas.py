import vampytest

from ....role import Role

from ..fields import validate_roles_and_role_datas


def iter_options__passing():
    role_id = 20230606290001
    role_name = 'Koishi'
    
    role = Role.precreate(
        role_id,
        name = role_name,
    )
    
    yield None, None
    yield [], None
    yield [role], [role]
    yield [{'name': role_name}], [{'name': role_name}]
    yield [role, {'name': role_name}], [role, {'name': role_name}]

    
@vampytest._(vampytest.call_from(iter_options__passing()).returning_last())
def test__validate_roles_and_role_datas__passing(input_value):
    """
    Tests whether ``validate_roles_and_role_datas`` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        Value to pass to the validators.
    
    Returns
    -------
    expected_output : `None | list<Role | dict>`
    """
    return validate_roles_and_role_datas(input_value)


def iter_options__type_error():
    yield 12.6
    yield [12.6]
    yield {}


@vampytest.raising(TypeError)
@vampytest.call_from(iter_options__type_error())
def test__validate_roles_and_role_datas__type_error(input_value):
    """
    Tests whether ``validate_roles_and_role_datas`` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        Value to pass to the validators.
    
    Raises
    ------
    TypeError
        The occurred exception.
    """
    validate_roles_and_role_datas(input_value)
