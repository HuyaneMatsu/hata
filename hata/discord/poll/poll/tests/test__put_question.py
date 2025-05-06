import vampytest

from ...poll_question import PollQuestion

from ..fields import put_question


def _iter_options():
    question = PollQuestion(text = 'hey mister')
    
    yield None, False, {'question': None}
    yield None, True, {'question': None}
    yield question, False, {'question': question.to_data(defaults = False, include_internals = True)}
    yield question, True, {'question': question.to_data(defaults = True, include_internals = True)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_question(input_value, defaults):
    """
    Tests whether ``put_question`` works as intended.
    
    Parameters
    ----------
    input_value : `None | PollQuestion`
        The value to serialise.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_question(input_value, {}, defaults, include_internals = True)
