from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....utils import datetime_to_timestamp

from ..guild_incidents import GuildIncidents

from .test__GuildIncidents__constructor import _assert_fields_set


def test__GuildIncidents__from_data():
    """
    Tests whether ``GuildIncidents.from_data`` works as intended.
    
    Case: All fields given.
    """
    direct_message_spam_detected_at = DateTime(2015, 5, 14, tzinfo = TimeZone.utc)
    direct_messages_disabled_until = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    invites_disabled_until = DateTime(2017, 5, 14, tzinfo = TimeZone.utc)
    raid_detected_at = DateTime(2018, 5, 14, tzinfo = TimeZone.utc)
    
    data = {
        'dm_spam_detected_at': datetime_to_timestamp(direct_message_spam_detected_at),
        'dms_disabled_until': datetime_to_timestamp(direct_messages_disabled_until),
        'invites_disabled_until': datetime_to_timestamp(invites_disabled_until),
        'raid_detected_at': datetime_to_timestamp(raid_detected_at),
    }
    
    guild_incidents = GuildIncidents.from_data(data)
    _assert_fields_set(guild_incidents)
    
    vampytest.assert_eq(guild_incidents.direct_message_spam_detected_at, direct_message_spam_detected_at)
    vampytest.assert_eq(guild_incidents.direct_messages_disabled_until, direct_messages_disabled_until)
    vampytest.assert_eq(guild_incidents.invites_disabled_until, invites_disabled_until)
    vampytest.assert_eq(guild_incidents.raid_detected_at, raid_detected_at)


def test__GuildIncidents__to_data():
    """
    Tests whether ``GuildIncidents.to_data`` works as intended.
    
    Case: Include defaults and internals.
    """
    direct_message_spam_detected_at = DateTime(2015, 5, 14, tzinfo = TimeZone.utc)
    direct_messages_disabled_until = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    invites_disabled_until = DateTime(2017, 5, 14, tzinfo = TimeZone.utc)
    raid_detected_at = DateTime(2018, 5, 14, tzinfo = TimeZone.utc)
    
    guild_incidents = GuildIncidents(
        direct_message_spam_detected_at = direct_message_spam_detected_at,
        direct_messages_disabled_until = direct_messages_disabled_until,
        invites_disabled_until = invites_disabled_until,
        raid_detected_at = raid_detected_at,
    )
    
    expected_output = {
        'dm_spam_detected_at': datetime_to_timestamp(direct_message_spam_detected_at),
        'dms_disabled_until': datetime_to_timestamp(direct_messages_disabled_until),
        'invites_disabled_until': datetime_to_timestamp(invites_disabled_until),
        'raid_detected_at': datetime_to_timestamp(raid_detected_at),
    }
    
    vampytest.assert_eq(
        guild_incidents.to_data(defaults = True, include_internals = True),
        expected_output,
    )
