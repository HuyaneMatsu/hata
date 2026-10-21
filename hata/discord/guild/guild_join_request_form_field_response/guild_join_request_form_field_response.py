__all__ = (
    'GuildJoinRequestFormFieldResponse', 'guild_join_request_form_field_response_convert_to_data',
    'guild_join_request_form_field_response_create_boolean_terms',
    'guild_join_request_form_field_response_create_choice_single',
    'guild_join_request_form_field_response_create_from_data',
    'guild_join_request_form_field_response_create_text_input'
)

from scarletio import RichType, copy_docs

from .fields import (
    parse_accepted, parse_choice_index, parse_choices, parse_description, parse_placeholder, parse_required,
    parse_terms, parse_title, parse_type, parse_value, put_accepted, put_choice_index, put_choices, put_description,
    put_placeholder, put_required, put_terms, put_title, put_type, put_value, validate_accepted, validate_choice_index,
    validate_choices, validate_description, validate_placeholder, validate_required, validate_terms,
    validate_text_input_style, validate_title, validate_value
)
from .metadata import (
    GuildJoinRequestFormFieldResponseMetadataBase, GuildJoinRequestFormFieldResponseMetadataBooleanTerms,
    GuildJoinRequestFormFieldResponseMetadataChoiceSingle, GuildJoinRequestFormFieldResponseMetadataTextInput
)
from .preinstanced import GuildJoinRequestFormFieldTextInputStyle, GuildJoinRequestFormFieldType


class GuildJoinRequestFormFieldResponse(metaclass = RichType, rich_type_feature_flags = ~0):
    """
    A guild join request's form field's response.
    
    Attributes
    ----------
    description : `None | str`
        Description of the field.
    
    metadata : ``GuildJoinRequestFormFieldResponseMetadataBase``
        Additional metadata.
    
    required : `bool`
        Whether the field is required.
    
    title : `None | str`
        Title of the field.
    
    type : ``GuildJoinRequestFormFieldType``
        The field's type.
    """
    __slots__ = ('description', 'metadata', 'required', 'title', 'type')
    
    
    # Field proxies
    
    # accepted
    
    @property
    @copy_docs(GuildJoinRequestFormFieldResponseMetadataBase.accepted)
    def accepted(self):
        return self.metadata.accepted
    
    @accepted.setter
    def accepted(self, accepted):
        self.metadata.accepted = validate_accepted(accepted)
    
    
    # terms
    
    @property
    @copy_docs(GuildJoinRequestFormFieldResponseMetadataBase.terms)
    def terms(self):
        return self.metadata.terms
    
    @terms.setter
    def terms(self, terms):
        self.metadata.terms = validate_terms(terms)
    
    
    # placeholder
    
    @property
    @copy_docs(GuildJoinRequestFormFieldResponseMetadataBase.placeholder)
    def placeholder(self):
        return self.metadata.placeholder
    
    @placeholder.setter
    def placeholder(self, placeholder):
        self.metadata.placeholder = validate_placeholder(placeholder)
    
    
    # value
    
    @property
    @copy_docs(GuildJoinRequestFormFieldResponseMetadataBase.value)
    def value(self):
        return self.metadata.value
    
    @value.setter
    def value(self, value):
        self.metadata.value = validate_value(value)
    
    
    # choice_index
    
    @property
    @copy_docs(GuildJoinRequestFormFieldResponseMetadataBase.choice_index)
    def choice_index(self):
        return self.metadata.choice_index
    
    @choice_index.setter
    def choice_index(self, choice_index):
        self.metadata.choice_index = validate_choice_index(choice_index)
    
    
    # choices
    
    @property
    @copy_docs(GuildJoinRequestFormFieldResponseMetadataBase.choices)
    def choices(self):
        return self.metadata.choices
    
    @choices.setter
    def choices(self, choices):
        self.metadata.choices = validate_choices(choices)


