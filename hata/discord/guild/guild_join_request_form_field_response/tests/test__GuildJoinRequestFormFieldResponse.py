import vampytest

from ..guild_join_request_form_field_response import (
    GuildJoinRequestFormFieldResponse, guild_join_request_form_field_response_convert_to_data,
    guild_join_request_form_field_response_create_boolean_terms,
    guild_join_request_form_field_response_create_choice_single,
    guild_join_request_form_field_response_create_from_data, guild_join_request_form_field_response_create_text_input
)
from ..metadata import (
    GuildJoinRequestFormFieldResponseMetadataBase, GuildJoinRequestFormFieldResponseMetadataBooleanTerms,
    GuildJoinRequestFormFieldResponseMetadataChoiceSingle, GuildJoinRequestFormFieldResponseMetadataTextInput
)
from ..preinstanced import GuildJoinRequestFormFieldTextInputStyle, GuildJoinRequestFormFieldType


def assert_guild_join_request_form_field_response_fields_set(guild_join_request_form_field_type):
    vampytest.assert_instance(guild_join_request_form_field_type, GuildJoinRequestFormFieldResponse)
    vampytest.assert_instance(guild_join_request_form_field_type.description, str, nullable = True)
    metadata = guild_join_request_form_field_type.metadata
    vampytest.assert_instance(metadata, GuildJoinRequestFormFieldResponseMetadataBase)
    vampytest.assert_instance(guild_join_request_form_field_type.required, bool)
    vampytest.assert_instance(guild_join_request_form_field_type.title, str, nullable = True)
    field_type = guild_join_request_form_field_type.type
    vampytest.assert_instance(field_type, GuildJoinRequestFormFieldType)
    
    if (field_type is GuildJoinRequestFormFieldType.boolean_terms):
        vampytest.assert_instance(metadata, GuildJoinRequestFormFieldResponseMetadataBooleanTerms)
        vampytest.assert_instance(metadata.accepted, bool)
        vampytest.assert_instance(metadata.terms, tuple, nullable = True)
    elif (
        (guild_join_request_form_field_type is GuildJoinRequestFormFieldType.text_input_short) or
        (guild_join_request_form_field_type is GuildJoinRequestFormFieldType.text_input_paragraph)
    ):
        vampytest.assert_instance(metadata, GuildJoinRequestFormFieldResponseMetadataTextInput)
        vampytest.assert_instance(metadata.accepted, bool)
        vampytest.assert_instance(metadata.terms, tuple, nullable = True)

    elif (guild_join_request_form_field_type is GuildJoinRequestFormFieldType.choice_single):
        vampytest.assert_instance(metadata, GuildJoinRequestFormFieldResponseMetadataChoiceSingle)
        vampytest.assert_instance(metadata.choice_index, int)
        vampytest.assert_instance(metadata.choices, tuple, nullable = True)
    
    else:
        # No other cases
        pass


def test__guild_join_request_form_field_response_create_from_data__boolean_terms():
    description = 'nue'
    required = False
    title = 'murasa'
    field_type = GuildJoinRequestFormFieldType.boolean_terms
    accepted = True
    terms = ('hey', 'mister')
    
    data = {
        'description': description,
        'required': required,
        'label': title,
        'type': field_type,
        'response': accepted,
        'values': [*terms],
    }
    
    guild_join_request_form_field_type = guild_join_request_form_field_response_create_from_data(data)
    assert_guild_join_request_form_field_response_fields_set(guild_join_request_form_field_type)
    
    vampytest.assert_eq(guild_join_request_form_field_type.description, description)
    vampytest.assert_eq(guild_join_request_form_field_type.required, required)
    vampytest.assert_eq(guild_join_request_form_field_type.title, title)
    vampytest.assert_eq(guild_join_request_form_field_type.type, field_type)
    vampytest.assert_eq(guild_join_request_form_field_type.accepted, accepted)
    vampytest.assert_eq(guild_join_request_form_field_type.terms, terms)


def test__guild_join_request_form_field_response_create_from_data__text_input_short():
    field_type = GuildJoinRequestFormFieldType.text_input_short
    placeholder = 'hey'
    value = 'mister'
    
    data = {
        'type': field_type,
        'placeholder': placeholder,
        'response': value,
    }
    
    guild_join_request_form_field_type = guild_join_request_form_field_response_create_from_data(data)
    assert_guild_join_request_form_field_response_fields_set(guild_join_request_form_field_type)
    
    vampytest.assert_eq(guild_join_request_form_field_type.type, field_type)
    vampytest.assert_eq(guild_join_request_form_field_type.placeholder, placeholder)
    vampytest.assert_eq(guild_join_request_form_field_type.value, value)


def test__guild_join_request_form_field_response_create_from_data__choice_single():
    field_type = GuildJoinRequestFormFieldType.choice_single
    choice_index = 1
    choices = ('hey', 'mister')
    
    data = {
        'type': field_type,
        'response': choice_index,
        'choices': [*choices],
    }
    
    guild_join_request_form_field_type = guild_join_request_form_field_response_create_from_data(data)
    assert_guild_join_request_form_field_response_fields_set(guild_join_request_form_field_type)
    
    vampytest.assert_eq(guild_join_request_form_field_type.type, field_type)
    vampytest.assert_eq(guild_join_request_form_field_type.choice_index, choice_index)
    vampytest.assert_eq(guild_join_request_form_field_type.choices, choices)


def test__guild_join_request_form_field_response_create_boolean_terms__no_fields():
    guild_join_request_form_field_type = guild_join_request_form_field_response_create_boolean_terms()
    assert_guild_join_request_form_field_response_fields_set(guild_join_request_form_field_type)


