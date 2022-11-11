import vampytest

from ...channel_metadata import ChannelMetadataBase

from ..flags import ChannelTypeFlag
from ..preinstanced import ChannelType


def test__ChannelType__name():
    """
    Tests whether ``ChannelType`` instance names are all strings.
    """
    for instance in ChannelType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__ChannelType__value():
    """
    Tests whether ``ChannelType`` instance values are all the expected value type.
    """
    for instance in ChannelType.INSTANCES.values():
        vampytest.assert_instance(instance.value, ChannelType.VALUE_TYPE)


def test__ChannelType__flags():
    """
    Tests whether ``ChannelType`` instance flags are channel type flags.
    """
    for instance in ChannelType.INSTANCES.values():
        vampytest.assert_instance(instance.flags, ChannelTypeFlag)


def test__ChannelType__metadata_type():
    """
    Tests whether ``ChannelType`` instance metadata types are all metadata types.
    """
    for instance in ChannelType.INSTANCES.values():
        vampytest.assert_subtype(instance.metadata_type, ChannelMetadataBase)
