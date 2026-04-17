import vampytest

from ..preinstanced import AutoModerationKeywordPresetType


@vampytest.call_from(AutoModerationKeywordPresetType.INSTANCES.values())
def test__AutoModerationKeywordPresetType__instances(instance):
    """
    Tests whether ``AutoModerationKeywordPresetType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``AutoModerationKeywordPresetType``
        The instance to test.
    """
    vampytest.assert_instance(instance, AutoModerationKeywordPresetType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, AutoModerationKeywordPresetType.VALUE_TYPE)
