import vampytest

from ...poll_result import PollResult

from ..fields import validate_results


def _iter_options__passing():
    result_0 = PollResult(answer_id = 202404140020)
    result_1 = PollResult(answer_id = 202404140021)
    
    yield None, None
    yield [], None
    yield [result_0], [result_0]
    yield [result_0, result_0], [result_0, result_0]
    yield [result_0, result_1], [result_0, result_1]
    yield [result_1, result_0], [result_1, result_0]


def _iter_options__type_error():
    yield 2.3
    yield [2.3]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_results(input_value):
    """
    Tests whether ``validate_results`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | list<PollResult>`
    """
    return validate_results(input_value)
