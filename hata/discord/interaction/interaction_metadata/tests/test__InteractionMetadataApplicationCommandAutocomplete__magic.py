import vampytest

from ...interaction_option import InteractionOption

from ..application_command_autocomplete import InteractionMetadataApplicationCommandAutocomplete


def test__InteractionMetadataApplicationCommandAutocomplete__repr():
    """
    Tests whether ``InteractionMetadataApplicationCommandAutocomplete.__repr__`` works as intended.
    """
    id_ = 202211060005
    name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    
    interaction_metadata = InteractionMetadataApplicationCommandAutocomplete(
        id = id_,
        name = name,
        options = options,
    )
    vampytest.assert_instance(repr(interaction_metadata), str)


def test__InteractionMetadataApplicationCommandAutocomplete__hash():
    """
    Tests whether ``InteractionMetadataApplicationCommandAutocomplete.__hash__`` works as intended.
    """
    id_ = 202211060006
    name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    
    interaction_metadata = InteractionMetadataApplicationCommandAutocomplete(
        id = id_,
        name = name,
        options = options,
    )
    vampytest.assert_instance(hash(interaction_metadata), int)


def test__InteractionMetadataApplicationCommandAutocomplete__eq():
    """
    Tests whether ``InteractionMetadataApplicationCommandAutocomplete.__eq__`` works as intended.
    """
    id_ = 202211060007
    name = 'Inaba'
    options = [InteractionOption(name = 'Rem')]
    
    keyword_parameters = {
        'id': id_,
        'name': name,
        'options': options,
    }
    
    interaction_metadata = InteractionMetadataApplicationCommandAutocomplete(**keyword_parameters)
    
    vampytest.assert_eq(interaction_metadata, interaction_metadata)
    vampytest.assert_ne(interaction_metadata, object())
    
    for field_name, field_value in (
        ('id', 202211060008),
        ('name', 'Reisen'),
        ('options', None),
    ):
        test_interaction_metadata = InteractionMetadataApplicationCommandAutocomplete(
            **{**keyword_parameters, field_name: field_value}
        )
        vampytest.assert_ne(interaction_metadata, test_interaction_metadata)
