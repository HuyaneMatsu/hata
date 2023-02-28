import vampytest

from ..base import ApplicationCommandOptionMetadataBase


def test__ApplicationCommandOptionMetadataBase__repr():
    """
    Tests whether ``ApplicationCommandOptionMetadataBase.__repr__`` works as intended.
    """
    option_metadata = ApplicationCommandOptionMetadataBase({
    })
    
    vampytest.assert_instance(repr(option_metadata), str)


def test__ApplicationCommandOptionMetadataBase__hash():
    """
    Tests whether ``ApplicationCommandOptionMetadataBase.__hash__`` works as intended.
    """
    
    option_metadata = ApplicationCommandOptionMetadataBase({
    })
    
    vampytest.assert_instance(hash(option_metadata), int)


def test__ApplicationCommandOptionMetadataBase__eq():
    """
    Tests whether ``ApplicationCommandOptionMetadataBase.__eq__`` works as intended.
    """
    keyword_parameters = {
    }
    
    option_metadata = ApplicationCommandOptionMetadataBase(keyword_parameters)
    
    vampytest.assert_eq(option_metadata, option_metadata)
    vampytest.assert_ne(option_metadata, object())
    
    for field_name, field_value in (
    ):
        test_option_metadata = ApplicationCommandOptionMetadataBase({**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(option_metadata, test_option_metadata)
