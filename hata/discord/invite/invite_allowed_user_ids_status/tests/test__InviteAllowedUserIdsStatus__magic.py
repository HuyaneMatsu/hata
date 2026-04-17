from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..invite_allowed_user_ids_status import InviteAllowedUserIdsStatus
from ..preinstanced import InviteAllowedUserIdsStatusStatus


def test__InviteAllowedUserIdsStatus__repr():
    """
    Tests whether ``InviteAllowedUserIdsStatus.__repr__`` works as intended.
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
    
    output = repr(invite_allowed_user_ids_status)
    vampytest.assert_instance(output, str)


def test__InviteAllowedUserIdsStatus__hash():
    """
    Tests whether ``InviteAllowedUserIdsStatus.__hash__`` works as intended.
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
    
    output = hash(invite_allowed_user_ids_status)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    completed_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    error_message = 'Baka 9'
    processed = 5
    started_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    status = InviteAllowedUserIdsStatusStatus.failed
    total = 6
    
    keyword_parameters = {
        'completed_at': completed_at,
        'error_message': error_message,
        'processed': processed,
        'started_at': started_at,
        'status': status,
        'total': total,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'completed_at': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'error_message': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'processed': 0,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'started_at': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'status': InviteAllowedUserIdsStatusStatus.processing,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'total': 0,
        },
        False,
    )
    

@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__InviteAllowedUserIdsStatus__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``InviteAllowedUserIdsStatus.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    invite_allowed_user_ids_status_0 = InviteAllowedUserIdsStatus(**keyword_parameters_0)
    invite_allowed_user_ids_status_1 = InviteAllowedUserIdsStatus(**keyword_parameters_1)
    
    output = invite_allowed_user_ids_status_0 == invite_allowed_user_ids_status_1
    vampytest.assert_instance(output, bool)
    return output
