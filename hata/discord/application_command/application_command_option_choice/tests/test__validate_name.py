from enum import Enum

import vampytest

from ..constants import NAME_LENGTH_MAX
from ..fields import validate_name


class TestEnum(Enum):
    ayaya = 'owo'


def _iter_options():
    yield None, ''
    yield '', ''
    yield 'a', 'a'
    yield 'aa', 'aa'


def _iter_options__passing():
    yield None, ''
    yield '', ''
    yield 'a', 'a'
    yield 'aa', 'aa'
    yield TestEnum.ayaya, 'ayaya'


def _iter_options__type_error():
    yield 12.6


def _iter_options__value_error():
    yield 'a' * (NAME_LENGTH_MAX + 1)


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_name(input_value):
    """
    Tests whether `validate_name` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `str`
    
    Raises
    ------
    TypeError
    """
    return validate_name(input_value)
