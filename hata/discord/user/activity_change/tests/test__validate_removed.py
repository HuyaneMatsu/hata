import vampytest

from ....activity import Activity, ActivityType

from ..fields import validate_removed


def _iter_options__passing():
    activity = Activity('tsuki', activity_type = ActivityType.competing)
    
    yield None, None
    yield [], None
    yield [activity], [activity]


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_removed(input_value):
    """
    Tests whether `validate_removed` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to test with.
    
    Returns
    -------
    output : `None | list<Activity>`
    
    Raises
    ------
    TypeError
    """
    return validate_removed(input_value)
