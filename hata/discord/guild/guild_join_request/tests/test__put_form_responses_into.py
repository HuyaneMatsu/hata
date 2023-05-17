import vampytest

from ...guild_join_request_form_response import GuildJoinRequestFormResponse

from ..fields import put_form_responses_into


def test__put_form_responses_into():
    """
    Tests whether ``put_form_responses_into`` works as intended.
    """
    form_response_0 = GuildJoinRequestFormResponse()
    form_response_1 = GuildJoinRequestFormResponse()
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'form_responses': []}),
        ((form_response_0, ), False, {'form_responses': [form_response_0.to_data()]},),
        (
            (form_response_0, form_response_1),
            True,
            {'form_responses': [form_response_0.to_data(defaults = True), form_response_1.to_data(defaults = True)]},
        ),
    ):
        output = put_form_responses_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