def guild_join_request_form_field_response_create_from_data(data):
    """
    Creates a new guild join request form field response instance from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`.
        Form field response data.
    
    Returns
    -------
    guild_join_request_form_field_response : ``GuildJoinRequestFormFieldResponse``
    """
    guild_join_request_form_field_response = object.__new__(GuildJoinRequestFormFieldResponse)
    guild_join_request_form_field_response.description = parse_description(data)
    guild_join_request_form_field_response.required = parse_required(data)
    guild_join_request_form_field_response.title = parse_title(data)
    guild_join_request_form_field_type = parse_type(data)
    guild_join_request_form_field_response.type = guild_join_request_form_field_type
    if guild_join_request_form_field_type is GuildJoinRequestFormFieldType.boolean_terms:
        metadata = object.__new__(GuildJoinRequestFormFieldResponseMetadataBooleanTerms)
        metadata.accepted = parse_accepted(data)
        metadata.terms = parse_terms(data)
    elif (
        (guild_join_request_form_field_type is GuildJoinRequestFormFieldType.text_input_short) or
        (guild_join_request_form_field_type is GuildJoinRequestFormFieldType.text_input_paragraph)
    ):
        metadata = object.__new__(GuildJoinRequestFormFieldResponseMetadataTextInput)
        metadata.placeholder = parse_placeholder(data)
        metadata.value = parse_value(data)
    elif (guild_join_request_form_field_type is GuildJoinRequestFormFieldType.choice_single):
        metadata = object.__new__(GuildJoinRequestFormFieldResponseMetadataChoiceSingle)
        metadata.choice_index = parse_choice_index(data)
        metadata.choices = parse_choices(data)
    else:
        metadata = object.__new__(GuildJoinRequestFormFieldResponseMetadataBase)
    guild_join_request_form_field_response.metadata = metadata
    
    return guild_join_request_form_field_response


