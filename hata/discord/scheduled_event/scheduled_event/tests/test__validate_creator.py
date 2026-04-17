import vampytest

from ....user import ClientUserBase, User, ZEROUSER

from ..fields import validate_creator


def _iter_options__passing():
    creator = User.precreate(202405010002, name = 'Yuuka')
    yield creator, creator
    yield None, ZEROUSER


def _iter_options__type_error():
    yield 'a'


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_creator(input_value):
    """
    Tests whether `validate_creator` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : ``ClientUserBase``
    
    Raises
    ------
    TypeError
    """
    output = validate_creator(input_value)
    vampytest.assert_instance(output, ClientUserBase)
    return output
