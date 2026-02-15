from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..fields import validate_occasion_counts


def _iter_options__passing():
    date_time = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield (
        None,
        None,
    )
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            date_time : 5,
        },
        {
            date_time : 5,
        },
    )


def _iter_options__type_error():
    date_time = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield 12.6
    yield '12'
    yield {'nyan' : 6}
    yield {date_time : 'nyan'}


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_occasion_counts(input_value):
    """
    Tests whether `validate_occasion_counts` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `None | dict<Datetime, int>`
    
    Raises
    ------
    TypeError
    """
    output = validate_occasion_counts(input_value)
    vampytest.assert_instance(output, dict, nullable = True)
    if (output is not None):
        for key, value in output.items():
            vampytest.assert_instance(key, DateTime)
            vampytest.assert_instance(value, int)
    
    return output
