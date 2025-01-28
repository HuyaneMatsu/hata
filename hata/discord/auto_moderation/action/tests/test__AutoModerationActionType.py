import vampytest

from ...action_metadata import AutoModerationActionMetadataBase

from ..preinstanced import AutoModerationActionType

def _assert_fields_set(auto_moderation_action_type):
    """
    Asserts whether every field are set of the given auto moderation action type.
    
    Parameters
    ----------
    auto_moderation_action_type : ``AutoModerationActionType``
        The instance to test.
    """
    vampytest.assert_instance(auto_moderation_action_type, AutoModerationActionType)
    vampytest.assert_instance(auto_moderation_action_type.name, str)
    vampytest.assert_instance(auto_moderation_action_type.value, AutoModerationActionType.VALUE_TYPE)
    vampytest.assert_subtype(auto_moderation_action_type.metadata_type, AutoModerationActionMetadataBase)


@vampytest.call_from(AutoModerationActionType.INSTANCES.values())
def test__AutoModerationActionType__instances(instance):
    """
    Tests whether ``AutoModerationActionType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``AutoModerationActionType``
        The instance to test.
    """
    _assert_fields_set(instance)


def test__AutoModerationActionType__new__min_fields():
    """
    Tests whether ``AutoModerationActionType.__new__`` works as intended.
    
    Case: minimal amount of fields given.
    """
    value = 50
    
    try:
        output = AutoModerationActionType(value)
        _assert_fields_set(output)
        
        vampytest.assert_eq(output.value, value)
        vampytest.assert_eq(output.name, AutoModerationActionType.NAME_DEFAULT)
        vampytest.assert_is(output.metadata_type, AutoModerationActionMetadataBase)
        vampytest.assert_is(AutoModerationActionType.INSTANCES.get(value, None), output)
    
    finally:
        try:
            del AutoModerationActionType.INSTANCES[value]
        except KeyError:
            pass
