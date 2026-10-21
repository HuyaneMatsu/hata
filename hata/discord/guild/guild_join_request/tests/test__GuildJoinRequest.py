from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....user import ClientUserBase, User
from ....utils import datetime_to_timestamp

from ...guild_join_request_form_field_response import (
    guild_join_request_form_field_response_convert_to_data, guild_join_request_form_field_response_create_boolean_terms
)

from ..guild_join_request import (
    GuildJoinRequest, guild_join_request_convert_to_data, guild_join_request_create, guild_join_request_create_from_data
)
from ..preinstanced import GuildJoinRequestStatus


def assert_guild_join_request_fields_set(guild_join_request):
    vampytest.assert_instance(guild_join_request, GuildJoinRequest)
    vampytest.assert_instance(guild_join_request.actioned_by, ClientUserBase, nullable = True)
    vampytest.assert_instance(guild_join_request.actioned_at, DateTime, nullable = True)
    vampytest.assert_instance(guild_join_request.created_at, DateTime, nullable = True)
    vampytest.assert_instance(guild_join_request.form_field_responses, tuple, nullable = True)
    vampytest.assert_instance(guild_join_request.guild_id, int)
    vampytest.assert_instance(guild_join_request.id, int)
    vampytest.assert_instance(guild_join_request.last_seen_at, DateTime, nullable = True)
    vampytest.assert_instance(guild_join_request.rejection_reason, str, nullable = True)
    vampytest.assert_instance(guild_join_request.status, GuildJoinRequestStatus)
    vampytest.assert_instance(guild_join_request.user, ClientUserBase, nullable = True)


def test__guild_join_request_create__no_fields():
    guild_join_request = guild_join_request_create()
    assert_guild_join_request_fields_set(guild_join_request)


def test__guild_join_request_create__all_fields():
    actioned_by = User.precreate(202305170003, name = 'Koishi')
    actioned_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    created_at = DateTime(2017, 7, 6, tzinfo = TimeZone.utc)
    form_field_responses = (
        guild_join_request_form_field_response_create_boolean_terms(description = 'hey'),
        guild_join_request_form_field_response_create_boolean_terms(description = 'ho'),
    )
    guild_id = 202305170004
    guild_join_request_id = 202610100020
    last_seen_at = DateTime(2018, 4, 4, tzinfo = TimeZone.utc)
    rejection_reason = 'Koishi is better'
    status = GuildJoinRequestStatus.rejected
    user = User.precreate(202305170005, name = 'Koisheep')
    
    guild_join_request = guild_join_request_create(
        actioned_by = actioned_by,
        actioned_at = actioned_at,
        created_at = created_at,
        form_field_responses = form_field_responses,
        guild_id = guild_id,
        guild_join_request_id = guild_join_request_id,
        last_seen_at = last_seen_at,
        rejection_reason = rejection_reason,
        status = status,
        user = user,
    )
    assert_guild_join_request_fields_set(guild_join_request)
    
    vampytest.assert_is(guild_join_request.actioned_by, actioned_by)
    vampytest.assert_eq(guild_join_request.actioned_at, actioned_at)
    vampytest.assert_eq(guild_join_request.created_at, created_at)
    vampytest.assert_eq(guild_join_request.form_field_responses, form_field_responses)
    vampytest.assert_eq(guild_join_request.guild_id, guild_id)
    vampytest.assert_eq(guild_join_request.id, guild_join_request_id)
    vampytest.assert_eq(guild_join_request.last_seen_at, last_seen_at)
    vampytest.assert_eq(guild_join_request.rejection_reason, rejection_reason)
    vampytest.assert_is(guild_join_request.status, status)
    vampytest.assert_is(guild_join_request.user, user)


