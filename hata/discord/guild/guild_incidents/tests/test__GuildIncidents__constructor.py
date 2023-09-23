from datetime import datetime as DateTime

import vampytest

from ..guild_incidents import GuildIncidents


def _assert_fields_set(guild_incidents):
    """
    Asserts whether every fields are set of the guild guild incidents.
    
    Parameters
    ----------
    guild_incidents : ``GuildIncidents`
        The guild incidents to check.
    """
    vampytest.assert_instance(guild_incidents, GuildIncidents)
    vampytest.assert_instance(guild_incidents.direct_message_spam_detected_at, DateTime, nullable = True)
    vampytest.assert_instance(guild_incidents.direct_messages_disabled_until, DateTime, nullable = True)
    vampytest.assert_instance(guild_incidents.invites_disabled_until, DateTime, nullable = True)
    vampytest.assert_instance(guild_incidents.raid_detected_at, DateTime, nullable = True)


def test__GuildIncidents__new__no_fields():
    """
    Tests whether ``GuildIncidents.__new__`` works as intended.
    
    Case: No fields given.
    """
    guild_incidents = GuildIncidents()
    _assert_fields_set(guild_incidents)


def test__GuildIncidents__new__all_fields():
    """
    Tests whether ``GuildIncidents.__new__`` works as intended.
    
    Case: All fields given.
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
    _assert_fields_set(guild_incidents)
    
    vampytest.assert_eq(guild_incidents.direct_message_spam_detected_at, direct_message_spam_detected_at)
    vampytest.assert_eq(guild_incidents.direct_messages_disabled_until, direct_messages_disabled_until)
    vampytest.assert_eq(guild_incidents.invites_disabled_until, invites_disabled_until)
    vampytest.assert_eq(guild_incidents.raid_detected_at, raid_detected_at)
