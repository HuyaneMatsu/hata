import vampytest

from ...poll_answer import PollAnswer

from ..fields import put_answers_into


def _iter_options():
    answer_0 = PollAnswer.precreate(202404140006, text = 'hey')
    answer_1 = PollAnswer.precreate(202404140007, text = 'mister')
    
    yield (
        None,
        False,
        {
            'answers': []
        },
    )
    
    yield (
        None,
        True,
        {
            'answers': []
        },
    )
    
    yield (
        (answer_0, answer_1),
        False,
        {
            'answers': [
                answer_0.to_data(defaults = False, include_internals = True),
                answer_1.to_data(defaults = False, include_internals = True),
            ]
        },
    )
    
    yield (
        (answer_0, answer_1),
        True,
        {
            'answers': [
                answer_0.to_data(defaults = True, include_internals = True),
                answer_1.to_data(defaults = True, include_internals = True),
            ]
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_answers_into(input_value, defaults):
    """
    Tests whether ``put_answers_into`` works as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<PollAnswer>`
        Value to serialise.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------    
    output : `dict<str, object>`
    """
    return put_answers_into(input_value, {}, defaults, include_internals = True)
