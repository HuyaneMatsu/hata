import vampytest

from ...action_metadata import AutoModerationActionMetadataBase

from ..preinstanced import AutoModerationActionType


@vampytest.call_from(AutoModerationActionType.INSTANCES.values())
def test__AutoModerationActionType__instances(instance):
    """
    Tests whether ``AutoModerationActionType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``AutoModerationActionType``
        The instance to test.
    """
    vampytest.assert_instance(instance, AutoModerationActionType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, AutoModerationActionType.VALUE_TYPE)
    vampytest.assert_subtype(instance.metadata_type, AutoModerationActionMetadataBase)
