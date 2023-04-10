import vampytest

from ..base import ApplicationCommandOptionMetadataBase


def test__ApplicationCommandOptionMetadataBase__placeholders():
    """
    Tests whether all placeholders of ``ApplicationCommandOptionMetadataBase`` work as intended.
    """
    option_metadata = ApplicationCommandOptionMetadataBase()
    
    vampytest.assert_instance(option_metadata.autocomplete, bool)
    vampytest.assert_instance(option_metadata.channel_types, tuple, nullable = True)
    vampytest.assert_instance(option_metadata.choices, tuple, nullable = True)
    vampytest.assert_instance(option_metadata.default, bool)
    vampytest.assert_instance(option_metadata.max_length, int)
    vampytest.assert_instance(option_metadata.max_value, object, nullable = True)
    vampytest.assert_instance(option_metadata.min_length, int)
    vampytest.assert_instance(option_metadata.min_value, object, nullable = True)
    vampytest.assert_instance(option_metadata.options, tuple, nullable = True)
    vampytest.assert_instance(option_metadata.required, bool)
