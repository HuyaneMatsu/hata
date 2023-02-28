import vampytest

from ..parameter import ApplicationCommandOptionMetadataParameter


def _asert_fields_set(option_metadata):
    """
    Asserts whether all attributes of the application command option metadata are set.
    
    Parameters
    ----------
    option_metadata : ``ApplicationCommandOptionMetadataParameter``
        The application command option metadata to check.
    """
    vampytest.assert_instance(option_metadata, ApplicationCommandOptionMetadataParameter)
    
    vampytest.assert_instance(option_metadata.required, bool)


def test__ApplicationCommandOptionMetadataParameter__new__0():
    """
    Tests whether ``ApplicationCommandOptionMetadataParameter.__new__`` works as intended.
    
    Case: No fields given.
    """
    option_metadata = ApplicationCommandOptionMetadataParameter({})
    _asert_fields_set(option_metadata)


def test__ApplicationCommandOptionMetadataParameter__new__1():
    """
    Tests whether ``ApplicationCommandOptionMetadataParameter.__new__`` works as intended.
    
    Case: All fields given.
    """
    required = True
    
    option_metadata = ApplicationCommandOptionMetadataParameter({
        'required': required,
    })
    _asert_fields_set(option_metadata)
    
    vampytest.assert_eq(option_metadata.required, required)
