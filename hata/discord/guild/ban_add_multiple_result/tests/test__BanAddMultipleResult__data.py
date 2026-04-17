import vampytest

from ..ban_add_multiple_result import BanAddMultipleResult


from .test__BanAddMultipleResult__constructor import _assert_fields_set


def test__BanAddMultipleResult__from_data():
    """
    Tests whether ``BanAddMultipleResult.from_data`` works as intended.
    
    Case: all fields given.
    """
    banned_user_ids = [202405010031, 202405010032]
    failed_user_ids = [202405010032, 202405010033]
    
    data = {
        'banned_users': [str(user_id) for user_id in banned_user_ids],
        'failed_users': [str(user_id) for user_id in failed_user_ids],
    }
    
    ban_add_multiple_result = BanAddMultipleResult.from_data(data)
    _assert_fields_set(ban_add_multiple_result)
    
    vampytest.assert_eq(ban_add_multiple_result.banned_user_ids, tuple(banned_user_ids))
    vampytest.assert_eq(ban_add_multiple_result.failed_user_ids, tuple(failed_user_ids))


def test__BanAddMultipleResult__to_data():
    """
    Tests whether ``BanAddMultipleResult.to_data`` works as intended.
    
    Case: Include defaults.
    """
    banned_user_ids = [202405010034, 202405010035]
    failed_user_ids = [202405010036, 202405010037]
    
    ban_add_multiple_result = BanAddMultipleResult(
        banned_user_ids = banned_user_ids,
        failed_user_ids = failed_user_ids,
    )
    expected_output = {
        'banned_users': [str(user_id) for user_id in banned_user_ids],
        'failed_users': [str(user_id) for user_id in failed_user_ids],
    }
    
    vampytest.assert_eq(
        ban_add_multiple_result.to_data(defaults = True),
        expected_output,
    )
