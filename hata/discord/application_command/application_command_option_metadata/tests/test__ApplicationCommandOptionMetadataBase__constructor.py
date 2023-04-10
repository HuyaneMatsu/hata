import vampytest

from ..base import ApplicationCommandOptionMetadataBase


def _asert_fields_set(option_metadata):
    """
    Asserts whether all attributes of the application command option metadata are set.
    
    Parameters
    ----------
    option_metadata : ``ApplicationCommandOptionMetadataBase``
        The application command option metadata to check.
    """
    vampytest.assert_instance(option_metadata, ApplicationCommandOptionMetadataBase)
    
    # No extra fields


def test__ApplicationCommandOptionMetadataBase__new__0():
    """
    Tests whether ``ApplicationCommandOptionMetadataBase.__new__`` works as intended.
    
    Case: No fields given.
    """
    option_metadata = ApplicationCommandOptionMetadataBase()
    _asert_fields_set(option_metadata)


def test__ApplicationCommandOptionMetadataBase__from_keyword_parameters__1():
    """
    Tests whether ``ApplicationCommandOptionMetadataBase.from_keyword_parameters`` works as intended.
    
    Case: No fields given.
    """
    option_metadata = ApplicationCommandOptionMetadataBase.from_keyword_parameters({})
    _asert_fields_set(option_metadata)
