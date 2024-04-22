import vampytest

from ....activity import Activity, ActivityType

from ..fields import validate_activity


def _iter_options__passing():
    activity = Activity('tsuki', activity_type = ActivityType.competing)
    
    yield activity, activity


def _iter_options__type_error():
    yield 12.6
    yield None


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_activity__passing(input_value):
    """
    Tests whether `validate_activity` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to test with.
    
    Returns
    -------
    output : ``Activity``
    
    Raises
    ------
    TypeError
    """
    return validate_activity(input_value)
