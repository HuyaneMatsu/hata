import vampytest

from ..guild_join_request_form_response import GuildJoinRequestFormResponse


def test__GuildJoinRequestFormResponse__repr():
    """
    Tests whether ``GuildJoinRequestFormResponse.__repr__`` works as intended.
    """
    form_response = GuildJoinRequestFormResponse()
    
    vampytest.assert_instance(repr(form_response), str)


def test__GuildJoinRequestFormResponse__hash():
    """
    Tests whether ``GuildJoinRequestFormResponse.__hash__`` works as intended.
    """
    form_response = GuildJoinRequestFormResponse()
    
    vampytest.assert_instance(hash(form_response), int)



def test__GuildJoinRequestFormResponse__eq():
    """
    Tests whether ``GuildJoinRequestFormResponse.__repr__`` works as intended.
    """
    fields = {}
    
    form_response = GuildJoinRequestFormResponse(**fields)
    
    vampytest.assert_eq(form_response, form_response)
    vampytest.assert_ne(form_response, object())
    
    for field_name, field_value in (
    ):
        test_form_response = GuildJoinRequestFormResponse(**{**fields, field_name: field_value})
        vampytest.assert_ne(form_response, test_form_response)
