import vampytest

from ...guild_join_request_form_response import GuildJoinRequestFormResponse

from ..fields import parse_form_responses


def test__parse_form_responses():
    """
    Tests whether ``parse_form_responses`` works as intended.
    """
    form_response_0 = GuildJoinRequestFormResponse()
    form_response_1 = GuildJoinRequestFormResponse()
    
    for input_value, expected_output in (
        ({}, None),
        ({'form_responses': None}, None),
        ({'form_responses': [form_response_0.to_data()]}, (form_response_0, )),
        ({'form_responses': [form_response_0.to_data(), form_response_1.to_data()]}, (form_response_0, form_response_1)),
    ):
        output = parse_form_responses(input_value)
        vampytest.assert_eq(output, expected_output)
