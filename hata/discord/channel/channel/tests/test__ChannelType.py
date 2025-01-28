import vampytest

from ...channel_metadata import ChannelMetadataBase

from ..flags import ChannelTypeFlag
from ..preinstanced import ChannelType


def _assert_fields_set(channel_type):
    """
    Asserts whether every field are set of the given channel type.
    
    Parameters
    ----------
    channel_type : ``ChannelType``
        The instance to test.
    """
    vampytest.assert_instance(channel_type, ChannelType)
    vampytest.assert_instance(channel_type.name, str)
    vampytest.assert_instance(channel_type.value, ChannelType.VALUE_TYPE)
    vampytest.assert_instance(channel_type.flags, ChannelTypeFlag)
    vampytest.assert_subtype(channel_type.metadata_type, ChannelMetadataBase)


@vampytest.call_from(ChannelType.INSTANCES.values())
def test__ChannelType__instances(instance):
    """
    Tests whether ``ChannelType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ChannelType``
        The instance to test.
    """
    _assert_fields_set(instance)


def test__ChannelType__new__min_fields():
    """
    Tests whether ``ChannelType.__new__`` works as intended.
    
    Case: minimal amount of fields given.
    """
    value = 50
    
    try:
        output = ChannelType(value)
        _assert_fields_set(output)
        
        vampytest.assert_eq(output.value, value)
        vampytest.assert_eq(output.name, ChannelType.NAME_DEFAULT)
        vampytest.assert_eq(output.flags, ChannelTypeFlag.all)
        vampytest.assert_is(output.metadata_type, ChannelMetadataBase)
        vampytest.assert_is(ChannelType.INSTANCES.get(value, None), output)
    
    finally:
        try:
            del ChannelType.INSTANCES[value]
        except KeyError:
            pass
