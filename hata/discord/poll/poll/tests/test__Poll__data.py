from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_timestamp

from ...poll_answer import PollAnswer
from ...poll_question import PollQuestion
from ...poll_result import PollResult

from ..poll import Poll
from ..preinstanced import PollLayout

from .test__Poll__constructor import _assert_fields_set


def test__Poll__from_data():
    """
    Tests whether ``Poll.from_data`` works as intended.
    """
    allow_multiple_choices = True
    answers = [
        PollAnswer.precreate(202404140024, text = 'hey'),
        PollAnswer.precreate(202404140025, text = 'mister'),
    ]
    duration = 7200
    expires_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    finalized = True
    layout = PollLayout.default
    question = PollQuestion(text = 'wanna play')
    results = [
        PollResult(answer_id = 202404140056),
        PollResult(answer_id = 202404140057),
    ]
    
    data = {
        'allow_multiselect': allow_multiple_choices,
        'answers': [answer.to_data(defaults = True, include_internals = True) for answer in answers],
        'duration': duration // 3600,
        'expiry': datetime_to_timestamp(expires_at),
        'layout_type': layout.value,
        'question': question.to_data(defaults = True),
        'results': {
            'answer_counts': [result.to_data() for result in results],
            'is_finalized': finalized,
        },
    }
    
    poll = Poll.from_data(data)
    _assert_fields_set(poll)
    
    vampytest.assert_eq(poll.allow_multiple_choices, allow_multiple_choices)
    vampytest.assert_eq(poll.answers, tuple(answers))
    vampytest.assert_eq(poll.duration, duration)
    vampytest.assert_eq(poll.expires_at, expires_at)
    vampytest.assert_eq(poll.finalized, finalized)
    vampytest.assert_is(poll.layout, layout)
    vampytest.assert_eq(poll.results, results)


