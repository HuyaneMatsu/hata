from datetime import datetime as DateTime

import vampytest

from ..guild_incidents import GuildIncidents


def test__GuildIncidents__repr():
    """
    Tests whether ``GuildIncidents.__repr__`` works as intended.
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
    
    vampytest.assert_instance(repr(guild_incidents), str)


def test__GuildIncidents__hash():
    """
    Tests whether ``GuildIncidents.__hash__`` works as intended.
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
    
    vampytest.assert_instance(hash(guild_incidents), int)


def test__GuildIncidents__eq():
    """
    Tests whether ``GuildIncidents.__eq__`` works as intended.
    """
    direct_message_spam_detected_at = DateTime(2015, 5, 14)
    direct_messages_disabled_until = DateTime(2016, 5, 14)
    invites_disabled_until = DateTime(2017, 5, 14)
    raid_detected_at = DateTime(2018, 5, 14)
    
    keyword_parameters = {
        'direct_message_spam_detected_at': direct_message_spam_detected_at,
        'direct_messages_disabled_until': direct_messages_disabled_until,
        'invites_disabled_until': invites_disabled_until,
        'raid_detected_at': raid_detected_at,
    }
    
    guild_incidents = GuildIncidents(**keyword_parameters)
    
    vampytest.assert_eq(guild_incidents, guild_incidents)
    vampytest.assert_ne(guild_incidents, object())
    
    for field_name, field_value in (
        ('direct_message_spam_detected_at', DateTime(2015, 5, 15)),
        ('direct_messages_disabled_until', DateTime(2016, 5, 15)),
        ('invites_disabled_until', DateTime(2017, 5, 15)),
        ('raid_detected_at', DateTime(2018, 5, 15)),
    ):
        test_guild_incidents = GuildIncidents(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(guild_incidents, test_guild_incidents)


def _iter_options__bool():
    until = DateTime(2016, 5, 14)
    
    yield GuildIncidents(), False
    yield GuildIncidents(direct_message_spam_detected_at = until), True
    yield GuildIncidents(direct_messages_disabled_until = until), True
    yield GuildIncidents(invites_disabled_until = until), True
    yield GuildIncidents(raid_detected_at = until), True


@vampytest._(vampytest.call_from(_iter_options__bool()).returning_last())
def test__GuildIncidents__bool(guild_incidents):
    """
    Tests whether ``GuildIncidents.__bool__`` works as intended.
    
    Parameters
    ----------
    guild_incidents : ``GuildIncidents``
        The guild incidents to get its boolean value of.
    
    Returns
    -------
    output : `bool`
    """
    output = bool(guild_incidents)
    vampytest.assert_instance(output, bool)
    return output
