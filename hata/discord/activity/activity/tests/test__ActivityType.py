import vampytest

from ...activity_metadata import ActivityMetadataBase, ActivityMetadataRich

from ..preinstanced import ActivityType


def _assert_fields_set(activity_type):
    """
    Asserts whether every field are set of the given activity type.
    
    Parameters
    ----------
    activity_type : ``ActivityType``
        The instance to test.
    """
    vampytest.assert_instance(activity_type, ActivityType)
    vampytest.assert_instance(activity_type.name, str)
    vampytest.assert_instance(activity_type.value, ActivityType.VALUE_TYPE)
    vampytest.assert_subtype(activity_type.metadata_type, ActivityMetadataBase)


@vampytest.call_from(ActivityType.INSTANCES.values())
def test__ActivityType__instances(instance):
    """
    Tests whether ``ActivityType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ActivityType``
        The instance to test.
    """
    _assert_fields_set(instance)


def test__ActivityType__new__min_fields():
    """
    Tests whether ``ActivityType.__new__`` works as intended.
    
    Case: minimal amount of fields given.
    """
    value = 50
    
    try:
        output = ActivityType(value)
        _assert_fields_set(output)
        
        vampytest.assert_eq(output.value, value)
        vampytest.assert_eq(output.name, ActivityType.NAME_DEFAULT)
        vampytest.assert_is(output.metadata_type, ActivityMetadataRich)
        vampytest.assert_is(ActivityType.INSTANCES.get(value, None), output)
    
    finally:
        try:
            del ActivityType.INSTANCES[value]
        except KeyError:
            pass
