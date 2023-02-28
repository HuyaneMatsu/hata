import vampytest

from ..parameter import ApplicationCommandOptionMetadataParameter

from .test__ApplicationCommandOptionMetadataParameter__constructor import _asert_fields_set


def test__ApplicationCommandOptionMetadataParameter__from_data():
    """
    Tests whether ``ApplicationCommandOptionMetadataParameter.from_data`` works as intended.
    """
    required = True
    
    data = {
        'required': required,
    }
    
    option_metadata = ApplicationCommandOptionMetadataParameter.from_data(data)
    _asert_fields_set(option_metadata)
    
    vampytest.assert_eq(option_metadata.required, required)



def test__ApplicationCommandOptionMetadataParameter__to_data():
    """
    Tests whether ``ApplicationCommandOptionMetadataParameter.to_data`` works as intended.
    
    Case: include defaults
    """
    required = True
    
    option_metadata = ApplicationCommandOptionMetadataParameter({
        'required': required,
    })
    
    expected_output = {
        'required': required,
    }
    
    vampytest.assert_eq(
        option_metadata.to_data(
            defaults = True,
        ),
        expected_output
    )
