import vampytest

from ....user import User

from ..poll_result import PollResult


def _assert_fields_set(poll_result):
    """
    Asserts whether every attributes are set of the given poll result.
    
    Parameters
    ----------
    poll_result : ``PollResult``
        The poll result to check.
    """
    vampytest.assert_instance(poll_result, PollResult)
    vampytest.assert_instance(poll_result.answer_id, int)
    vampytest.assert_instance(poll_result.count, int)
    vampytest.assert_instance(poll_result.users, set, nullable = True)



def test__PollResult__new__no_fields():
    """
    Tests whether ``PollResult.__new__`` works as intended.
    
    Case: No fields given.
    """
    poll_result = PollResult()
    _assert_fields_set(poll_result)


def test__PollResult__new__all_fields():
    """
    Tests whether ``PollResult.__new__`` works as intended.
    
    Case: all fields given.
    """
    answer_id = 202404040003
    count = 3
    users = [
        User.precreate(202404160010),
        User.precreate(202404160011),
    ]
    
    poll_result = PollResult(
        answer_id = answer_id,
        count = count,
        users = users,
    )
    
    _assert_fields_set(poll_result)
    vampytest.assert_eq(poll_result.answer_id, answer_id)
    vampytest.assert_eq(poll_result.count, count)
    vampytest.assert_eq(poll_result.users, set(users))


def test__PollResult__create_empty():
    """
    Tests whether ``PollResult._create_empty`` works as intended.
    
    Case: No fields given.
    """
    answer_id = 202404190000
    
    poll_result = PollResult._create_empty(answer_id)
    _assert_fields_set(poll_result)
    
    vampytest.assert_eq(poll_result.answer_id, answer_id)
