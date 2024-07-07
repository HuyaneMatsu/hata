from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....user import User
from ....utils import datetime_to_timestamp

from ...guild_join_request_form_response import GuildJoinRequestFormResponse

from ..guild_join_request import GuildJoinRequest
from ..preinstanced import GuildJoinRequestStatus


from .test__GuildJoinRequest__constructor import _assert_fields_set


def test__GuildJoinRequest__from_data__0():
    """
    Tests whether ``GuildJoinRequest.from_data`` works as intended.
    
    Case: all fields given.
    """
    actioned_by = User.precreate(202305170006, name = 'Koishi')
    actioned_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    created_at = DateTime(2017, 7, 6, tzinfo = TimeZone.utc)
    form_responses = [GuildJoinRequestFormResponse(), GuildJoinRequestFormResponse()]
    guild_id = 202305170007
    last_seen_at = DateTime(2018, 4, 4, tzinfo = TimeZone.utc)
    rejection_reason = 'Koishi is better'
    status = GuildJoinRequestStatus.rejected
    user = User.precreate(202305170008, name = 'Koisheep')
    
    data = {
        'actioned_by_user': actioned_by.to_data(defaults = True, include_internals = True),
        'actioned_at': datetime_to_timestamp(actioned_at),
        'created_at': datetime_to_timestamp(created_at),
        'form_responses': [form_response.to_data(defaults = True) for form_response in form_responses],
        'guild_id': str(guild_id),
        'last_seen': datetime_to_timestamp(last_seen_at),
        'rejection_reason': rejection_reason,
        'application_status': status.value,
        'user': user.to_data(defaults = True, include_internals = True),
        'user_id': str(user.id),
    }
    
    event = GuildJoinRequest.from_data(data)
    _assert_fields_set(event)
    
    vampytest.assert_is(event.actioned_by, actioned_by)
    vampytest.assert_eq(event.actioned_at, actioned_at)
    vampytest.assert_eq(event.created_at, created_at)
    vampytest.assert_eq(event.form_responses, tuple(form_responses))
    vampytest.assert_eq(event.guild_id, guild_id)
    vampytest.assert_eq(event.last_seen_at, last_seen_at)
    vampytest.assert_eq(event.rejection_reason, rejection_reason)
    vampytest.assert_is(event.status, status)
    vampytest.assert_is(event.user, user)


def test__GuildJoinRequest__to_data__0():
    """
    Tests whether ``GuildJoinRequest.to_data`` works as intended.
    
    Case: Include defaults.
    """
    actioned_by = User.precreate(202305170009, name = 'Koishi')
    actioned_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    created_at = DateTime(2017, 7, 6, tzinfo = TimeZone.utc)
    form_responses = [GuildJoinRequestFormResponse(), GuildJoinRequestFormResponse()]
    guild_id = 202305170010
    last_seen_at = DateTime(2018, 4, 4, tzinfo = TimeZone.utc)
    rejection_reason = 'Koishi is better'
    status = GuildJoinRequestStatus.rejected
    user = User.precreate(202305170011, name = 'Koisheep')
    
    event = GuildJoinRequest(
        actioned_by = actioned_by,
        actioned_at = actioned_at,
        created_at = created_at,
        form_responses = form_responses,
        guild_id = guild_id,
        last_seen_at = last_seen_at,
        rejection_reason = rejection_reason,
        status = status,
        user = user,
    )
    expected_output = {
        'actioned_by_user': actioned_by.to_data(defaults = True, include_internals = True),
        'actioned_at': datetime_to_timestamp(actioned_at),
        'created_at': datetime_to_timestamp(created_at),
        'form_responses': [form_response.to_data(defaults = True) for form_response in form_responses],
        'guild_id': str(guild_id),
        'last_seen': datetime_to_timestamp(last_seen_at),
        'rejection_reason': rejection_reason,
        'application_status': status.value,
        'user': user.to_data(defaults = True, include_internals = True),
        'user_id': str(user.id),
    }
    
    vampytest.assert_eq(
        event.to_data(defaults = True),
        expected_output,
    )
