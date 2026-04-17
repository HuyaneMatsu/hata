from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...poll_answer import PollAnswer
from ...poll_question import PollQuestion
from ...poll_result import PollResult

from ..poll import Poll
from ..preinstanced import PollLayout


def _assert_fields_set(poll):
    """
    Checks whether the poll has every of its fields set.
    
    Parameters
    ----------
    poll : ``Poll``
        The poll to check.
    """
    vampytest.assert_instance(poll, Poll)
    vampytest.assert_instance(poll.allow_multiple_choices, bool)
    vampytest.assert_instance(poll.answers, tuple, nullable = True)
    vampytest.assert_instance(poll.duration, int)
    vampytest.assert_instance(poll.expires_at, DateTime, nullable = True)
    vampytest.assert_instance(poll.finalized, bool)
    vampytest.assert_instance(poll.layout, PollLayout)
    vampytest.assert_instance(poll.question, PollQuestion, nullable = True)
    vampytest.assert_instance(poll.results, list, nullable = True)


def test__Poll__new__no_fields():
    """
    Tests whether ``Poll.__new__`` works as intended.
    
    Case: No fields given.
    """
    poll = Poll()
    _assert_fields_set(poll)


def test__Poll__new__all_fields():
    """
    Tests whether ``Poll.__new__`` works as intended.
    
    Case: All fields given.
    """
    allow_multiple_choices = True
    answers = [
        PollAnswer.precreate(202404140022, text = 'hey'),
        PollAnswer.precreate(202404140023, text = 'mister'),
    ]
    duration = 7200
    expires_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    finalized = True
    layout = PollLayout.default
    question = PollQuestion(text = 'wanna play')
    results = [
        PollResult(answer_id = 202404140054),
        PollResult(answer_id = 202404140055),
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
    _assert_fields_set(poll)
    
    vampytest.assert_eq(poll.allow_multiple_choices, allow_multiple_choices)
    vampytest.assert_eq(poll.answers, tuple(answers))
    vampytest.assert_eq(poll.duration, duration)
    vampytest.assert_eq(poll.expires_at, expires_at)
    vampytest.assert_eq(poll.finalized, finalized)
    vampytest.assert_is(poll.layout, layout)
    vampytest.assert_eq(poll.question, question)
    vampytest.assert_eq(poll.results, results)


def test__Poll__create_empty():
    """
    Tests whether ``Poll._create_empty`` works as intended.
    """
    poll = Poll._create_empty()
    _assert_fields_set(poll)