def test__guild_join_request_form_field_response_create_boolean_terms__all_fields():
    description = 'nue'
    required = False
    title = 'murasa'
    accepted = True
    terms = ('hey', 'mister')
    
    guild_join_request_form_field_type = guild_join_request_form_field_response_create_boolean_terms(
        description = description,
        required = required,
        title = title,
        accepted = accepted,
        terms = terms,
    )
    assert_guild_join_request_form_field_response_fields_set(guild_join_request_form_field_type)
    
    vampytest.assert_eq(guild_join_request_form_field_type.description, description)
    vampytest.assert_eq(guild_join_request_form_field_type.required, required)
    vampytest.assert_eq(guild_join_request_form_field_type.title, title)
    vampytest.assert_eq(guild_join_request_form_field_type.type, GuildJoinRequestFormFieldType.boolean_terms)
    vampytest.assert_eq(guild_join_request_form_field_type.accepted, accepted)
    vampytest.assert_eq(guild_join_request_form_field_type.terms, terms)


def test__guild_join_request_form_field_response_create_text_input__no_fields():
    guild_join_request_form_field_type = guild_join_request_form_field_response_create_text_input()
    assert_guild_join_request_form_field_response_fields_set(guild_join_request_form_field_type)


def test__guild_join_request_form_field_response_create_text_input__all_fields():
    description = 'nue'
    required = False
    title = 'murasa'
    placeholder = 'hey'
    value = 'mister'
    
    guild_join_request_form_field_type = guild_join_request_form_field_response_create_text_input(
        description = description,
        required = required,
        title = title,
        placeholder = placeholder,
        value = value,
        style = GuildJoinRequestFormFieldTextInputStyle.paragraph,
    )
    assert_guild_join_request_form_field_response_fields_set(guild_join_request_form_field_type)
    
    vampytest.assert_eq(guild_join_request_form_field_type.description, description)
    vampytest.assert_eq(guild_join_request_form_field_type.required, required)
    vampytest.assert_eq(guild_join_request_form_field_type.title, title)
    vampytest.assert_eq(guild_join_request_form_field_type.type, GuildJoinRequestFormFieldType.text_input_paragraph)
    vampytest.assert_eq(guild_join_request_form_field_type.placeholder, placeholder)
    vampytest.assert_eq(guild_join_request_form_field_type.value, value)
    

def test__guild_join_request_form_field_response_create_choice_single__no_fields():
    guild_join_request_form_field_type = guild_join_request_form_field_response_create_choice_single()
    assert_guild_join_request_form_field_response_fields_set(guild_join_request_form_field_type)
    

def test__guild_join_request_form_field_response_create_choice_single__all_fields():
    description = 'nue'
    required = False
    title = 'murasa'
    choice_index = 1
    choices = ('hey', 'mister')
    
    guild_join_request_form_field_type = guild_join_request_form_field_response_create_choice_single(
        description = description,
        required = required,
        title = title,
        choice_index = choice_index,
        choices = choices,
    )
    assert_guild_join_request_form_field_response_fields_set(guild_join_request_form_field_type)
    
    vampytest.assert_eq(guild_join_request_form_field_type.description, description)
    vampytest.assert_eq(guild_join_request_form_field_type.required, required)
    vampytest.assert_eq(guild_join_request_form_field_type.title, title)
    vampytest.assert_eq(guild_join_request_form_field_type.type, GuildJoinRequestFormFieldType.choice_single)
    vampytest.assert_eq(guild_join_request_form_field_type.choice_index, choice_index)
    vampytest.assert_eq(guild_join_request_form_field_type.choices, choices)


def test__guild_join_request_form_field_response_convert_to_data__boolean_terms():
    description = 'nue'
    required = False
    title = 'murasa'
    accepted = True
    terms = ('hey', 'mister')
    
    guild_join_request_form_field_type = guild_join_request_form_field_response_create_boolean_terms(
        description = description,
        required = required,
        title = title,
        accepted = accepted,
        terms = terms,
    )
    
    vampytest.assert_eq(
        guild_join_request_form_field_response_convert_to_data(guild_join_request_form_field_type),
        {
            'description': description,
            'required': required,
            'label': title,
            'type': GuildJoinRequestFormFieldType.boolean_terms.value,
            'response': accepted,
            'values': [*terms],
        },
    )


def test__guild_join_request_form_field_response_convert_to_data__text_input():
    description = 'nue'
    required = False
    title = 'murasa'
    placeholder = 'hey'
    value = 'mister'
    
    guild_join_request_form_field_type = guild_join_request_form_field_response_create_text_input(
        description = description,
        required = required,
        title = title,
        placeholder = placeholder,
        value = value,
        style = GuildJoinRequestFormFieldTextInputStyle.paragraph,
    )
    
    vampytest.assert_eq(
        guild_join_request_form_field_response_convert_to_data(guild_join_request_form_field_type),
        {
            'description': description,
            'required': required,
            'label': title,
            'type': GuildJoinRequestFormFieldType.text_input_paragraph.value,
            'placeholder': placeholder,
            'response': value,
        },
    )
    

def test__guild_join_request_form_field_response_convert_to_data__choice_single():
    description = 'nue'
    required = False
    title = 'murasa'
    choice_index = 1
    choices = ('hey', 'mister')
    
    guild_join_request_form_field_type = guild_join_request_form_field_response_create_choice_single(
        description = description,
        required = required,
        title = title,
        choice_index = choice_index,
        choices = choices,
    )
    
    vampytest.assert_eq(
        guild_join_request_form_field_response_convert_to_data(guild_join_request_form_field_type),
        {
            'description': description,
            'required': required,
            'label': title,
            'type': GuildJoinRequestFormFieldType.choice_single.value,
            'response': choice_index,
            'choices': [*choices],
        },
    )
