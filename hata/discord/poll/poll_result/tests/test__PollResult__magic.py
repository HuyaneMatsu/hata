import vampytest

from ....user import User

from ..poll_result import PollResult


def test__PollResult__repr():
    """
    Tests whether ``PollResult.__repr__`` works as intended.
    """
    answer_id = 202404040006
    count = 3
    users = [
        User.precreate(202404160014),
        User.precreate(202404160015),
    ]
    
    poll_result = PollResult(
        answer_id = answer_id,
        count = count,
        users = users,
    )
    
    vampytest.assert_instance(repr(poll_result), str)


def test__PollResult__hash():
    """
    Tests whether ``PollResult.__hash__`` works as intended.
    """
    answer_id = 202404040007
    count = 3
    users = [
        User.precreate(202404160016),
        User.precreate(202404160017),
    ]
    
    poll_result = PollResult(
        answer_id = answer_id,
        count = count,
        users = users,
    )
    
    vampytest.assert_instance(hash(poll_result), int)


def test__PollResult__eq():
    """
    Tests whether ``PollResult.__eq__`` works as intended.
    """
    answer_id = 202404040008
    count = 3
    users = [
        User.precreate(202404160018),
        User.precreate(202404160019),
    ]
    
    keyword_parameters = {
        'answer_id': answer_id,
        'count': count,
        'users': users,
    }
    
    poll_result = PollResult(**keyword_parameters)
    vampytest.assert_eq(poll_result, poll_result)
    vampytest.assert_ne(poll_result, object())
    
    for field_name, field_value in (
        ('answer_id', 202404040009),
        ('count', 4),
        ('users', None),
    ):
        test_poll_result = PollResult(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(poll_result, test_poll_result)


def _iter_options__len():
    user_0 = User.precreate(202404160028)
    user_1 = User.precreate(202404160029)
    
    yield {'count': 0}, 0
    yield {'count': 2}, 0
    yield {'users': []}, 0
    yield {'users': [user_0, user_1]}, 2


@vampytest._(vampytest.call_from(_iter_options__len()).returning_last())
def test__PollResult__len(keyword_parameters):
    """
    Tests whether ``PollResult.__len__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Parameters to test with.
    
    Returns
    -------
    output : `int`
    """
    poll_result = PollResult(**keyword_parameters)
    output = len(poll_result)
    vampytest.assert_instance(output, int)
    return output


def _iter_options__iter():
    user_0 = User.precreate(202404160028)
    user_1 = User.precreate(202404160029)
    
    yield {'count': 0}, set()
    yield {'count': 2}, set()
    yield {'users': []}, set()
    yield {'users': [user_0, user_1]}, {user_0, user_1}


@vampytest._(vampytest.call_from(_iter_options__iter()).returning_last())
def test__PollResult__iter(keyword_parameters):
    """
    Tests whether ``PollResult.__iter__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Parameters to test with.
    
    Returns
    -------
    output : `set<ClientUserBase>`
    """
    poll_result = PollResult(**keyword_parameters)
    return {*poll_result}


def _iter_options__contains():
    user_0 = User.precreate(202404200020)
    user_1 = User.precreate(202404200021)
    
    yield {'count': 0}, user_0, False
    yield {'count': 2}, user_0, False
    yield {'users': [user_0]}, user_0, True
    yield {'users': [user_1]}, user_0, False


@vampytest._(vampytest.call_from(_iter_options__contains()).returning_last())
def test__PollResult__contains(keyword_parameters, user):
    """
    Tests whether ``PollResult.__contains__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Parameters to test with.
    
    Returns
    -------
    output : `bool`
    """
    poll_result = PollResult(**keyword_parameters)
    output = user in poll_result
    vampytest.assert_instance(output, bool)
    return output
