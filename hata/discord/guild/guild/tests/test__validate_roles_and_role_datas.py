import vampytest

from ....role import Role

from ..fields import validate_roles_and_role_datas


def _iter_options__passing():
    role_id = 20230606290001
    role_name = 'Koishi'
    
    role = Role.precreate(
        role_id,
        name = role_name,
    )
    
    yield (
        None,
        None,
    )
    
    yield (
        [],
        None,
    )
    
    yield (
        [
            role,
        ],
        [
            role,
        ],
    )
    
    yield (
        [
            {
                'name': role_name,
            },
        ],
        [
            {
                'name': role_name,
            },
        ],
    )
    
    yield (
        [
            role,
            {
                'name': role_name,
            },
        ],
        [
            role,
            {
                'name': role_name,
            },
        ],
    )


def _iter_options__type_error():
    yield 12.6
    yield [12.6]
    yield {}


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_roles_and_role_datas(input_value):
    """
    Tests whether ``validate_roles_and_role_datas`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to pass to the validators.
    
    Returns
    -------
    output : ``None | list<Role | dict<str, object>>``
    
    Raises
    ------
    TypeError
    """
    output = validate_roles_and_role_datas(input_value)
    
    vampytest.assert_instance(output, list, nullable = True)
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, Role, dict)
    
    return output
