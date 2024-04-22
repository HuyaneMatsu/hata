import vampytest

from ...poll_question import PollQuestion

from ..fields import validate_question


def _iter_options__passing():
    question = PollQuestion(text = 'hey mister')
    
    yield None, None
    yield question, question
    yield question.text, question


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_question(input_value):
    """
    Tests whether `validate_question` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `None | PollQuestion`
    
    Raises
    ------
    TypeError
    """
    return validate_question(input_value)
