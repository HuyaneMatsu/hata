import vampytest

from ..ban_add_multiple_result import BanAddMultipleResult


def _assert_fields_set(ban_add_multiple_result):
    """
    Checks whether every attribute is set of the given ban add multiple result.
    
    Parameters
    ----------
    ban_add_multiple_result : ``BanAddMultipleResult``
        The ban add multiple result to check.
    """
    vampytest.assert_instance(ban_add_multiple_result, BanAddMultipleResult)
    vampytest.assert_instance(ban_add_multiple_result.banned_user_ids, tuple, nullable = True)
    vampytest.assert_instance(ban_add_multiple_result.failed_user_ids, tuple, nullable = True)


def test__BanAddMultipleResult__new__no_fields():
    """
    Tests whether ``BanAddMultipleResult.__new__`` works as intended.
    
    Case: No given.
    """

    ban_add_multiple_result = BanAddMultipleResult()
    
    _assert_fields_set(ban_add_multiple_result)


def test__BanAddMultipleResult__new__all_fields():
    """
    Tests whether ``BanAddMultipleResult.__new__`` works as intended.
    
    Case: all fields given.
    """
    banned_user_ids = [202405010026, 202405010027]
    failed_user_ids = [202405010028, 202405010029]
    
    ban_add_multiple_result = BanAddMultipleResult(
        banned_user_ids = banned_user_ids,
        failed_user_ids = failed_user_ids,
    )
    
    _assert_fields_set(ban_add_multiple_result)
    
    vampytest.assert_eq(ban_add_multiple_result.banned_user_ids, tuple(banned_user_ids))
    vampytest.assert_eq(ban_add_multiple_result.failed_user_ids, tuple(failed_user_ids))
