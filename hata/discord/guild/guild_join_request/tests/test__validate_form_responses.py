import vampytest

from ...guild_join_request_form_response import GuildJoinRequestFormResponse

from ..fields import validate_form_responses


def test__validate_form_responses__0():
    """
    Tests whether ``validate_form_responses`` works as intended.
    
    Case: passing.
    """
    form_response_0 = GuildJoinRequestFormResponse()
    form_response_1 = GuildJoinRequestFormResponse()
    
    for input_value, expected_output in (
        (None, None),
        ([], None),
        ([form_response_0], (form_response_0, )),
        ([form_response_0, form_response_1], (form_response_0, form_response_1)),
    ):
        output = validate_form_responses(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_form_responses__1():
    """
    Tests whether ``validate_form_responses`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
        [12.6],
    ):
        with vampytest.assert_raises(TypeError):
            validate_form_responses(input_value)
