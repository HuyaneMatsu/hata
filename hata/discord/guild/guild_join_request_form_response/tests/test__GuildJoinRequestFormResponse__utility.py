import vampytest

from ..guild_join_request_form_response import GuildJoinRequestFormResponse

from .test__GuildJoinRequestFormResponse__constructor import _assert_fields_set


def test__GuildJoinRequestFormResponse__copy():
    """
    Tests whether ``GuildJoinRequestFormResponse.copy`` works as intended.
    """
    form_response = GuildJoinRequestFormResponse()
    copy = form_response.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(form_response, copy)

    vampytest.assert_eq(form_response, copy)



def test__GuildJoinRequestFormResponse__copy_with__0():
    """
    Tests whether ``GuildJoinRequestFormResponse.copy_with`` works as intended.
    
    Case: no fields given.
    """
    form_response = GuildJoinRequestFormResponse()
    copy = form_response.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(form_response, copy)

    vampytest.assert_eq(form_response, copy)
