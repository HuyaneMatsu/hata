from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....user import User

from ...poll_answer import PollAnswer
from ...poll_question import PollQuestion
from ...poll_result import PollResult

from ..poll import Poll
from ..preinstanced import PollLayout

from .test__Poll__constructor import _assert_fields_set


def test__Poll__clean_copy():
    """
    Tests whether ``Poll.clean_copy`` works as intended.
    """
    user = User.precreate(202404140015, name = 'koishi')
    
    allow_multiple_choices = True
    answers = [
        PollAnswer.precreate(202404140041, text = user.mention),
    ]
    duration = 7200
    expires_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    finalized = True
    layout = PollLayout.default
    question = PollQuestion(text = 'wanna play')
    results = [
        PollResult(answer_id = 202404140073),
        PollResult(answer_id = 202404140077),
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
    copy = poll.clean_copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(poll, copy)
    
    vampytest.assert_eq(copy.allow_multiple_choices, allow_multiple_choices)
    vampytest.assert_eq(copy.answers, (PollAnswer(text = f'@{user.name!s}'),))
    vampytest.assert_eq(copy.duration, duration)
    


def test__Poll__copy():
    """
    Tests whether ``Poll.copy`` works as intended.
    """
    allow_multiple_choices = True
    answers = [
        PollAnswer.precreate(202404140042, text = 'hey'),
        PollAnswer.precreate(202404140043, text = 'mister'),
    ]
    duration = 7200
    expires_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    finalized = True
    layout = PollLayout.default
    question = PollQuestion(text = 'wanna play')
    results = [
        PollResult(answer_id = 202404140075),
        PollResult(answer_id = 202404140076),
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
    copy = poll.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(poll, copy)
    
    vampytest.assert_eq(poll, copy)


def test__Poll__copy_with__no_fields():
    """
    Tests whether ``Poll.copy_with`` works as intended.
    
    Case: No fields given.
    """
    allow_multiple_choices = True
    answers = [
        PollAnswer.precreate(202404140044, text = 'hey'),
        PollAnswer.precreate(202404140045, text = 'mister'),
    ]
    duration = 7200
    expires_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    finalized = True
    layout = PollLayout.default
    question = PollQuestion(text = 'wanna play')
    results = [
        PollResult(answer_id = 202404140077),
        PollResult(answer_id = 202404140078),
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
    copy = poll.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(poll, copy)
    
    vampytest.assert_eq(poll, copy)


def test__Poll__copy_with__all_fields():
    """
    Tests whether ``Poll.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_allow_multiple_choices = True
    old_answers = [
        PollAnswer.precreate(202404140046, text = 'hey'),
        PollAnswer.precreate(202404140047, text = 'mister'),
    ]
    old_duration = 7200
    old_expires_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    old_finalized = True
    old_layout = PollLayout.default
    old_question = PollQuestion(text = 'wanna play')
    old_results = [
        PollResult(answer_id = 202404140079),
        PollResult(answer_id = 202404140080),
    ]
    
    new_allow_multiple_choices = False
    new_answers = [
        PollAnswer.precreate(202404140048, text = 'orin'),
        PollAnswer.precreate(202404140049, text = 'carting'),
    ]
    new_duration = 3600
    new_expires_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    new_finalized = False
    new_layout = PollLayout.none
    new_question = PollQuestion(text = 'magic farm')
    new_results = [
        PollResult(answer_id = 202404140081),
        PollResult(answer_id = 202404140082),
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
    copy = poll.copy_with(
        allow_multiple_choices = new_allow_multiple_choices,
        answers = new_answers,
        duration = new_duration,
        expires_at = new_expires_at,
        finalized = new_finalized,
        layout = new_layout,
        question = new_question,
        results = new_results,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(poll, copy)
    
    vampytest.assert_eq(copy.allow_multiple_choices, new_allow_multiple_choices)
    vampytest.assert_eq(copy.answers, tuple(new_answers))
    vampytest.assert_eq(copy.duration, new_duration)
    vampytest.assert_eq(copy.expires_at, new_expires_at)
    vampytest.assert_eq(copy.finalized, new_finalized)
    vampytest.assert_eq(copy.layout, new_layout)
    vampytest.assert_eq(copy.question, new_question)
    vampytest.assert_eq(copy.results, new_results)


def _iter_options__contents():
    allow_multiple_choices = True
    answers = [
        PollAnswer.precreate(202404140050, text = 'hey'),
        PollAnswer.precreate(202404140051, text = 'mister'),
    ]
    duration = 7200
    expires_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    finalized = True
    layout = PollLayout.default
    question = PollQuestion(text = 'wanna play')
    results = [
        PollResult(answer_id = 202404140083),
        PollResult(answer_id = 202404140084),
    ]
    
    yield {}, set()
    yield {'allow_multiple_choices': allow_multiple_choices}, set()
    yield {'answers': answers}, {'hey', 'mister'}
    yield {'duration': duration}, set()
    yield {'expires_at': expires_at}, set()
    yield {'finalized': finalized}, set()
    yield {'layout': layout}, set()
    yield {'question': question}, {'wanna play'}
    yield {'results': results}, set()


@vampytest._(vampytest.call_from(_iter_options__contents()).returning_last())
def test__Poll__contents(keyword_parameters):
    """
    Tests whether ``Poll.contents`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the poll question with.
    
    Returns
    -------
    output : `set<str>`
    """
    poll = Poll(**keyword_parameters)
    output = poll.contents
    vampytest.assert_instance(output, list)
    return {*output}


def _iter_options__iter_contents():
    allow_multiple_choices = True
    answers = [
        PollAnswer.precreate(202404140052, text = 'hey'),
        PollAnswer.precreate(202404140053, text = 'mister'),
    ]
    duration = 7200
    expires_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    finalized = True
    layout = PollLayout.default
    question = PollQuestion(text = 'wanna play')
    results = [
        PollResult(answer_id = 202404140085),
        PollResult(answer_id = 202404140086),
    ]
    
    yield {}, set()
    yield {'allow_multiple_choices': allow_multiple_choices}, set()
    yield {'answers': answers}, {'hey', 'mister'}
    yield {'duration': duration}, set()
    yield {'expires_at': expires_at}, set()
    yield {'finalized': finalized}, set()
    yield {'layout': layout}, set()
    yield {'question': question}, {'wanna play'}
    yield {'results': results}, set()


@vampytest._(vampytest.call_from(_iter_options__iter_contents()).returning_last())
def test__Poll__iter_contents(keyword_parameters):
    """
    Tests whether ``Poll.iter_contents`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the poll question with.
    
    Returns
    -------
    output : `set<str>`
    """
    poll = Poll(**keyword_parameters)
    return {*poll.iter_contents()}


def _iter_options__iter_answers():
    answer_0 = PollAnswer.precreate(202404170022, text = 'hey')
    answer_1 = PollAnswer.precreate(202404170023, text = 'mister')
    
    yield None, set()
    yield [answer_0], {answer_0}
    yield [answer_0, answer_1], {answer_0, answer_1}


@vampytest._(vampytest.call_from(_iter_options__iter_answers()).returning_last())
def test__Poll__iter_answers(input_value):
    """
    Tests whether ``Poll.iter_answers`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<PollAnswer>`
        Poll answers to create the poll with.
    
    Returns
    -------
    output : `set<PollAnswer>`
    """
    poll = Poll(answers = input_value)
    return {*poll.iter_answers()}


def _iter_options__iter_results():
    result_0 = PollResult(answer_id = 202404170024, count = 2)
    result_1 = PollResult(answer_id = 202404170025, count = 3)
    
    yield None, set()
    yield [result_0], {result_0}
    yield [result_0, result_1], {result_0, result_1}


@vampytest._(vampytest.call_from(_iter_options__iter_results()).returning_last())
def test__Poll__iter_results(input_value):
    """
    Tests whether ``Poll.iter_results`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<PollResult>`
        Poll results to create the poll with.
    
    Returns
    -------
    output : `set<PollResult>`
    """
    poll = Poll(results = input_value)
    return {*poll.iter_results()}


def _iter_options__add_vote():
    answer_id_0 = 202404200000
    answer_id_1 = 202404200001
    user_0 = User.precreate(202404200002)
    user_1 = User.precreate(202404200003)
    
    yield (
        None,
        answer_id_0,
        user_0,
        (
            True,
            [
                PollResult(answer_id = answer_id_0, count = 1, users = [user_0]),
            ],
        ),
    )
    
    yield (
        [
            PollResult(answer_id = answer_id_1, count = 1, users = [user_1]),
        ],
        answer_id_0,
        user_0,
        (
            True,
            [
                PollResult(answer_id = answer_id_1, count = 1, users = [user_1]),
                PollResult(answer_id = answer_id_0, count = 1, users = [user_0]),
            ],
        ),
    )
    
    yield (
        [
            PollResult(answer_id = answer_id_1, count = 1, users = [user_1]),
        ],
        answer_id_1,
        user_0,
        (
            True,
            [
                PollResult(answer_id = answer_id_1, count = 2, users = [user_1, user_0]),
            ],
        ),
    )
    
    yield (
        [
            PollResult(answer_id = answer_id_1, count = 1, users = [user_1]),
        ],
        answer_id_1,
        user_1,
        (
            False,
            [
                PollResult(answer_id = answer_id_1, count = 1, users = [user_1]),
            ],
        ),
    )



@vampytest._(vampytest.call_from(_iter_options__add_vote()).returning_last())
def test__Poll__add_vote(results, answer_id, user):
    """
    Tests whether ``Poll._add_vote`` works as intended.
    
    Parameters
    ----------
    results : `None | list<PollResult>`
        Results to create the poll with.
    answer_id : `int`
        The answer's identifier.
    user : ``ClientUserBase``
        The user who voted.
    
    Returns
    -------
    output : `(int, None | list<PollResult>)`
    """
    if (results is not None):
        results = [result.copy() for result in results]
    
    poll = Poll(results = results)
    output = poll._add_vote(answer_id, user)
    vampytest.assert_instance(output, bool)
    return output, poll.results


def _iter_options__remove_vote():
    answer_id_0 = 202404200004
    answer_id_1 = 202404200005
    user_0 = User.precreate(202404200006)
    user_1 = User.precreate(202404200007)
    
    yield (
        None,
        answer_id_0,
        user_0,
        (
            False,
            None,
        ),
    )
    
    yield (
        [
            PollResult(answer_id = answer_id_1, count = 1, users = [user_1]),
        ],
        answer_id_0,
        user_0,
        (
            False,
            [
                PollResult(answer_id = answer_id_1, count = 1, users = [user_1]),
            ],
        ),
    )
    
    yield (
        [
            PollResult(answer_id = answer_id_1, count = 1, users = [user_1, user_0]),
        ],
        answer_id_1,
        user_0,
        (
            True,
            [
                PollResult(answer_id = answer_id_1, count = 1, users = [user_1]),
            ],
        ),
    )
    
    yield (
        [
            PollResult(answer_id = answer_id_1, count = 1, users = [user_1]),
        ],
        answer_id_1,
        user_1,
        (
            True,
            [
                PollResult(answer_id = answer_id_1, count = 0, users = []),
            ],
        ),
    )


@vampytest._(vampytest.call_from(_iter_options__remove_vote()).returning_last())
def test__Poll__remove_vote(results, answer_id, user):
    """
    Tests whether ``Poll._remove_vote`` works as intended.
    
    Parameters
    ----------
    results : `None | list<PollResult>`
        Results to create the poll with.
    answer_id : `int`
        The answer's identifier.
    user : ``ClientUserBase``
        The user who removed their vote.
    
    Returns
    -------
    output : `(int, None | list<PollResult>)`
    """
    if (results is not None):
        results = [result.copy() for result in results]
    
    poll = Poll(results = results)
    output = poll._remove_vote(answer_id, user)
    vampytest.assert_instance(output, bool)
    return output, poll.results


def _iter_options__get_answer_id():
    answer_0 = PollAnswer.precreate(202404200034, text = 'hey')
    answer_1 = PollAnswer.precreate(202404200035, text = 'mister')
    answer_2 = PollAnswer(text = 'mister')
    answer_3 = PollAnswer(text = 'sister')
    
    yield [answer_0, answer_1], answer_0, answer_0.id
    yield [answer_0, answer_1], answer_1, answer_1.id
    yield [answer_0, answer_1], answer_2, answer_1.id
    yield [answer_0, answer_1], answer_3, 0
    yield None, answer_0, 0


@vampytest._(vampytest.call_from(_iter_options__get_answer_id()).returning_last())
def test__Poll__get_answer_id(answers, answer):
    """
    Tests whether ``Poll.get_answer_id`` works as intended.
    
    Parameters
    ----------
    answers : `None | list<PollAnswer>`
        Poll answers to create the poll with.
    answer : ``PollAnswer``
        Answer to get id for.
    
    Returns
    -------
    results : `int`
    """
    poll = Poll(answers = answers)
    output =  poll.get_answer_id(answer)
    vampytest.assert_instance(output, int)
    return output


def _iter_options__get_or_create_result():
    answer_id_0 = 202404210000
    answer_id_1 = 202404210001
    user_0 = User.precreate(202404210002)
    
    yield (
        None,
        answer_id_0,
        (
            PollResult(answer_id = answer_id_0, count = 0),
            [
                PollResult(answer_id = answer_id_0, count = 0),
            ],
        ),
    )
    
    yield (
        [
            PollResult(answer_id = answer_id_1, count = 1, users = [user_0]),
        ],
        answer_id_0,
        (
            PollResult(answer_id = answer_id_0, count = 0),
            [
                PollResult(answer_id = answer_id_1, count = 1, users = [user_0]),
                PollResult(answer_id = answer_id_0, count = 0),
            ],
        ),
    )
    
    yield (
        [
            PollResult(answer_id = answer_id_1, count = 1, users = [user_0]),
        ],
        answer_id_1,
        (
            PollResult(answer_id = answer_id_1, count = 1, users = [user_0]),
            [
                PollResult(answer_id = answer_id_1, count = 1, users = [user_0]),
            ],
        ),
    )


@vampytest._(vampytest.call_from(_iter_options__get_or_create_result()).returning_last())
def test__Poll__get_or_create_result(results, answer_id):
    """
    Tests whether ``Poll._get_or_create_result`` works as intended.
    
    Parameters
    ----------
    results : `None | list<PollResult>`
        Results to create the poll with.
    answer_id : `int`
        The answer's identifier.
    
    Returns
    -------
    output : `(int, None | list<PollResult>)`
    """
    if (results is not None):
        results = [result.copy() for result in results]
    
    poll = Poll(results = results)
    output = poll._get_or_create_result(answer_id)
    vampytest.assert_instance(output, PollResult)
    return output, poll.results


def _iter_options__fill_some_votes():
    answer_id_0 = 202404210007
    answer_id_1 = 202404210008
    user_0 = User.precreate(202404210009)
    user_1 = User.precreate(202404210010)
    
    yield (
        None,
        answer_id_0,
        [],
        [
            PollResult(answer_id = answer_id_0, count = 0),
        ],
    )
    
    yield (
        [
            PollResult(answer_id = answer_id_0, count = 1, users = [user_1]),
        ],
        answer_id_0,
        [],
        [
            PollResult(answer_id = answer_id_0, count = 1, users = [user_1]),
        ],
    )
    
    yield (
        None,
        answer_id_0,
        [user_0],
        [
            PollResult(answer_id = answer_id_0, count = 1, users = [user_0]),
        ],
    )
    
    yield (
        [
            PollResult(answer_id = answer_id_1, count = 1, users = [user_1]),
        ],
        answer_id_0,
        [user_0],
        [
            PollResult(answer_id = answer_id_1, count = 1, users = [user_1]),
            PollResult(answer_id = answer_id_0, count = 1, users = [user_0]),
        ],
    )
    
    yield (
        [
            PollResult(answer_id = answer_id_1, count = 1, users = [user_1]),
        ],
        answer_id_1,
        [user_0],
        [
            PollResult(answer_id = answer_id_1, count = 2, users = [user_1, user_0]),
        ],
    )
    
    yield (
        [
            PollResult(answer_id = answer_id_1, count = 1, users = [user_1]),
        ],
        answer_id_1,
        [user_1],
        [
            PollResult(answer_id = answer_id_1, count = 1, users = [user_1]),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options__fill_some_votes()).returning_last())
def test__Poll__fill_some_votes(results, answer_id, user):
    """
    Tests whether ``Poll._fill_some_votes`` works as intended.
    
    Parameters
    ----------
    results : `None | list<PollResult>`
        Results to create the poll with.
    answer_id : `int`
        The answer's identifier.
    user : ``ClientUserBase``
        The user who voted.
    
    Returns
    -------
    output : `(int, None | list<PollResult>)`
    """
    if (results is not None):
        results = [result.copy() for result in results]
    
    poll = Poll(results = results)
    poll._fill_some_votes(answer_id, user)
    return poll.results


def _iter_options__fill_all_votes():
    answer_id_0 = 202404210011
    answer_id_1 = 202404210012
    user_0 = User.precreate(202404210013)
    user_1 = User.precreate(202404210014)
    
    yield (
        None,
        answer_id_0,
        [],
        [
            PollResult(answer_id = answer_id_0, count = 0),
        ],
    )
    
    yield (
        [
            PollResult(answer_id = answer_id_0, count = 1, users = [user_1]),
        ],
        answer_id_0,
        [],
        [
            PollResult(answer_id = answer_id_0, count = 0),
        ],
    )
    
    yield (
        None,
        answer_id_0,
        [user_0],
        [
            PollResult(answer_id = answer_id_0, count = 1, users = [user_0]),
        ],
    )
    
    yield (
        [
            PollResult(answer_id = answer_id_1, count = 1, users = [user_1]),
        ],
        answer_id_0,
        [user_0],
        [
            PollResult(answer_id = answer_id_1, count = 1, users = [user_1]),
            PollResult(answer_id = answer_id_0, count = 1, users = [user_0]),
        ],
    )
    
    yield (
        [
            PollResult(answer_id = answer_id_1, count = 1, users = [user_1]),
        ],
        answer_id_1,
        [user_0],
        [
            PollResult(answer_id = answer_id_1, count = 1, users = [user_0]),
        ],
    )
    
    yield (
        [
            PollResult(answer_id = answer_id_1, count = 1, users = [user_1]),
        ],
        answer_id_1,
        [user_1],
        [
            PollResult(answer_id = answer_id_1, count = 1, users = [user_1]),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options__fill_all_votes()).returning_last())
def test__Poll__fill_all_votes(results, answer_id, user):
    """
    Tests whether ``Poll._fill_all_votes`` works as intended.
    
    Parameters
    ----------
    results : `None | list<PollResult>`
        Results to create the poll with.
    answer_id : `int`
        The answer's identifier.
    user : ``ClientUserBase``
        The user who voted.
    
    Returns
    -------
    output : `(int, None | list<PollResult>)`
    """
    if (results is not None):
        results = [result.copy() for result in results]
    
    poll = Poll(results = results)
    poll._fill_all_votes(answer_id, user)
    return poll.results


def test__Poll__iter_items():
    """
    Tests whether ``Poll.iter_items`` works as intended.
    """
    answer_id_0 = 202404210030
    answer_id_1 = 202404210031
    answer_id_2 = 202404210032
    
    answer_0 = PollAnswer.precreate(answer_id_0, text = 'pudding')
    answer_1 = PollAnswer.precreate(answer_id_1, text = 'eater')
    
    result_0 = PollResult(answer_id = answer_id_0, count = 1)
    result_1 = PollResult(answer_id = answer_id_1, count = 0)
    result_2 = PollResult(answer_id = answer_id_2, count = 1)
    
    poll = Poll(answers = [answer_0, answer_1], results = [result_0, result_2])
    
    output = [*poll.iter_items()]
    
    vampytest.assert_eq(
        output,
        [
            (answer_0, result_0),
            (answer_1, result_1),
        ],
    )
