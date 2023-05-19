import vampytest

from ..guild_join_request_form_response import GuildJoinRequestFormResponse


def _assert_fields_set(form_response):
    """
    Checks whether every attribute is set of the given guild join request form response.
    
    Parameters
    ----------
    form_response : ``GuildJoinRequestFormResponse``
        The field to check.
    """
    vampytest.assert_instance(form_response, GuildJoinRequestFormResponse)


def test__GuildJoinRequestFormResponse__new__0():
    """
    Tests whether ``GuildJoinRequestFormResponse.__new__`` works as intended.
    
    Case: No fields given.
    """
    form_response = GuildJoinRequestFormResponse()
    _assert_fields_set(form_response)
