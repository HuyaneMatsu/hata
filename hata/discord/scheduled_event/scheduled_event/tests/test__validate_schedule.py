import vampytest

from ...schedule import Schedule

from ..fields import validate_schedule


def _iter_options__passing():
    schedule = Schedule(occurrence_spacing = 2)
    
    yield None, None
    yield schedule, schedule


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_schedule(input_value):
    """
    Tests whether ``validate_schedule`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `None | Schedule`
    
    Raises
    ------
    TypeError
    """
    output = validate_schedule(input_value)
    vampytest.assert_instance(output, Schedule, nullable = True)
    return output
