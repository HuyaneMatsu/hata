import vampytest

from ....user import User

from ..poll_result import PollResult

from .test__PollResult__constructor import _assert_fields_set


def test__PollResult__copy():
    """
    Tests whether ``PollResult.copy`` works as intended.
    """
    answer_id = 202404040010
    count = 3
    users = [
        User.precreate(202404160020),
        User.precreate(202404160021),
    ]
    
    poll_result = PollResult(
        answer_id = answer_id,
        count = count,
        users = users,
    )
    
    copy = poll_result.copy()
    _assert_fields_set(copy)
    vampytest.assert_eq(poll_result, copy)
    vampytest.assert_is_not(poll_result, copy)


def test__PollResult__copy_with__no_fields():
    """
    Tests whether ``PollResult.copy`` works as intended.
    
    Case: No count
    """
    answer_id = 202404040011
    count = 3
    users = [
        User.precreate(202404160022),
        User.precreate(202404160023),
    ]
    
    poll_result = PollResult(
        answer_id = answer_id,
        count = count,
        users = users,
    )
    
    copy = poll_result.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_eq(poll_result, copy)
    vampytest.assert_is_not(poll_result, copy)


def test__PollResult__copy_with__all_fields():
    """
    Tests whether ``PollResult.copy`` works as intended.
    
    Case: No count
    """
    old_answer_id = 202404040012
    old_count = 3
    old_users = [
        User.precreate(202404160024),
        User.precreate(202404160025),
    ]
    
    new_answer_id = 202404040013
    new_count = 4
    new_users = [
        User.precreate(202404160026),
        User.precreate(202404160027),
    ]
    
    poll_result = PollResult(
        answer_id = old_answer_id,
        count = old_count,
        users = old_users,
    )
    
    copy = poll_result.copy_with(
        answer_id = new_answer_id,
        count = new_count,
        users = new_users,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(poll_result, copy)

    vampytest.assert_eq(copy.answer_id, new_answer_id)
    vampytest.assert_eq(copy.count, new_count)


def _iter_options__merge_with():
    user_0 = User.precreate(202404160032)
    user_1 = User.precreate(202404160033)
    
    yield {'count': 1}, {'count': 1}, (1, None)
    yield {'count': 2}, {'count': 1}, (1, None)
    yield {'count': 1}, {'count': 2}, (2, None)
    yield {'count': 1, 'users': {user_0}}, {'count': 1}, (1, {user_0})
    yield {'count': 2, 'users': {user_0, user_1}}, {'count': 1}, (1, set())
    yield {'count': 1, 'users': {user_0}}, {'count': 2}, (2, set())


@vampytest._(vampytest.call_from(_iter_options__merge_with()).returning_last())
def test__PollResult__merge_with(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``PollResult._merge_with`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create an instance.
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create an other instance.
    
    Returns
    -------
    output : `(int, None | set<ClientUserBase>)`
    """
    poll_result_0 = PollResult(**keyword_parameters_0)
    poll_result_1 = PollResult(**keyword_parameters_1)
    poll_result_0._merge_with(poll_result_1)
    return poll_result_0.count, poll_result_0.users


def _iter_options__add_vote():
    user_0 = User.precreate(202404190001)
    user_1 = User.precreate(202404190002)
    
    
    yield {}, user_0, (True, 1, {user_0})
    yield {'count': 1}, user_0, (True, 2, {user_0})
    yield {'count': 1, 'users': {user_0}}, user_0, (False, 1, {user_0})
    yield {'count': 1, 'users': {user_1}}, user_0, (True, 2, {user_0, user_1})


@vampytest._(vampytest.call_from(_iter_options__add_vote()).returning_last())
def test__PollResult__add_vote(keyword_parameters, user):
    """
    Tests whether ``PollResult._add_vote`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create an instance.
    user : ``ClientUserBase``
        Voter to add.
    
    Returns
    -------
    output : `(bool, int, None | set<ClientUserBase>)`
    """
    poll_result = PollResult(**keyword_parameters)
    output = poll_result._add_vote(user)
    vampytest.assert_instance(output, bool)
    return output, poll_result.count, poll_result.users


def _iter_options__remove_vote():
    user_0 = User.precreate(202404190003)
    user_1 = User.precreate(202404190004)
    
    
    yield {}, user_0, (False, 0, None)
    yield {'count': 1}, user_0, (True, 0, None)
    yield {'count': 1, 'users': {user_0}}, user_0, (True, 0, set())
    yield {'count': 1, 'users': {user_1}}, user_0, (False, 1, {user_1})
    yield {'count': 2, 'users': {user_0, user_1}}, user_0, (True, 1, {user_1})


@vampytest._(vampytest.call_from(_iter_options__remove_vote()).returning_last())
def test__PollResult__remove_vote(keyword_parameters, user):
    """
    Tests whether ``PollResult._remove_vote`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create an instance.
    user : ``ClientUserBase``
        Voter to remove.
    
    Returns
    -------
    output : `(bool, int, None | set<ClientUserBase>)`
    """
    poll_result = PollResult(**keyword_parameters)
    output = poll_result._remove_vote(user)
    vampytest.assert_instance(output, bool)
    return output, poll_result.count, poll_result.users


def _iter_options__unknown():
    user_0 = User.precreate(202404200036)
    user_1 = User.precreate(202404200037)
    
    yield {}, 0
    yield {'count': 2}, 2
    yield {'count': 2, 'users': {user_0, user_1}}, 0


@vampytest._(vampytest.call_from(_iter_options__unknown()).returning_last())
def test__PollResult__unknown(keyword_parameters):
    """
    Tests whether ``PollResult.unknown`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create an instance.
    
    Returns
    -------
    output : `int`
    """
    poll_result = PollResult(**keyword_parameters)
    output = poll_result.unknown
    vampytest.assert_instance(output, int)
    return output


def _iter_options__filter_after():
    user_0 = User.precreate(202404200038)
    user_1 = User.precreate(202404200039)
    user_2 = User.precreate(202404200040)
    user_3 = User.precreate(202404200041)
    user_4 = User.precreate(202404200042)
    
    yield {}, 2, user_1.id, []
    yield {'users': [user_0, user_1, user_2, user_3, user_4]}, 2, user_1.id, [user_2, user_3]


@vampytest._(vampytest.call_from(_iter_options__filter_after()).returning_last())
def test__PollResult__filter_after(keyword_parameters, limit, after):
    """
    Tests whether ``PollResult.filter_after`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create an instance.
    
    Returns
    -------
    output : `int`
    """
    poll_result = PollResult(**keyword_parameters)
    output = poll_result.filter_after(limit, after)
    vampytest.assert_instance(output, list)
    return output


def _iter_options__fill_some_votes():
    user_0 = User.precreate(202404210003)
    user_1 = User.precreate(202404210004)
    
    yield {}, [], (0, None)
    yield {'count': 1, 'users': {user_0}}, [], (1, {user_0})
    yield {}, [user_0], (1, {user_0})
    yield {'count': 1}, [user_0], (1, {user_0})
    yield {'count': 1, 'users': {user_0}}, [user_0], (1, {user_0})
    yield {'count': 1, 'users': {user_1}}, [user_0], (2, {user_0, user_1})


@vampytest._(vampytest.call_from(_iter_options__fill_some_votes()).returning_last())
def test__PollResult__fill_some_votes(keyword_parameters, user):
    """
    Tests whether ``PollResult._fill_some_votes`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create an instance.
    users : `list` of ``ClientUserBase``
        Voters to fill.
    
    Returns
    -------
    output : `(int, None | set<ClientUserBase>)`
    """
    poll_result = PollResult(**keyword_parameters)
    poll_result._fill_some_votes(user)
    return poll_result.count, poll_result.users


def _iter_options__fill_all_votes():
    user_0 = User.precreate(202404210005)
    user_1 = User.precreate(202404210006)
    
    yield {}, [], (0, None)
    yield {'count': 1, 'users': {user_0}}, [], (0, set())
    yield {}, [user_0], (1, {user_0})
    yield {'count': 1}, [user_0], (1, {user_0})
    yield {'count': 1, 'users': {user_0}}, [user_0], (1, {user_0})
    yield {'count': 1, 'users': {user_1}}, [user_0], (1, {user_0})


@vampytest._(vampytest.call_from(_iter_options__fill_all_votes()).returning_last())
def test__PollResult__fill_all_votes(keyword_parameters, user):
    """
    Tests whether ``PollResult._fill_all_votes`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create an instance.
    users : `list` of ``ClientUserBase``
        Voters to fill.
    
    Returns
    -------
    output : `(int, None | set<ClientUserBase>)`
    """
    poll_result = PollResult(**keyword_parameters)
    poll_result._fill_all_votes(user)
    return poll_result.count, poll_result.users
