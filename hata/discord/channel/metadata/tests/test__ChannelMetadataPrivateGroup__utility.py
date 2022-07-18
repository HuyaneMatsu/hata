from .. import ChannelMetadataPrivateGroup


def test__ChannelMetadataPrivateGroup__precreate():
    """
    Issue: `AttributeError` at `ChannelMetadataPrivateGroup._precreate`.
    
    No data was passed. Attribute field was missing.
    """
    return ChannelMetadataPrivateGroup._precreate({})
