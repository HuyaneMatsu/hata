from datetime import datetime as DateTime

import vampytest

from ....user import User

from ...guild_join_request_form_response import GuildJoinRequestFormResponse

from ..guild_join_request import GuildJoinRequest
from ..preinstanced import GuildJoinRequestStatus


def test__GuildJoinRequest__repr():
    """
    Tests whether ``GuildJoinRequest.__repr__`` works as intended.
    """
    actioned_by = User.precreate(202305170012, name = 'Koishi')
    actioned_at = DateTime(2016, 5, 14)
    created_at = DateTime(2017, 7, 6)
    form_responses = [GuildJoinRequestFormResponse(), GuildJoinRequestFormResponse()]
    guild_id = 202305170013
    last_seen_at = DateTime(2018, 4, 4)
    rejection_reason = 'Koishi is better'
    status = GuildJoinRequestStatus.rejected
    user = User.precreate(202305170014, name = 'Koisheep')
    
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
    
    vampytest.assert_instance(repr(event), str)


def test__GuildJoinRequest__hash():
    """
    Tests whether ``GuildJoinRequest.__hash__`` works as intended.
    """
    actioned_by = User.precreate(202305170015, name = 'Koishi')
    actioned_at = DateTime(2016, 5, 14)
    created_at = DateTime(2017, 7, 6)
    form_responses = [GuildJoinRequestFormResponse(), GuildJoinRequestFormResponse()]
    guild_id = 202305170016
    last_seen_at = DateTime(2018, 4, 4)
    rejection_reason = 'Koishi is better'
    status = GuildJoinRequestStatus.rejected
    user = User.precreate(202305170017, name = 'Koisheep')
    
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
    
    vampytest.assert_instance(hash(event), int)


def test__GuildJoinRequest__eq():
    """
    Tests whether ``GuildJoinRequest.__repr__`` works as intended.
    """
    actioned_by = User.precreate(202305170018, name = 'Koishi')
    actioned_at = DateTime(2016, 5, 14)
    created_at = DateTime(2017, 7, 6)
    form_responses = [GuildJoinRequestFormResponse(), GuildJoinRequestFormResponse()]
    guild_id = 202305170019
    last_seen_at = DateTime(2018, 4, 4)
    rejection_reason = 'Koishi is better'
    status = GuildJoinRequestStatus.rejected
    user = User.precreate(202305170020, name = 'Koisheep')
    
    keyword_parameters = {
        'actioned_by': actioned_by,
        'actioned_at': actioned_at,
        'created_at': created_at,
        'form_responses': form_responses,
        'guild_id': guild_id,
        'last_seen_at': last_seen_at,
        'rejection_reason': rejection_reason,
        'status': status,
        'user': user,
    }
    
    event = GuildJoinRequest(**keyword_parameters)
    
    vampytest.assert_eq(event, event)
    vampytest.assert_ne(event, object())
    
    for event_name, event_value in (
        ('actioned_by', None),
        ('actioned_at', None),
        ('created_at', None),
        ('form_responses', None),
        ('guild_id', 202305170021),
        ('last_seen_at', None),
        ('rejection_reason', None),
        ('status', GuildJoinRequestStatus.pending),
        ('user', User.precreate(202305170022, name = 'Satori')),
    ):
        event_altered = GuildJoinRequest(**{**keyword_parameters, event_name: event_value})
        vampytest.assert_ne(event, event_altered)


def test__GuildJoinRequest__unpack():
    """
    Tests whether ``GuildJoinRequest`` unpacking works as intended.
    """
    actioned_by = User.precreate(202305170023, name = 'Koishi')
    actioned_at = DateTime(2016, 5, 14)
    created_at = DateTime(2017, 7, 6)
    form_responses = [GuildJoinRequestFormResponse(), GuildJoinRequestFormResponse()]
    guild_id = 202305170024
    last_seen_at = DateTime(2018, 4, 4)
    rejection_reason = 'Koishi is better'
    status = GuildJoinRequestStatus.rejected
    user = User.precreate(202305170025, name = 'Koisheep')
    
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
    
    vampytest.assert_eq(len([*event]), len(event))
