from datetime import datetime as DateTime

import vampytest

from ..guild_incidents import GuildIncidents

from .test__GuildIncidents__constructor import _assert_fields_set


def test__GuildIncidents__copy():
    """
    Tests whether ``GuildIncidents.copy`` works as intended.
    """
    direct_message_spam_detected_at = DateTime(2015, 5, 14)
    direct_messages_disabled_until = DateTime(2016, 5, 14)
    invites_disabled_until = DateTime(2017, 5, 14)
    raid_detected_at = DateTime(2018, 5, 14)
    
    guild_incidents = GuildIncidents(
        direct_message_spam_detected_at = direct_message_spam_detected_at,
        direct_messages_disabled_until = direct_messages_disabled_until,
        invites_disabled_until = invites_disabled_until,
        raid_detected_at = raid_detected_at,
    )
    
    copy = guild_incidents.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, guild_incidents)
    
    vampytest.assert_eq(copy, guild_incidents)


def test__GuildIncidents__copy_with__no_fields():
    """
    Tests whether ``GuildIncidents.copy_with`` works as intended.
    
    Case: No fields given.
    """
    direct_message_spam_detected_at = DateTime(2015, 5, 14)
    direct_messages_disabled_until = DateTime(2016, 5, 14)
    invites_disabled_until = DateTime(2017, 5, 14)
    raid_detected_at = DateTime(2018, 5, 14)
    
    guild_incidents = GuildIncidents(
        direct_message_spam_detected_at = direct_message_spam_detected_at,
        direct_messages_disabled_until = direct_messages_disabled_until,
        invites_disabled_until = invites_disabled_until,
        raid_detected_at = raid_detected_at,
    )
    
    copy = guild_incidents.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, guild_incidents)
    
    vampytest.assert_eq(copy, guild_incidents)


def test__GuildIncidents__copy_with_all_fields1():
    """
    Tests whether ``GuildIncidents.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_direct_message_spam_detected_at = DateTime(2015, 5, 14)
    old_direct_messages_disabled_until = DateTime(2016, 5, 14)
    old_invites_disabled_until = DateTime(2017, 5, 14)
    old_raid_detected_at = DateTime(2018, 5, 14)
    
    new_direct_message_spam_detected_at = DateTime(2015, 5, 15)
    new_direct_messages_disabled_until = DateTime(2016, 5, 11)
    new_invites_disabled_until = DateTime(2017, 5, 15)
    new_raid_detected_at = DateTime(2018, 5, 15)
    
    guild_incidents = GuildIncidents(
        direct_message_spam_detected_at = old_direct_message_spam_detected_at,
        direct_messages_disabled_until = old_direct_messages_disabled_until,
        invites_disabled_until = old_invites_disabled_until,
        raid_detected_at = old_raid_detected_at,
    )
    
    copy = guild_incidents.copy_with(
        direct_message_spam_detected_at = new_direct_message_spam_detected_at,
        direct_messages_disabled_until = new_direct_messages_disabled_until,
        invites_disabled_until = new_invites_disabled_until,
        raid_detected_at = new_raid_detected_at,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, guild_incidents)
    
    vampytest.assert_eq(copy.direct_message_spam_detected_at, new_direct_message_spam_detected_at)
    vampytest.assert_eq(copy.direct_messages_disabled_until, new_direct_messages_disabled_until)
    vampytest.assert_eq(copy.invites_disabled_until, new_invites_disabled_until)
    vampytest.assert_eq(copy.raid_detected_at, new_raid_detected_at)
