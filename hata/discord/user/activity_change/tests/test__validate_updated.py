import vampytest

from ....activity import Activity, ActivityType

from ...activity_update import ActivityUpdate

from ..fields import validate_updated


def _iter_options__passing():
    activity = Activity('tsuki', activity_type = ActivityType.competing)
    activity_update = ActivityUpdate(activity = activity, old_attributes = {'a': 'b'})
    
    yield None, None
    yield [], None
    yield [activity_update], [activity_update]


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_updated(input_value):
    """
    Tests whether `validate_updated` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value to test with.
    
    Returns
    -------
    output : `None | list<ActivityUpdate>`
    
    Raises
    ------
    TypeError
    """
    return validate_updated(input_value)
