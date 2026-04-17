import vampytest

from ...poll_answer import PollAnswer

from ..fields import parse_answers


def _iter_options():
    answer_0 = PollAnswer.precreate(202404140002, text = 'hey')
    answer_1 = PollAnswer.precreate(202404140003, text = 'mister')
    
    yield {}, None
    yield {'answers': None}, None
    yield {'answers': []}, None
    yield (
        {
            'answers': [
                answer_0.to_data(defaults = True, include_internals = True),
            ],
        },
        (answer_0, ),
    )
    yield (
        {
            'answers': [
                answer_0.to_data(defaults = True, include_internals = True),
                answer_1.to_data(defaults = True, include_internals = True),
            ],
        },
        (answer_0, answer_1),
    )
    yield (
        {
            'answers': [
                answer_1.to_data(defaults = True, include_internals = True),
                answer_0.to_data(defaults = True, include_internals = True),
            ],
        },
        (answer_1, answer_0),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_answers(input_data):
    """
    Tests whether ``parse_answers`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `none | tuple<PollAnswer>`
    """
    return parse_answers(input_data)
