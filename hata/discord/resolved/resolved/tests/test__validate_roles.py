import vampytest

from ....role import Role

from ..fields import validate_roles


def _iter_options__passing():
    role_id = 202211050018
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
        {
            role_id: role,
        },
    )
    
    yield (
        {
            role_id: role,
        },
        {
            role_id: role,
        },
    )


def _iter_options__type_error():
    yield 12.6
    yield [12.6]
    yield {12.6: 12.6}


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_roles(input_value):
    """
    Tests whether ``validate_roles`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to pass to the validators.
    
    Returns
    -------
    output : ``None | dict<int, Role>``
    
    Raises
    ------
    TypeError
    """
    output = validate_roles(input_value)
    
    vampytest.assert_instance(output, dict, nullable = True)
    if (output is not None):
        for key, value in output.items():
            vampytest.assert_instance(key, int)
            vampytest.assert_instance(value, Role)
    
    return output
