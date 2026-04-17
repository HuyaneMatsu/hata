import vampytest

from ....user import User

from ..fields import validate_allowed_user_ids


def _iter_options():
    user_id_0 = 202604060010
    user_id_1 = 202604060011
    
    user_0 = User.precreate(
        user_id_0,
    )
    
    user_1 = User.precreate(
        user_id_1,
    )
    
    yield (
        None,
        set(),
    )
    
    yield (
        [],
        set(),
    )
    
    yield (
        [
            user_id_0,
            user_id_1,
        ],
        {
            user_id_0,
            user_id_1,
        },
    )
    
    yield (
        [
            user_0,
            user_1,
        ],
        {
            user_id_0,
            user_id_1,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_allowed_user_ids(input_value):
    """
    Tests whether ``validate_allowed_user_ids`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to validate.
    
    Returns
    -------
    output : `set<int>`
    """
    output = validate_allowed_user_ids(input_value)
    
    vampytest.assert_instance(output, set)
    for element in output:
        vampytest.assert_instance(element, int)
    
    return output
