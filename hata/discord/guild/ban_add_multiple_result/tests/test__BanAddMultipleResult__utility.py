import vampytest

from ....user import User

from ..ban_add_multiple_result import BanAddMultipleResult

from .test__BanAddMultipleResult__constructor import _assert_fields_set


def test__BanAddMultipleResult__copy():
    """
    Tests whether ``BanAddMultipleResult.copy`` works as intended.
    """
    banned_user_ids = [202405010054, 202405010055]
    failed_user_ids = [202405010056, 202405010057]
    
    ban_add_multiple_result = BanAddMultipleResult(
        banned_user_ids = banned_user_ids,
        failed_user_ids = failed_user_ids,
    )
    
    copy = ban_add_multiple_result.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(ban_add_multiple_result, copy)

    vampytest.assert_eq(ban_add_multiple_result, copy)


def test__BanAddMultipleResult__copy_with__no_fields():
    """
    Tests whether ``BanAddMultipleResult.copy_with`` works as intended.
    
    Case: no fields given.
    """
    banned_user_ids = [202405010058, 202405010059]
    failed_user_ids = [202405010060, 202405010061]
    
    ban_add_multiple_result = BanAddMultipleResult(
        banned_user_ids = banned_user_ids,
        failed_user_ids = failed_user_ids,
    )
    
    copy = ban_add_multiple_result.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(ban_add_multiple_result, copy)

    vampytest.assert_eq(ban_add_multiple_result, copy)


def test__BanAddMultipleResult__copy_with__all_fields():
    """
    Tests whether ``BanAddMultipleResult.copy_with`` works as intended.
    
    Case: all fields given.
    """
    old_banned_user_ids = [202405010062, 202405010063]
    old_failed_user_ids = [202405010064, 202405010065]
    
    new_banned_user_ids = [202405010066, 202405010067]
    new_failed_user_ids = [202405010068, 202405010069]
    
    ban_add_multiple_result = BanAddMultipleResult(
        banned_user_ids = old_banned_user_ids,
        failed_user_ids = old_failed_user_ids,
    )
    
    copy = ban_add_multiple_result.copy_with(
        banned_user_ids = new_banned_user_ids,
        failed_user_ids = new_failed_user_ids,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(ban_add_multiple_result, copy)
    
    vampytest.assert_eq(copy.banned_user_ids, tuple(new_banned_user_ids))
    vampytest.assert_eq(copy.failed_user_ids, tuple(new_failed_user_ids))


def _iter_options__iter_banned_user_ids():
    user_id_0 = 202405010068
    user_id_1 = 202405010069
    
    yield None, []
    yield [user_id_0], [user_id_0]
    yield [user_id_0, user_id_1], [user_id_0, user_id_1]


@vampytest._(vampytest.call_from(_iter_options__iter_banned_user_ids()).returning_last())
def test__BanAddMultipleResult__iter_banned_user_ids(input_banned_user_ids):
    """
    Tests whether ``BanAddMultipleResult.iter_banned_user_ids`` works as intended.
    
    Parameters
    ----------
    input_banned_user_ids : `None | list<int>`
        User identifiers to create the ban add multiple results with.
    
    Returns
    -------
    output : `list<int>`
    """
    ban_add_multiple_result = BanAddMultipleResult(banned_user_ids = input_banned_user_ids)
    return [*ban_add_multiple_result.iter_banned_user_ids()]


def _iter_options__iter_banned_users():
    user_id_0 = 202405010070
    user_id_1 = 202405010071
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    
    yield None, []
    yield [user_id_0], [user_0]
    yield [user_id_0, user_id_1], [user_0, user_1]


@vampytest._(vampytest.call_from(_iter_options__iter_banned_users()).returning_last())
def test__BanAddMultipleResult__iter_banned_users(input_banned_user_ids):
    """
    Tests whether ``BanAddMultipleResult.iter_banned_users`` works as intended.
    
    Parameters
    ----------
    input_banned_user_ids : `None | list<int>`
        User identifiers to create the ban add multiple results with.
    
    Returns
    -------
    output : `list<User>`
    """
    ban_add_multiple_result = BanAddMultipleResult(banned_user_ids = input_banned_user_ids)
    return [*ban_add_multiple_result.iter_banned_users()]


def _iter_options__iter_failed_user_ids():
    user_id_0 = 202405010072
    user_id_1 = 202405010073
    
    yield None, []
    yield [user_id_0], [user_id_0]
    yield [user_id_0, user_id_1], [user_id_0, user_id_1]


@vampytest._(vampytest.call_from(_iter_options__iter_failed_user_ids()).returning_last())
def test__BanAddMultipleResult__iter_failed_user_ids(input_failed_user_ids):
    """
    Tests whether ``BanAddMultipleResult.iter_failed_user_ids`` works as intended.
    
    Parameters
    ----------
    input_failed_user_ids : `None | list<int>`
        User identifiers to create the ban add multiple results with.
    
    Returns
    -------
    output : `list<int>`
    """
    ban_add_multiple_result = BanAddMultipleResult(failed_user_ids = input_failed_user_ids)
    return [*ban_add_multiple_result.iter_failed_user_ids()]


def _iter_options__iter_failed_users():
    user_id_0 = 202405010074
    user_id_1 = 202405010075
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    
    yield None, []
    yield [user_id_0], [user_0]
    yield [user_id_0, user_id_1], [user_0, user_1]


@vampytest._(vampytest.call_from(_iter_options__iter_failed_users()).returning_last())
def test__BanAddMultipleResult__iter_failed_users(input_failed_user_ids):
    """
    Tests whether ``BanAddMultipleResult.iter_failed_users`` works as intended.
    
    Parameters
    ----------
    input_failed_user_ids : `None | list<int>`
        User identifiers to create the ban add multiple results with.
    
    Returns
    -------
    output : `list<User>`
    """
    ban_add_multiple_result = BanAddMultipleResult(failed_user_ids = input_failed_user_ids)
    return [*ban_add_multiple_result.iter_failed_users()]
