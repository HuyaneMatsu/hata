import vampytest

from ..base import ApplicationCommandOptionMetadataBase

from .test__ApplicationCommandOptionMetadataBase__constructor import _asert_fields_set


def test__ApplicationCommandOptionMetadataBase__from_data():
    """
    Tests whether ``ApplicationCommandOptionMetadataBase.from_data`` works as intended.
    """
    data = {}
    
    option_metadata = ApplicationCommandOptionMetadataBase.from_data(data)
    _asert_fields_set(option_metadata)



def test__ApplicationCommandOptionMetadataBase__to_data():
    """
    Tests whether ``ApplicationCommandOptionMetadataBase.to_data`` works as intended.
    
    Case: include defaults
    """
    option_metadata = ApplicationCommandOptionMetadataBase({
    })
    
    expected_output = {}
    
    vampytest.assert_eq(
        option_metadata.to_data(
            defaults = True,
        ),
        expected_output
    )
