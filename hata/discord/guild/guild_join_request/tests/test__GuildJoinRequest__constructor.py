from datetime import datetime as DateTime

import vampytest

from ....user import ClientUserBase, User

from ...guild_join_request_form_response import GuildJoinRequestFormResponse

from ..guild_join_request import GuildJoinRequest
from ..preinstanced import GuildJoinRequestStatus


def _assert_fields_set(event):
    """
    Checks whether every attribute is set of the given guild join request event.
    
    Parameters
    ----------
    event : ``GuildJoinRequest``
        The event to check.
    """
    vampytest.assert_instance(event, GuildJoinRequest)
    vampytest.assert_instance(event.actioned_by, ClientUserBase, nullable = True)
    vampytest.assert_instance(event.actioned_at, DateTime, nullable = True)
    vampytest.assert_instance(event.created_at, DateTime, nullable = True)
    vampytest.assert_instance(event.form_responses, tuple, nullable = True)
    vampytest.assert_instance(event.guild_id, int)
    vampytest.assert_instance(event.last_seen_at, DateTime, nullable = True)
    vampytest.assert_instance(event.rejection_reason, str, nullable = True)
    vampytest.assert_instance(event.status, GuildJoinRequestStatus)
    vampytest.assert_instance(event.user, ClientUserBase)


def test__GuildJoinRequest__new__0():
    """
    Tests whether ``GuildJoinRequest.__new__`` works as intended.
    
    Case: No fields given.
    """
    event = GuildJoinRequest()
    _assert_fields_set(event)


def test__GuildJoinRequest__new__1():
    """
    Tests whether ``GuildJoinRequest.__new__`` works as intended.
    
    Case: Fields given.
    """
    actioned_by = User.precreate(202305170003, name = 'Koishi')
    actioned_at = DateTime(2016, 5, 14)
    created_at = DateTime(2017, 7, 6)
    form_responses = [GuildJoinRequestFormResponse(), GuildJoinRequestFormResponse()]
    guild_id = 202305170004
    last_seen_at = DateTime(2018, 4, 4)
    rejection_reason = 'Koishi is better'
    status = GuildJoinRequestStatus.rejected
    user = User.precreate(202305170005, name = 'Koisheep')
    
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
