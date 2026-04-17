from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_timestamp

from ..invite_allowed_user_ids_status import InviteAllowedUserIdsStatus
from ..preinstanced import InviteAllowedUserIdsStatusStatus

from .test__InviteAllowedUserIdsStatus__constructor import _assert_fields_set


def test__InviteAllowedUserIdsStatus__from_data():
    """
    Tests whether ``InviteAllowedUserIdsStatus.from_data`` works as intended.
    """
    completed_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    error_message = 'Baka 9'
    processed = 5
    started_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    status = InviteAllowedUserIdsStatusStatus.failed
    total = 6
    
    data = {
        'completed_at': datetime_to_timestamp(completed_at),
        'error_message': error_message,
        'processed_users': processed,
        'created_at': datetime_to_timestamp(started_at),
        'status': status.value,
        'total_users': total,
    }
    
    invite_allowed_user_ids_status = InviteAllowedUserIdsStatus.from_data(data)
    _assert_fields_set(invite_allowed_user_ids_status)
    
    vampytest.assert_eq(invite_allowed_user_ids_status.completed_at, completed_at)
    vampytest.assert_eq(invite_allowed_user_ids_status.error_message, error_message)
    vampytest.assert_eq(invite_allowed_user_ids_status.processed, processed)
    vampytest.assert_eq(invite_allowed_user_ids_status.started_at, started_at)
    vampytest.assert_is(invite_allowed_user_ids_status.status, status)
    vampytest.assert_eq(invite_allowed_user_ids_status.total, total)


def test__InviteAllowedUserIdsStatus__to_data():
    """
    Tests whether ``InviteAllowedUserIdsStatus.to_data`` works as intended.
    """
    completed_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    error_message = 'Baka 9'
    processed = 5
    started_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    status = InviteAllowedUserIdsStatusStatus.failed
    total = 6
    
    expected_output = {
        'completed_at': datetime_to_timestamp(completed_at),
        'error_message': error_message,
        'processed_users': processed,
        'created_at': datetime_to_timestamp(started_at),
        'status': status.value,
        'total_users': total,
    }
    
    invite_allowed_user_ids_status = InviteAllowedUserIdsStatus(
        completed_at = completed_at,
        error_message = error_message,
        processed = processed,
        started_at = started_at,
        status = status,
        total = total,
    )
    
    vampytest.assert_eq(
        invite_allowed_user_ids_status.to_data(defaults = True),
        expected_output,
    )