def test__Poll__to_data__include_internals():
    """
    Tests whether ``Poll.to_data`` works as intended.
    
    Case: Include defaults & internals.
    """
    allow_multiple_choices = True
    answers = [
        PollAnswer.precreate(202404140026, text = 'hey'),
        PollAnswer.precreate(202404140027, text = 'mister'),
    ]
    duration = 7200
    expires_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    finalized = True
    layout = PollLayout.default
    question = PollQuestion(text = 'wanna play')
    results = [
        PollResult(answer_id = 202404140058),
        PollResult(answer_id = 202404140059),
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
    
    expected_output = {
        'allow_multiselect': allow_multiple_choices,
        'answers': [answer.to_data(defaults = True, include_internals = True) for answer in answers],
        'expiry': datetime_to_timestamp(expires_at),
        'layout_type': layout.value,
        'question': question.to_data(defaults = True),
        'results': {
            'answer_counts': [result.to_data() for result in results],
            'is_finalized': finalized,
        },
    }
    
    vampytest.assert_eq(
        poll.to_data(defaults = True, include_internals = True),
        expected_output,
    )


def test__Poll__to_data__exclude_internals():
    """
    Tests whether ``Poll.to_data`` works as intended.
    
    Case: Exclude internals.
    """
    allow_multiple_choices = True
    answers = [
        PollAnswer.precreate(202404140028, text = 'hey'),
        PollAnswer.precreate(202404140029, text = 'mister'),
    ]
    duration = 7200
    expires_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    finalized = True
    layout = PollLayout.default
    question = PollQuestion(text = 'wanna play')
    results = [
        PollResult(answer_id = 202404140060),
        PollResult(answer_id = 202404140061),
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
    
    expected_output = {
        'allow_multiselect': allow_multiple_choices,
        'answers': [answer.to_data(defaults = True) for answer in answers],
        'duration': duration // 3600,
        'layout_type': layout.value,
        'question': question.to_data(defaults = True),
    }
    
    vampytest.assert_eq(
        poll.to_data(defaults = True, include_internals = False),
        expected_output,
    )


def test__Poll__update_attributes():
    """
    Tests whether ``Poll._update_attributes`` works as intended.
    """
    old_allow_multiple_choices = True
    old_answers = [
        PollAnswer.precreate(202404170005, text = 'hey'),
        PollAnswer.precreate(202404170006, text = 'mister'),
    ]
    old_duration = 7200
    old_expires_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    old_finalized = True
    old_layout = PollLayout.default
    old_question = PollQuestion(text = 'wanna play')
    old_results = [
        PollResult(answer_id = 202404170007),
        PollResult(answer_id = 202404170008),
    ]
    
    new_allow_multiple_choices = False
    new_answers = [
        PollAnswer.precreate(202404170009, text = 'hey'),
        PollAnswer.precreate(202404170010, text = 'sister'),
    ]
    new_duration = 3600
    new_expires_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    new_finalized = False
    new_layout = PollLayout.none
    new_question = PollQuestion(text = 'wanna wake up')
    new_results = [
        PollResult(answer_id = 202404170011),
        PollResult(answer_id = 202404170012),
    ]
    
    poll = Poll(
        allow_multiple_choices = old_allow_multiple_choices,
        answers = old_answers,
        duration = old_duration,
        expires_at = old_expires_at,
        finalized = old_finalized,
        layout = old_layout,
        question = old_question,
        results = old_results,
    )
    
    data = {
        'allow_multiselect': new_allow_multiple_choices,
        'answers': [answer.to_data(defaults = True, include_internals = True) for answer in new_answers],
        'duration': new_duration // 3600,
        'expiry': datetime_to_timestamp(new_expires_at),
        'layout_type': new_layout.value,
        'question': new_question.to_data(defaults = True),
        'results': {
            'answer_counts': [result.to_data() for result in new_results],
            'is_finalized': new_finalized,
        },
    }
    
    poll._update_attributes(data)
    
    vampytest.assert_eq(poll.allow_multiple_choices, new_allow_multiple_choices)
    vampytest.assert_eq(poll.answers, tuple(new_answers))
    vampytest.assert_eq(poll.duration, new_duration)
    vampytest.assert_eq(poll.expires_at, new_expires_at)
    vampytest.assert_eq(poll.finalized, new_finalized)
    vampytest.assert_is(poll.layout, new_layout)
    vampytest.assert_eq(poll.results, new_results)


def test__Poll__difference_update_attributes():
    """
    Tests whether ``Poll._difference_update_attributes`` works as intended.
    """
    old_allow_multiple_choices = True
    old_answers = [
        PollAnswer.precreate(202404170013, text = 'hey'),
        PollAnswer.precreate(202404170014, text = 'mister'),
    ]
    old_duration = 7200
    old_expires_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    old_finalized = True
    old_layout = PollLayout.default
    old_question = PollQuestion(text = 'wanna play')
    old_results = [
        PollResult(answer_id = 202404170015),
        PollResult(answer_id = 202404170016),
    ]
    
    new_allow_multiple_choices = False
    new_answers = [
        PollAnswer.precreate(202404170017, text = 'hey'),
        PollAnswer.precreate(202404170018, text = 'sister'),
    ]
    new_duration = 3600
    new_expires_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    new_finalized = False
    new_layout = PollLayout.none
    new_question = PollQuestion(text = 'wanna wake up')
    new_results = [
        PollResult(answer_id = 202404170019),
        PollResult(answer_id = 202404170020),
    ]
    
    poll = Poll(
        allow_multiple_choices = old_allow_multiple_choices,
        answers = old_answers,
        duration = old_duration,
        expires_at = old_expires_at,
        finalized = old_finalized,
        layout = old_layout,
        question = old_question,
        results = old_results,
    )
    
    data = {
        'allow_multiselect': new_allow_multiple_choices,
        'answers': [answer.to_data(defaults = True, include_internals = True) for answer in new_answers],
        'duration': new_duration // 3600,
        'expiry': datetime_to_timestamp(new_expires_at),
        'layout_type': new_layout.value,
        'question': new_question.to_data(defaults = True),
        'results': {
            'answer_counts': [result.to_data() for result in new_results],
            'is_finalized': new_finalized,
        },
    }
    
    old_attributes = poll._difference_update_attributes(data)
    
    vampytest.assert_eq(poll.allow_multiple_choices, new_allow_multiple_choices)
    vampytest.assert_eq(poll.answers, tuple(new_answers))
    vampytest.assert_eq(poll.duration, new_duration)
    vampytest.assert_eq(poll.expires_at, new_expires_at)
    vampytest.assert_eq(poll.finalized, new_finalized)
    vampytest.assert_is(poll.layout, new_layout)
    vampytest.assert_eq(poll.results, new_results)
    
    vampytest.assert_eq(
        old_attributes,
        {
            'allow_multiple_choices': old_allow_multiple_choices,
            'answers': tuple(old_answers),
            'duration': old_duration,
            'expires_at': old_expires_at,
            'layout': old_layout,
            'question': old_question,
            # 'results': old_results,
            'finalized': old_finalized,
        },
    )
