import vampytest

from ....user import User

from ..poll_result import PollResult

from .test__PollResult__constructor import _assert_fields_set


def test__PollResult__from_data():
    """
    Tests whether ``PollResult.from_data`` works as intended.
    """
    answer_id = 202404040004
    count = 3
    
    data = {
        'id': str(answer_id),
        'count': count,
    }
    
    poll_result = PollResult.from_data(data)
    _assert_fields_set(poll_result)
    
    vampytest.assert_eq(poll_result.answer_id, answer_id)
    vampytest.assert_eq(poll_result.count, count)
    vampytest.assert_eq(poll_result.users, None)


def test__PollResult__to_data():
    """
    Tests whether ``PollResult.to_data`` works as intended.
    
    Case: Include defaults.
    """
    answer_id = 202404040005
    count = 3
    users = [
        User.precreate(202404160012),
        User.precreate(202404160013),
    ]
    
    poll_result = PollResult(
        answer_id = answer_id,
        count = count,
        users = users,
    )
    
    expected_output = {
        'id': str(answer_id),
        'count': count,
    }
    
    vampytest.assert_eq(poll_result.to_data(defaults = True), expected_output)
