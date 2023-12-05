import vampytest

from ..preinstanced import ApplicationCommandOptionType

from ...application_command_option_metadata import ApplicationCommandOptionMetadataBase


@vampytest.call_from(ApplicationCommandOptionType.INSTANCES.values())
def test__ApplicationCommandOptionType__instances(instance):
    """
    Tests whether ``ApplicationCommandOptionType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ApplicationCommandOptionType``
        The instance to test.
    """
    vampytest.assert_instance(instance, ApplicationCommandOptionType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, ApplicationCommandOptionType.VALUE_TYPE)
    vampytest.assert_subtype(instance.metadata_type, ApplicationCommandOptionMetadataBase)
