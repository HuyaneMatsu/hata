from datetime import datetime as DateTime, timedelta as TimeDelta

import vampytest

from ..fields import validate_invites_disabled_duration


class DateTimeMock(DateTime):
    current_date_time = None
    
    @classmethod
    def set_current(cls, value):
        cls.current_date_time = value
    
    @classmethod
    def utcnow(cls):
        value = cls.current_date_time
        if value is None:
            value = DateTime.utcnow()
        return value


def _iter_options():
    current_date = DateTime(2016, 5, 14)
    
    yield current_date, 0, None
    yield current_date, -1, None
    yield current_date, +1, current_date + TimeDelta(seconds = 1)
    
    
    yield current_date, TimeDelta(), None
    yield current_date, TimeDelta(seconds = -1), None
    yield current_date, TimeDelta(seconds = +1), current_date + TimeDelta(seconds = 1)
    
    yield current_date, 0.0, None
    yield current_date, -1.0, None
    yield current_date, +1.0, current_date + TimeDelta(seconds = 1)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_invites_disabled_duration__passing(current_date, input_value):
    """
    Tests whether ``validate_invites_disabled_duration`` works as intended.
    
    Case: Passing.
    
    Parameters
    ----------
    current_date : `DateTime`
        Current date to use.
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `None | DateTime`
    """
    DateTimeMock.set_current(current_date)
    mocked = vampytest.mock_globals(validate_invites_disabled_duration, DateTime = DateTimeMock)
    return mocked(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(None)
@vampytest.call_with('Orin')
def test__validate_invites_disabled_duration__type_error(input_value):
    """
    Tests whether ``validate_invites_disabled_duration`` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_invites_disabled_duration(input_value)
