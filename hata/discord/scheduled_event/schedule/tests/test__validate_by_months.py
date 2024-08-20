import vampytest

from ..fields import validate_by_months
from ..preinstanced import ScheduleMonth


def _iter_options__passing():
    yield None, None
    yield [], None
    yield ScheduleMonth.january, (ScheduleMonth.january, )
    yield ScheduleMonth.january.value, (ScheduleMonth.january, )
    yield [ScheduleMonth.january], (ScheduleMonth.january, )
    yield [ScheduleMonth.january.value], (ScheduleMonth.january, )
    yield (
        [ScheduleMonth.january, ScheduleMonth.august],
        (ScheduleMonth.january, ScheduleMonth.august,),
    )
    yield (
        [ScheduleMonth.august, ScheduleMonth.january],
        (ScheduleMonth.january, ScheduleMonth.august,),
    )


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_by_months(input_value):
    """
    Tests whether `validate_by_months` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `None | tuple<ScheduleMonth>`
    
    Raises
    ------
    TypeError
    """
    return validate_by_months(input_value)
