import vampytest

from ..preinstanced import GuildJoinRequestStatus


def _assert_fields_set(guild_join_request_status):
    """
    Asserts whether every field are set of the given guild join request status.
    
    Parameters
    ----------
    guild_join_request_status : ``GuildJoinRequestStatus``
        The instance to test.
    """
    vampytest.assert_instance(guild_join_request_status, GuildJoinRequestStatus)
    vampytest.assert_instance(guild_join_request_status.name, str)
    vampytest.assert_instance(guild_join_request_status.value, GuildJoinRequestStatus.VALUE_TYPE)


@vampytest.call_from(GuildJoinRequestStatus.INSTANCES.values())
def test__GuildJoinRequestStatus__instances(instance):
    """
    Tests whether ``GuildJoinRequestStatus`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``GuildJoinRequestStatus``
        The instance to test.
    """
    _assert_fields_set(instance)


def test__GuildJoinRequestStatus__new__min_fields():
    """
    Tests whether ``GuildJoinRequestStatus.__new__`` works as intended.
    
    Case: minimal amount of fields given.
    """
    value = 'Crash_Loop_Backoff'
    
    try:
        output = GuildJoinRequestStatus(value)
        _assert_fields_set(output)
        
        vampytest.assert_eq(output.value, value)
        vampytest.assert_eq(output.name, 'crash loop backoff')
        vampytest.assert_is(GuildJoinRequestStatus.INSTANCES.get(value, None), output)
    
    finally:
        try:
            del GuildJoinRequestStatus.INSTANCES[value]
        except KeyError:
            pass
