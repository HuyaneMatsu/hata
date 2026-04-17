import vampytest

from ..parameter import ApplicationCommandOptionMetadataParameter


def test__ApplicationCommandOptionMetadataParameter__repr():
    """
    Tests whether ``ApplicationCommandOptionMetadataParameter.__repr__`` works as intended.
    """
    required = True
    
    option_metadata = ApplicationCommandOptionMetadataParameter(
        required = required,
    )
    
    vampytest.assert_instance(repr(option_metadata), str)


def test__ApplicationCommandOptionMetadataParameter__hash():
    """
    Tests whether ``ApplicationCommandOptionMetadataParameter.__hash__`` works as intended.
    """
    required = True
    
    option_metadata = ApplicationCommandOptionMetadataParameter(
        required = required,
    )
    
    vampytest.assert_instance(hash(option_metadata), int)


def test__ApplicationCommandOptionMetadataParameter__eq():
    """
    Tests whether ``ApplicationCommandOptionMetadataParameter.__eq__`` works as intended.
    """
    required = True
    
    keyword_parameters = {
        'required': required,
    }
    
    option_metadata = ApplicationCommandOptionMetadataParameter(**keyword_parameters)
    
    vampytest.assert_eq(option_metadata, option_metadata)
    vampytest.assert_ne(option_metadata, object())
    
    for field_name, field_value in (
        ('required', False),
    ):
        test_option_metadata = ApplicationCommandOptionMetadataParameter(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(option_metadata, test_option_metadata)
