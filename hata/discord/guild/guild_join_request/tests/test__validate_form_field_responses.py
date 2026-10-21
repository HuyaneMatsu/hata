import vampytest

from ...guild_join_request_form_field_response import (
    GuildJoinRequestFormFieldResponse, guild_join_request_form_field_response_create_boolean_terms
)

from ..fields import validate_form_field_responses


def _iter_options():
    form_field_responses = (
        guild_join_request_form_field_response_create_boolean_terms(description = 'hey'),
        guild_join_request_form_field_response_create_boolean_terms(description = 'ho'),
    )
    
    yield (
        None,
        None,
    )
    
    
    yield (
        (),
        None,
    )
    
    yield (
        form_field_responses,
        form_field_responses,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_form_field_responses(input_value):
    output = validate_form_field_responses(input_value)
    
    vampytest.assert_instance(output, tuple, nullable = True)
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, GuildJoinRequestFormFieldResponse)
    
    return output
