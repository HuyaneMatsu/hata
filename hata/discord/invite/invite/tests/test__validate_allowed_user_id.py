import vampytest

from ....user import User

from ..fields import validate_allowed_user_id


def _iter_options():
    user_id_0 = 202610070000
    
    user_0 = User.precreate(
        user_id_0,
    )
    
    yield (
        user_id_0,
        user_id_0,
    )
    
    yield (
        user_0,
        user_id_0,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_allowed_user_id(input_value):
    output = validate_allowed_user_id(input_value)
    vampytest.assert_instance(output, int)
    return output
