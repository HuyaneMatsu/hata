import vampytest

from ...poll_answer import PollAnswer

from ..fields import validate_answers


def _iter_options__passing():
    answer_0 = PollAnswer.precreate(202404140010, text = 'hey')
    answer_1 = PollAnswer.precreate(202404140011, text = 'mister')
    
    yield None, None
    yield [], None
    yield [answer_0], (answer_0,)
    yield [answer_0, answer_0], (answer_0, answer_0)
    yield [answer_0, answer_1], (answer_0, answer_1)
    yield [answer_1, answer_0], (answer_1, answer_0)


def _iter_options__type_error():
    yield 2.3
    yield [2.3]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_answers(input_value):
    """
    Tests whether ``validate_answers`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | tuple<PollAnswer>`
    """
    return validate_answers(input_value)
