from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....guild import Guild
from ....user import User

from ...guild_join_request_form_response import GuildJoinRequestFormResponse

from ..guild_join_request import GuildJoinRequest
from ..preinstanced import GuildJoinRequestStatus

from .test__GuildJoinRequest__constructor import _assert_fields_set


def test__GuildJoinRequest__copy():
    """
    Tests whether ``GuildJoinRequest.copy`` works as intended.
    """
    actioned_by = User.precreate(202305170026, name = 'Koishi')
    actioned_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    created_at = DateTime(2017, 7, 6, tzinfo = TimeZone.utc)
    form_responses = [GuildJoinRequestFormResponse(), GuildJoinRequestFormResponse()]
    guild_id = 202305170027
    last_seen_at = DateTime(2018, 4, 4, tzinfo = TimeZone.utc)
    rejection_reason = 'Koishi is better'
    status = GuildJoinRequestStatus.rejected
    user = User.precreate(202305170028, name = 'Koisheep')
    
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
    
    copy = event.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(event, copy)

    vampytest.assert_eq(event, copy)


def test__GuildJoinRequest__copy_with__0():
    """
    Tests whether ``GuildJoinRequest.copy_with`` works as intended.
    
    Case: no fields given.
    """
    actioned_by = User.precreate(202305170029, name = 'Koishi')
    actioned_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    created_at = DateTime(2017, 7, 6, tzinfo = TimeZone.utc)
    form_responses = [GuildJoinRequestFormResponse(), GuildJoinRequestFormResponse()]
    guild_id = 202305170030
    last_seen_at = DateTime(2018, 4, 4, tzinfo = TimeZone.utc)
    rejection_reason = 'Koishi is better'
    status = GuildJoinRequestStatus.rejected
    user = User.precreate(202305170031, name = 'Koisheep')
    
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
    
    copy = event.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(event, copy)

    vampytest.assert_eq(event, copy)


def test__GuildJoinRequest__copy_with__1():
    """
    Tests whether ``GuildJoinRequest.copy_with`` works as intended.
    
    Case: all fields given.
    """
    old_actioned_by = User.precreate(202305170032, name = 'Koishi')
    old_actioned_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    old_created_at = DateTime(2017, 7, 6, tzinfo = TimeZone.utc)
    old_form_responses = [GuildJoinRequestFormResponse(), GuildJoinRequestFormResponse()]
    old_guild_id = 202305170033
    old_last_seen_at = DateTime(2018, 4, 4, tzinfo = TimeZone.utc)
    old_rejection_reason = 'Koishi is better'
    old_status = GuildJoinRequestStatus.rejected
    old_user = User.precreate(202305170034, name = 'Koisheep')
    
    new_actioned_by = User.precreate(202305170035, name = 'Satori')
    new_actioned_at = DateTime(2016, 5, 13, tzinfo = TimeZone.utc)
    new_created_at = DateTime(2017, 7, 5, tzinfo = TimeZone.utc)
    new_form_responses = [GuildJoinRequestFormResponse()]
    new_guild_id = 202305170036
    new_last_seen_at = DateTime(2018, 4, 12, tzinfo = TimeZone.utc)
    new_rejection_reason = 'Satori is ok'
    new_status = GuildJoinRequestStatus.pending
    new_user = User.precreate(202305170037, name = 'Satosheep')
    
    event = GuildJoinRequest(
        actioned_by = old_actioned_by,
        actioned_at = old_actioned_at,
        created_at = old_created_at,
        form_responses = old_form_responses,
        guild_id = old_guild_id,
        last_seen_at = old_last_seen_at,
        rejection_reason = old_rejection_reason,
        status = old_status,
        user = old_user,
    )
    
    copy = event.copy_with(
        actioned_by = new_actioned_by,
        actioned_at = new_actioned_at,
        created_at = new_created_at,
        form_responses = new_form_responses,
        guild_id = new_guild_id,
        last_seen_at = new_last_seen_at,
        rejection_reason = new_rejection_reason,
        status = new_status,
        user = new_user,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(event, copy)

    vampytest.assert_is(copy.actioned_by, new_actioned_by)
    vampytest.assert_eq(copy.actioned_at, new_actioned_at)
    vampytest.assert_eq(copy.created_at, new_created_at)
    vampytest.assert_eq(copy.form_responses, tuple(new_form_responses))
    vampytest.assert_eq(copy.guild_id, new_guild_id)
    vampytest.assert_eq(copy.last_seen_at, new_last_seen_at)
    vampytest.assert_eq(copy.rejection_reason, new_rejection_reason)
    vampytest.assert_is(copy.status, new_status)
    vampytest.assert_is(copy.user, new_user)


def test__GuildJoinRequest__guild():
    """
    Tests whether ``GuildJoinRequest.guild`` works as intended.
    
    Case: no fields given.
    """
    guild_id_0 = 202305170038
    guild_id_1 = 202305170039
    
    for input_value, expected_output in (
        (0, None),
        (guild_id_0, None),
        (guild_id_1, Guild.precreate(guild_id_1)),
    ):
        event = GuildJoinRequest(
            guild_id = input_value,
        )
        
        vampytest.assert_is(event.guild, expected_output)


def test__GuildJoinRequest__user():
    """
    Tests whether ``GuildJoinRequest.user`` works as intended.
    
    Case: no fields given.
    """
    user_id = 202305170040
    user = User.precreate(user_id, name = 'Koishi')
    
    event = GuildJoinRequest(
        user = user,
    )
    
    output = event.user_id
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, user_id)


def test__GuildJoinRequest__iter_form_responses():
    """
    Tests whether ``GuildJoinRequest.iter_form_responses`` works as intended.
    """
    form_responses_0 = GuildJoinRequestFormResponse()
    form_responses_1 = GuildJoinRequestFormResponse()
    
    for input_value, expected_output in (
        (None, []),
        ([form_responses_1], [form_responses_1]),
        ([form_responses_0, form_responses_1], [form_responses_0, form_responses_1]),
    ):
        event = GuildJoinRequest(form_responses = input_value)
        output = [*event.iter_form_responses()]
        vampytest.assert_eq(output, expected_output)
