from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..invite_allowed_user_ids_status import InviteAllowedUserIdsStatus
from ..preinstanced import InviteAllowedUserIdsStatusStatus

from .test__InviteAllowedUserIdsStatus__constructor import _assert_fields_set


def test__InviteAllowedUserIdsStatus__copy():
    """
    Tests whether ``InviteAllowedUserIdsStatus.copy`` works as intended.
    """
    completed_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    error_message = 'Baka 9'
    processed = 5
    started_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    status = InviteAllowedUserIdsStatusStatus.failed
    total = 6
    
    invite_allowed_user_ids_status = InviteAllowedUserIdsStatus(
        completed_at = completed_at,
        error_message = error_message,
        processed = processed,
        started_at = started_at,
        status = status,
        total = total,
    )
    
    copy = invite_allowed_user_ids_status.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, invite_allowed_user_ids_status)
    vampytest.assert_eq(copy, invite_allowed_user_ids_status)


def test__InviteAllowedUserIdsStatus__copy_with__no_fields():
    """
    Tests whether ``InviteAllowedUserIdsStatus.copy_with`` works as intended.
    
    Case: no fields given.
    """
    completed_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    error_message = 'Baka 9'
    processed = 5
    started_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    status = InviteAllowedUserIdsStatusStatus.failed
    total = 6
    
    invite_allowed_user_ids_status = InviteAllowedUserIdsStatus(
        completed_at = completed_at,
        error_message = error_message,
        processed = processed,
        started_at = started_at,
        status = status,
        total = total,
    )
    
    copy = invite_allowed_user_ids_status.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, invite_allowed_user_ids_status)
    vampytest.assert_eq(copy, invite_allowed_user_ids_status)


def test__InviteAllowedUserIdsStatus__copy_with__all_fields():
    """
    Tests whether ``InviteAllowedUserIdsStatus.copy_with`` works as intended.
    
    Case: all fields given.
    """
    old_completed_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    old_error_message = 'Baka 9'
    old_processed = 5
    old_started_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    old_status = InviteAllowedUserIdsStatusStatus.failed
    old_total = 6
    
    new_completed_at = DateTime(2016, 9, 14, tzinfo = TimeZone.utc)
    new_error_message = 'Dai knows'
    new_processed = 8
    new_started_at = DateTime(2016, 9, 15, tzinfo = TimeZone.utc)
    new_status = InviteAllowedUserIdsStatusStatus.completed
    new_total = 9
    
    invite_allowed_user_ids_status = InviteAllowedUserIdsStatus(
        completed_at = old_completed_at,
        error_message = old_error_message,
        processed = old_processed,
        started_at = old_started_at,
        status = old_status,
        total = old_total,
    )
    
    copy = invite_allowed_user_ids_status.copy_with(
        completed_at = new_completed_at,
        error_message = new_error_message,
        processed = new_processed,
        started_at = new_started_at,
        status = new_status,
        total = new_total,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, invite_allowed_user_ids_status)
    vampytest.assert_ne(copy, invite_allowed_user_ids_status)
    
    vampytest.assert_eq(copy.completed_at, new_completed_at)
    vampytest.assert_eq(copy.error_message, new_error_message)
    vampytest.assert_eq(copy.processed, new_processed)
    vampytest.assert_eq(copy.started_at, new_started_at)
    vampytest.assert_is(copy.status, new_status)
    vampytest.assert_eq(copy.total, new_total)
