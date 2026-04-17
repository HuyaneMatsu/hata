import vampytest

from ....role import Role

from ..fields import validate_roles


def _iter_options__passing():
    role_id_0 = 202604040050
    role_id_1 = 202604040051
    role_name = 'Koishi'
    
    role_0 = Role.precreate(
        role_id_0,
        name = role_name,
    )
    
    role_1 = Role.precreate(
        role_id_1,
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
            role_0,
            role_1,
        ],
        (
            role_0,
            role_1
        )
    )
    
    yield (
        [
            role_1,
            role_0,
        ],
        (
            role_0,
            role_1
        )
    )


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


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
    output : ``None | tuple<Role>``
    
    Raises
    ------
    TypeError
    """
    output = validate_roles(input_value)
    
    vampytest.assert_instance(output, tuple, nullable = True)
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, Role)
    
    return output
