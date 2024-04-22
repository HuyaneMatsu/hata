from datetime import datetime as DateTime

import vampytest

from ...poll_answer import PollAnswer
from ...poll_question import PollQuestion
from ...poll_result import PollResult

from ..poll import Poll
from ..preinstanced import PollLayout


def test__Poll__repr():
    """
    Tests whether ``Poll.__repr__`` works as intended.
    """
    allow_multiple_choices = True
    answers = [
        PollAnswer.precreate(202404140030, text = 'hey'),
        PollAnswer.precreate(202404140031, text = 'mister'),
    ]
    duration = 7200
    expires_at = DateTime(2016, 5, 14)
    finalized = True
    layout = PollLayout.default
    question = PollQuestion(text = 'wanna play')
    results = [
        PollResult(answer_id = 202404140063),
        PollResult(answer_id = 202404140064),
    ]
    
    poll = Poll(
        allow_multiple_choices = allow_multiple_choices,
        answers = answers,
        duration = duration,
        expires_at = expires_at,
        finalized = finalized,
        layout = layout,
        question = question,
        results = results,
    )
    vampytest.assert_instance(repr(poll), str)


def test__Poll__hash():
    """
    Tests whether ``Poll.__hash__`` works as intended.
    """
    allow_multiple_choices = True
    answers = [
        PollAnswer.precreate(202404140032, text = 'hey'),
        PollAnswer.precreate(202404140033, text = 'mister'),
    ]
    duration = 7200
    expires_at = DateTime(2016, 5, 14)
    finalized = True
    layout = PollLayout.default
    question = PollQuestion(text = 'wanna play')
    results = [
        PollResult(answer_id = 202404140065),
        PollResult(answer_id = 202404140066),
    ]
    
    poll = Poll(
        allow_multiple_choices = allow_multiple_choices,
        answers = answers,
        duration = duration,
        expires_at = expires_at,
        finalized = finalized,
        layout = layout,
        question = question,
        results = results,
    )
    vampytest.assert_instance(hash(poll), int)


def test__Poll__eq():
    """
    Tests whether ``Poll.__eq__`` works as intended.
    """
    allow_multiple_choices = True
    answers = [
        PollAnswer.precreate(202404140034, text = 'hey'),
        PollAnswer.precreate(202404140035, text = 'mister'),
    ]
    duration = 7200
    expires_at = DateTime(2016, 5, 14)
    finalized = True
    layout = PollLayout.default
    question = PollQuestion(text = 'wanna play')
    results = [
        PollResult(answer_id = 202404140067),
        PollResult(answer_id = 202404140068),
    ]
    
    keyword_parameters = {
        'allow_multiple_choices': allow_multiple_choices,
        'answers': answers,
        'duration': duration,
        'expires_at': expires_at,
        'finalized': finalized,
        'layout': layout,
        'question': question,
        'results': results,
    }
    
    poll = Poll(**keyword_parameters)
    
    vampytest.assert_eq(poll, poll)
    vampytest.assert_ne(poll, object())
    
    for poll_name, poll_value in (
        ('allow_multiple_choices', False),
        ('answers', None),
        ('duration', 3600),
        ('expires_at', None),
        ('finalized', False),
        ('layout', PollLayout.none),
        ('question', None),
        ('results', None),
    ):
        test_poll = Poll(**{**keyword_parameters, poll_name: poll_value})
        vampytest.assert_ne(poll, test_poll)


def _iter_options__bool():
    allow_multiple_choices = True
    answers = [
        PollAnswer.precreate(202404140036, text = 'hey'),
        PollAnswer.precreate(202404140037, text = 'mister'),
    ]
    duration = 7200
    expires_at = DateTime(2016, 5, 14)
    finalized = True
    layout = PollLayout.default
    question = PollQuestion(text = 'wanna play')
    results = [
        PollResult(answer_id = 202404140069),
        PollResult(answer_id = 202404140070),
    ]
    
    yield {}, False
    yield {'allow_multiple_choices': allow_multiple_choices}, True
    yield {'answers': answers}, True
    yield {'duration': duration}, True
    yield {'expires_at': expires_at}, True
    yield {'finalized': finalized}, True
    yield {'layout': layout}, False
    yield {'layout': PollLayout.none}, False
    yield {'question': question}, True
    yield {'results': results}, False


@vampytest._(vampytest.call_from(_iter_options__bool()).returning_last())
def test__Poll__bool(keyword_parameters):
    """
    Tests whether ``Poll.__bool__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the poll question with.
    
    Returns
    -------
    output : `bool`
    """
    poll = Poll(**keyword_parameters)
    output = bool(poll)
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__len():
    allow_multiple_choices = True
    answers = [
        PollAnswer.precreate(202404140038, text = 'hey'),
        PollAnswer.precreate(202404140039, text = 'mister'),
    ]
    duration = 7200
    expires_at = DateTime(2016, 5, 14)
    finalized = True
    layout = PollLayout.default
    question = PollQuestion(text = 'wanna play')
    results = [
        PollResult(answer_id = 202404140071),
        PollResult(answer_id = 202404140072),
    ]
    
    yield {}, 0
    yield {'allow_multiple_choices': allow_multiple_choices}, 0
    yield {'answers': answers}, sum(len(answer) for answer in answers)
    yield {'duration': duration}, 0
    yield {'expires_at': expires_at}, 0
    yield {'finalized': finalized}, 0
    yield {'layout': layout}, 0
    yield {'question': question}, len(question)
    yield {'results': results}, 0


@vampytest._(vampytest.call_from(_iter_options__len()).returning_last())
def test__Poll__len(keyword_parameters):
    """
    Tests whether ``Poll.__len__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the poll question with.
    
    Returns
    -------
    output : `int`
    """
    poll = Poll(**keyword_parameters)
    output = len(poll)
    vampytest.assert_instance(output, int)
    return output


def _iter_options__get_item__passing():
    answer_0 = PollAnswer.precreate(202404170026, text = 'hey')
    answer_1 = PollAnswer.precreate(202404170027, text = 'mister')
    answer_2 = PollAnswer(text = 'mister')
    result_0 = PollResult(answer_id = 202404170026, count = 2)
    result_1 = PollResult(answer_id = 202404170027, count = 3)
    
    yield [answer_0, answer_1], [result_0, result_1], answer_0, result_0
    yield [answer_0, answer_1], [result_0, result_1], answer_1, result_1
    yield [answer_0, answer_1], [result_1], answer_0, None
    yield [answer_0, answer_1], [result_0], answer_1, None
    yield [answer_0, answer_1], [result_0, result_1], answer_2, result_1
    yield [answer_1], [result_1], answer_2, result_1
    yield [answer_0], [result_0], answer_2, None
    yield [answer_0, answer_1], None, answer_0, None
    yield None, None, answer_1, None
    yield [answer_1], [result_1], answer_1.id, result_1


def _iter_options__get_item__type_error():
    yield None, None, 12.6


@vampytest._(vampytest.call_from(_iter_options__get_item__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__get_item__type_error()).raising(TypeError))
def test__Poll__get_item(answers, results, key):
    """
    Tests whether ``Poll.__getitem__`` works as intended.
    
    Parameters
    ----------
    answers : `None | list<PollAnswer>`
        Poll answers to create the poll with.
    results : `None | list<PollResult>`
        Poll results to create the poll with.
    key : `PollAnswer | int | object`
        Key to get the results for.
    
    Returns
    -------
    results : `None | PollResult`
    """
    poll = Poll(answers = answers, results = results)
    output =  poll[key]
    vampytest.assert_instance(output, PollResult, nullable = True)
    return output