def guild_join_request_form_field_response_convert_to_data(guild_join_request_form_field_response, *, defaults = False):
    """
    Converts the guild join request form field response into a json serializable object.
    
    Parameters
    ----------
    guild_join_request_form_field_response : ``GuildJoinRequestFormFieldResponse``
        The instance to serialise.
    
    defaults : `bool` = `False`, Optional (Keyword only)
        Whether default field values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    data = {}
    put_description(guild_join_request_form_field_response.description, data, defaults)
    put_required(guild_join_request_form_field_response.required, data, defaults)
    put_title(guild_join_request_form_field_response.title, data, defaults)
    guild_join_request_form_field_type = guild_join_request_form_field_response.type
    put_type(guild_join_request_form_field_type, data, defaults)
    metadata = guild_join_request_form_field_response.metadata
    if guild_join_request_form_field_type is GuildJoinRequestFormFieldType.boolean_terms:
        put_accepted(metadata.accepted, data, defaults)
        put_terms(metadata.terms, data, defaults)
    elif (
        (guild_join_request_form_field_type is GuildJoinRequestFormFieldType.text_input_short) or
        (guild_join_request_form_field_type is GuildJoinRequestFormFieldType.text_input_paragraph)
    ):
        put_placeholder(metadata.placeholder, data, defaults)
        put_value(metadata.value, data, defaults)
    elif (guild_join_request_form_field_type is GuildJoinRequestFormFieldType.choice_single):
        put_choice_index(metadata.choice_index, data, defaults)
        put_choices(metadata.choices, data, defaults)
    
    return data


def guild_join_request_form_field_response_create_boolean_terms(
    *,
    accepted = ...,
    description = ...,
    required = ...,
    terms = ...,
    title = ...,
):
    """
    Creates a new guild join form field response of type boolean terms.
    
    Parameters
    ----------
    accepted : `bool`
        Whether the terms have been accepted.
    
    description : `None | str`
        Description of the field.
    
    required : `bool`
        Whether the field is required.
    
    terms : `None | iterable<str>`
        The accepted terms.
    
    title : `None | str`
        Title of the field.
    
    Returns
    -------
    guild_join_request_form_field_response : ``GuildJoinRequestFormFieldResponse``
    
    Raises
    ------
    TypeError
        - If a parameter's type is incorrect.
    ValueError
        - If a parameter's value is incorrect.
    """
    # accepted
    if accepted is ...:
        accepted = False
    else:
        accepted = validate_accepted(accepted)
    
    # description
    if description is ...:
        description = None
    else:
        description = validate_description(description)
    
    # required
    if required is ...:
        required = False
    else:
        required = validate_required(required)
    
    # terms
    if terms is ...:
        terms = None
    else:
        terms = validate_terms(terms)
    
    # title
    if title is ...:
        title = None
    else:
        title = validate_title(title)
    
    guild_join_request_form_field_response = object.__new__(GuildJoinRequestFormFieldResponse)
    guild_join_request_form_field_response.type = GuildJoinRequestFormFieldType.boolean_terms
    guild_join_request_form_field_response.description = description
    guild_join_request_form_field_response.required = required
    guild_join_request_form_field_response.title = title
    metadata = object.__new__(GuildJoinRequestFormFieldResponseMetadataBooleanTerms)
    metadata.accepted = accepted
    metadata.terms = terms
    guild_join_request_form_field_response.metadata = metadata
    return guild_join_request_form_field_response


def guild_join_request_form_field_response_create_text_input(
    *,
    description = ...,
    placeholder = ...,
    required = ...,
    style = ...,
    title = ...,
    value = ...,
):
    """
    Creates a new guild join form field response of type boolean terms.
    
    Parameters
    ----------
    description : `None | str`
        Description of the field.
    
    placeholder : `None | str`
        Placeholder text show inside the input.
    
    required : `bool`
        Whether the field is required.
    
    terms : `None | iterable<str>`
        The accepted terms.
    
    style : ``GuildJoinRequestFormFieldTextInputStyle``
        The style of the text input.
    
    title : `None | str`
        Title of the field.
    
    value : `None | str`
        The value inputted by the user.
    
    Returns
    -------
    guild_join_request_form_field_response : ``GuildJoinRequestFormFieldResponse``
    
    Raises
    ------
    TypeError
        - If a parameter's type is incorrect.
    ValueError
        - If a parameter's value is incorrect.
    """
    # description
    if description is ...:
        description = None
    else:
        description = validate_description(description)
    
    # placeholder
    if placeholder is ...:
        placeholder = False
    else:
        placeholder = validate_placeholder(placeholder)
    
    # required
    if required is ...:
        required = False
    else:
        required = validate_required(required)
    
    # style
    if style is ...:
        style = None
    else:
        style = validate_text_input_style(style)
    
    # title
    if title is ...:
        title = None
    else:
        title = validate_title(title)
    
    # value
    if value is ...:
        value = None
    else:
        value = validate_value(value)
    
    if style is GuildJoinRequestFormFieldTextInputStyle.short:
        field_type = GuildJoinRequestFormFieldType.text_input_short
    elif style is GuildJoinRequestFormFieldTextInputStyle.paragraph:
        field_type = GuildJoinRequestFormFieldType.text_input_paragraph
    else:
        field_type = GuildJoinRequestFormFieldType.text_input_short
    
    guild_join_request_form_field_response = object.__new__(GuildJoinRequestFormFieldResponse)
    guild_join_request_form_field_response.type = field_type
    guild_join_request_form_field_response.description = description
    guild_join_request_form_field_response.required = required
    guild_join_request_form_field_response.title = title
    metadata = object.__new__(GuildJoinRequestFormFieldResponseMetadataTextInput)
    metadata.placeholder = placeholder
    metadata.value = value
    guild_join_request_form_field_response.metadata = metadata
    return guild_join_request_form_field_response


def guild_join_request_form_field_response_create_choice_single(
    *,
    choice_index = ...,
    choices = ...,
    description = ...,
    required = ...,
    title = ...,
):
    """
    Creates a new guild join form field response of type choice single.
    
    Parameters
    ----------
    choice_index : `int`
        The choice's index selected by the user. `-1` if the user did not chose anything.
    
    choices : `None | tuple<str>`
        The offered choices.
    
    description : `None | str`
        Description of the field.
    
    required : `bool`
        Whether the field is required.
    
    title : `None | str`
        Title of the field.
    
    Returns
    -------
    guild_join_request_form_field_response : ``GuildJoinRequestFormFieldResponse``
    
    Raises
    ------
    TypeError
        - If a parameter's type is incorrect.
    ValueError
        - If a parameter's value is incorrect.
    """
    # choice_index
    if choice_index is ...:
        choice_index = False
    else:
        choice_index = validate_choice_index(choice_index)
    
    # choices
    if choices is ...:
        choices = None
    else:
        choices = validate_choices(choices)
    
    # description
    if description is ...:
        description = None
    else:
        description = validate_description(description)
    
    # required
    if required is ...:
        required = False
    else:
        required = validate_required(required)
    
    # title
    if title is ...:
        title = None
    else:
        title = validate_title(title)
    
    guild_join_request_form_field_response = object.__new__(GuildJoinRequestFormFieldResponse)
    guild_join_request_form_field_response.type = GuildJoinRequestFormFieldType.choice_single
    guild_join_request_form_field_response.description = description
    guild_join_request_form_field_response.required = required
    guild_join_request_form_field_response.title = title
    metadata = object.__new__(GuildJoinRequestFormFieldResponseMetadataChoiceSingle)
    metadata.choice_index = choice_index
    metadata.choices = choices
    guild_join_request_form_field_response.metadata = metadata
    return guild_join_request_form_field_response
