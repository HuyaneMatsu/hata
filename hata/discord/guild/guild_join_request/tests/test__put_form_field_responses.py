import vampytest

from ...guild_join_request_form_field_response import (
    guild_join_request_form_field_response_convert_to_data, guild_join_request_form_field_response_create_boolean_terms
)

from ..fields import put_form_field_responses


def _iter_options():
    form_field_responses = (
        guild_join_request_form_field_response_create_boolean_terms(description = 'hey'),
        guild_join_request_form_field_response_create_boolean_terms(description = 'ho'),
    )
    
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'form_responses': [],
        },
    )
    
    yield (
        form_field_responses,
        False,
        {
            'form_responses': [
                guild_join_request_form_field_response_convert_to_data(form_field_response, defaults = False)
                for form_field_response in form_field_responses
            ],
        },
    )
    
    yield (
        form_field_responses,
        True,
        {
            'form_responses': [
                guild_join_request_form_field_response_convert_to_data(form_field_response, defaults = True)
                for form_field_response in form_field_responses
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_form_field_responses(inout_data, defaults):
    return put_form_field_responses(inout_data, {}, defaults)
