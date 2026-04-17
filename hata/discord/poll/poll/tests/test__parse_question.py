import vampytest

from ...poll_question import PollQuestion

from ..fields import parse_question


def _iter_options():
    question = PollQuestion(text = 'hey mister')
    
    yield {}, None
    yield {'question': None}, None
    yield {'question': question.to_data(include_internals = True)}, question


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_question(input_data):
    """
    Tests whether ``parse_question`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | PollQuestion`
    """
    output = parse_question(input_data)
    vampytest.assert_instance(output, PollQuestion, nullable = True)
    return output
