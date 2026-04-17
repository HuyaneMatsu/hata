import vampytest

from ..guild_join_request_form_response import GuildJoinRequestFormResponse

from .test__GuildJoinRequestFormResponse__constructor import _assert_fields_set


def test__GuildJoinRequestFormResponse__from_data__0():
    """
    Tests whether ``GuildJoinRequestFormResponse.from_data`` works as intended.
    
    Case: all fields given.
    """
    data = {}
    
    form_response = GuildJoinRequestFormResponse.from_data(data)
    _assert_fields_set(form_response)


def test__GuildJoinRequestFormResponse__to_data__0():
    """
    Tests whether ``GuildJoinRequestFormResponse.to_data`` works as intended.
    
    Case: Include defaults.
    """
    form_response = GuildJoinRequestFormResponse()
    
    expected_output = {}
    
    vampytest.assert_eq(
        form_response.to_data(defaults = True),
        expected_output,
    )
