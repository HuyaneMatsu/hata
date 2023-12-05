import vampytest

from ...channel_metadata import ChannelMetadataBase

from ..flags import ChannelTypeFlag
from ..preinstanced import ChannelType


@vampytest.call_from(ChannelType.INSTANCES.values())
def test__ChannelType__instances(instance):
    """
    Tests whether ``ChannelType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ChannelType``
        The instance to test.
    """
    vampytest.assert_instance(instance, ChannelType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, ChannelType.VALUE_TYPE)
    vampytest.assert_instance(instance.flags, ChannelTypeFlag)
    vampytest.assert_subtype(instance.metadata_type, ChannelMetadataBase)
