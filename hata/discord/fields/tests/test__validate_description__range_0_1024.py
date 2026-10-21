import vampytest

from ..fields_common import validate_description__range_0_1024


def _iter_options__passing():
    yield None, None
    yield '', None
    yield 'a', 'a'


def _iter_options__type_error():
    yield 12.6


def _iter_options__value_error():
    yield 'a' * (1024 + 1)


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_description__range_0_1024(input_value):
    output = validate_description__range_0_1024(input_value)
    vampytest.assert_instance(output, str, nullable = True)
    return output
