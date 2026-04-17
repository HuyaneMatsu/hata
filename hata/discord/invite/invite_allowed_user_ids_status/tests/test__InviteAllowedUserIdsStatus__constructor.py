from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..invite_allowed_user_ids_status import InviteAllowedUserIdsStatus
from ..preinstanced import InviteAllowedUserIdsStatusStatus


def _assert_fields_set(invite_allowed_user_ids_status):
    """
    Asserts whether all the fields are set of the given instance.
    
    Parameters
    ----------
    invite_allowed_user_ids_status : ``InviteAllowedUserIdsStatus``
        The instance to check.
    """
    vampytest.assert_instance(invite_allowed_user_ids_status, InviteAllowedUserIdsStatus)
    vampytest.assert_instance(invite_allowed_user_ids_status.completed_at, DateTime, nullable = True)
    vampytest.assert_instance(invite_allowed_user_ids_status.error_message, str, nullable = True)
    vampytest.assert_instance(invite_allowed_user_ids_status.processed, int)
    vampytest.assert_instance(invite_allowed_user_ids_status.started_at, DateTime, nullable = True)
    vampytest.assert_instance(invite_allowed_user_ids_status.status, InviteAllowedUserIdsStatusStatus)
    vampytest.assert_instance(invite_allowed_user_ids_status.total, int)


def test__InviteAllowedUserIdsStatus__new__no_fields():
    """
    Tests whether ``InviteAllowedUserIdsStatus.__new__`` works as intended.
    
    Case: no fields given.
    """
    invite_allowed_user_ids_status = InviteAllowedUserIdsStatus()
    _assert_fields_set(invite_allowed_user_ids_status)


def test__InviteAllowedUserIdsStatus__new__all_fields():
    """
    Tests whether ``InviteAllowedUserIdsStatus.__new__`` works as intended.
    
    Case: all fields given.
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
    _assert_fields_set(invite_allowed_user_ids_status)
    
    vampytest.assert_eq(invite_allowed_user_ids_status.completed_at, completed_at)
    vampytest.assert_eq(invite_allowed_user_ids_status.error_message, error_message)
    vampytest.assert_eq(invite_allowed_user_ids_status.processed, processed)
    vampytest.assert_eq(invite_allowed_user_ids_status.started_at, started_at)
    vampytest.assert_is(invite_allowed_user_ids_status.status, status)
    vampytest.assert_eq(invite_allowed_user_ids_status.total, total)
