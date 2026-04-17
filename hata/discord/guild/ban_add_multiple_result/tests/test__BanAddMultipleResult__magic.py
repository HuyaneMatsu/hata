import vampytest

from ..ban_add_multiple_result import BanAddMultipleResult


def test__BanAddMultipleResult__repr():
    """
    Tests whether ``BanAddMultipleResult.__repr__`` works as intended.
    """
    banned_user_ids = [202405010038, 202405010039]
    failed_user_ids = [202405010040, 202405010041]
    
    ban_add_multiple_result = BanAddMultipleResult(
        banned_user_ids = banned_user_ids,
        failed_user_ids = failed_user_ids,
    )
    
    vampytest.assert_instance(repr(ban_add_multiple_result), str)


def test__BanAddMultipleResult__hash():
    """
    Tests whether ``BanAddMultipleResult.__hash__`` works as intended.
    """
    banned_user_ids = [202405010042, 202405010043]
    failed_user_ids = [202405010044, 202405010045]
    
    ban_add_multiple_result = BanAddMultipleResult(
        banned_user_ids = banned_user_ids,
        failed_user_ids = failed_user_ids,
    )
    
    vampytest.assert_instance(hash(ban_add_multiple_result), int)


def test__BanAddMultipleResult__eq():
    """
    Tests whether ``BanAddMultipleResult.__repr__`` works as intended.
    """
    banned_user_ids = [202405010046, 202405010047]
    failed_user_ids = [202405010048, 202405010049]
    
    keyword_parameters = {
        'banned_user_ids': banned_user_ids,
        'failed_user_ids': failed_user_ids,
    }
    
    ban_add_multiple_result = BanAddMultipleResult(**keyword_parameters)
    
    vampytest.assert_eq(ban_add_multiple_result, ban_add_multiple_result)
    vampytest.assert_ne(ban_add_multiple_result, object())
    
    for field_name, field_value in (
        ('banned_user_ids', None),
        ('failed_user_ids', None),
    ):
        ban_add_multiple_result_altered = BanAddMultipleResult(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(ban_add_multiple_result, ban_add_multiple_result_altered)


def test__BanAddMultipleResult__unpack():
    """
    Tests whether ``BanAddMultipleResult`` unpacking works as intended.
    """
    banned_user_ids = [202405010050, 202405010051]
    failed_user_ids = [202405010052, 202405010053]
    
    ban_add_multiple_result = BanAddMultipleResult(
        banned_user_ids = banned_user_ids,
        failed_user_ids = failed_user_ids,
    )
    
    vampytest.assert_eq(len([*ban_add_multiple_result]), len(ban_add_multiple_result))
