import vampytest

from ..poll_question import PollQuestion


def test__PollQuestion__repr():
    """
    Tests whether ``PollQuestion.__repr__`` works as intended.
    """
    text = 'orin'
    
    poll_question = PollQuestion(text = text)
    vampytest.assert_instance(repr(poll_question), str)


def test__PollQuestion__hash():
    """
    Tests whether ``PollQuestion.__hash__`` works as intended.
    """
    text = 'orin'
    
    poll_question = PollQuestion(text = text)
    vampytest.assert_instance(hash(poll_question), int)


def test__PollQuestion__eq():
    """
    Tests whether ``PollQuestion.__eq__`` works as intended.
    """
    text = 'orin'
    
    keyword_parameters = {
        'text': text,
    }
    
    poll_question = PollQuestion(**keyword_parameters)
    
    vampytest.assert_eq(poll_question, poll_question)
    vampytest.assert_ne(poll_question, object())
    
    for poll_question_name, poll_question_value in (
        ('text', 'rin'),
    ):
        test_poll_question = PollQuestion(**{**keyword_parameters, poll_question_name: poll_question_value})
        vampytest.assert_ne(poll_question, test_poll_question)


def _iter_options__bool():
    text = 'orin'
    
    yield {}, False
    yield {'text': text}, True


@vampytest._(vampytest.call_from(_iter_options__bool()).returning_last())
def test__PollQuestion__bool(keyword_parameters):
    """
    Tests whether ``PollQuestion.__bool__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the poll question with.
    
    Returns
    -------
    output : `bool`
    """
    poll_question = PollQuestion(**keyword_parameters)
    output = bool(poll_question)
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__len():
    text = 'orin'
    
    yield {}, 0
    yield {'text': text}, len(text)


@vampytest._(vampytest.call_from(_iter_options__len()).returning_last())
def test__PollQuestion__len(keyword_parameters):
    """
    Tests whether ``PollQuestion.__len__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the poll question with.
    
    Returns
    -------
    output : `int`
    """
    poll_question = PollQuestion(**keyword_parameters)
    output = len(poll_question)
    vampytest.assert_instance(output, int)
    return output