def test__guild_join_request_create_from_data():
    actioned_by = User.precreate(202305170006, name = 'Koishi')
    actioned_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    created_at = DateTime(2017, 7, 6, tzinfo = TimeZone.utc)
    form_field_responses = (
        guild_join_request_form_field_response_create_boolean_terms(description = 'hey'),
        guild_join_request_form_field_response_create_boolean_terms(description = 'ho'),
    )
    guild_id = 202305170007
    guild_join_request_id = 202610100010
    last_seen_at = DateTime(2018, 4, 4, tzinfo = TimeZone.utc)
    rejection_reason = 'Koishi is better'
    status = GuildJoinRequestStatus.rejected
    user = User.precreate(202305170008, name = 'Koisheep')
    
    data = {
        'actioned_by_user': actioned_by.to_data(defaults = True, include_internals = True),
        'actioned_at': datetime_to_timestamp(actioned_at),
        'created_at': datetime_to_timestamp(created_at),
        'form_responses': [
            guild_join_request_form_field_response_convert_to_data(form_field_response_field, defaults = True)
            for form_field_response_field in form_field_responses
        ],
        'guild_id': str(guild_id),
        'id': str(guild_join_request_id),
        'last_seen': datetime_to_timestamp(last_seen_at),
        'rejection_reason': rejection_reason,
        'application_status': status.value,
        'user': user.to_data(defaults = True, include_internals = True),
        'user_id': str(user.id),
    }
    
    guild_join_request = guild_join_request_create_from_data(data)
    assert_guild_join_request_fields_set(guild_join_request)
    
    vampytest.assert_is(guild_join_request.actioned_by, actioned_by)
    vampytest.assert_eq(guild_join_request.actioned_at, actioned_at)
    vampytest.assert_eq(guild_join_request.created_at, created_at)
    vampytest.assert_eq(guild_join_request.form_field_responses, form_field_responses)
    vampytest.assert_eq(guild_join_request.guild_id, guild_id)
    vampytest.assert_eq(guild_join_request.id, guild_join_request_id)
    vampytest.assert_eq(guild_join_request.last_seen_at, last_seen_at)
    vampytest.assert_eq(guild_join_request.rejection_reason, rejection_reason)
    vampytest.assert_is(guild_join_request.status, status)
    vampytest.assert_is(guild_join_request.user, user)


def test__guild_join_request_convert_to_data():
    actioned_by = User.precreate(202305170009, name = 'Koishi')
    actioned_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    created_at = DateTime(2017, 7, 6, tzinfo = TimeZone.utc)
    form_field_responses = (
        guild_join_request_form_field_response_create_boolean_terms(description = 'hey'),
        guild_join_request_form_field_response_create_boolean_terms(description = 'ho'),
    )
    guild_id = 202305170010
    guild_join_request_id = 202610100011
    last_seen_at = DateTime(2018, 4, 4, tzinfo = TimeZone.utc)
    rejection_reason = 'Koishi is better'
    status = GuildJoinRequestStatus.rejected
    user = User.precreate(202305170011, name = 'Koisheep')
    
    guild_join_request = guild_join_request_create(
        actioned_by = actioned_by,
        actioned_at = actioned_at,
        created_at = created_at,
        form_field_responses = form_field_responses,
        guild_id = guild_id,
        guild_join_request_id = guild_join_request_id,
        last_seen_at = last_seen_at,
        rejection_reason = rejection_reason,
        status = status,
        user = user,
    )
    expected_output = {
        'actioned_by_user': actioned_by.to_data(defaults = True, include_internals = True),
        'actioned_at': datetime_to_timestamp(actioned_at),
        'created_at': datetime_to_timestamp(created_at),
        'form_responses': [
            guild_join_request_form_field_response_convert_to_data(form_field_response_field, defaults = True)
            for form_field_response_field in form_field_responses
        ],
        'guild_id': str(guild_id),
        'id': str(guild_join_request_id),
        'last_seen': datetime_to_timestamp(last_seen_at),
        'rejection_reason': rejection_reason,
        'application_status': status.value,
        'user': user.to_data(defaults = True, include_internals = True),
        'user_id': str(user.id),
    }
    
    vampytest.assert_eq(
        guild_join_request_convert_to_data(guild_join_request, defaults = True),
        expected_output,
    )
