import vampytest

from ....user import User

from ...embedded_activity_user_state import EmbeddedActivityUserState

from ..fields import validate_user_states


def _iter_options__passing():
    user_id_0 = 202409010096
    user_id_1 = 202409010097
    
    embedded_activity_user_state_0 = EmbeddedActivityUserState(user = User.precreate(user_id_0, name = 'Koishi'))
    embedded_activity_user_state_1 = EmbeddedActivityUserState(user = User.precreate(user_id_1, name = 'Satori'))
    
    yield None, {}
    yield [], {}
    yield {}, {}
    yield [embedded_activity_user_state_0], {user_id_0: embedded_activity_user_state_0}
    yield {user_id_0: embedded_activity_user_state_0}, {user_id_0: embedded_activity_user_state_0}
    yield (
        [embedded_activity_user_state_0, embedded_activity_user_state_1],
        {user_id_0: embedded_activity_user_state_0, user_id_1: embedded_activity_user_state_1},
    )


def _iter_options__type_error():
    yield 12.6
    yield [12.6]
    yield {12.6: 12.6}


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_user_states(input_value):
    """
    Tests whether ``validate_user_states`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `dict<int, EmbeddedActivityUserState>`
    
    Raises
    ------
    TypeError
    """
    output = validate_user_states(input_value)
    vampytest.assert_instance(output, dict)
    return output
