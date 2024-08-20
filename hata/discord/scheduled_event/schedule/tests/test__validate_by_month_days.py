import vampytest

from ..fields import validate_by_month_days


def _iter_options__passing():
    yield None, None
    yield [], None
    yield 1, (1, )
    yield [1], (1, )
    yield (
        [1, 2],
        (1, 2,),
    )
    yield (
        [2, 1],
        (1, 2,),
    )


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


def _iter_options__value_error():
    yield [0]
    yield [32]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_by_month_days(input_value):
    """
    Tests whether `validate_by_month_days` works as intended.
    
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
    ValueError
    """
    return validate_by_month_days(input_value)
