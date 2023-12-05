import vampytest

from ..preinstanced import NsfwLevel


@vampytest.call_from(NsfwLevel.INSTANCES.values())
def test__NsfwLevel__instances(instance):
    """
    Tests whether ``NsfwLevel`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``NsfwLevel``
        The instance to test.
    """
    vampytest.assert_instance(instance, NsfwLevel)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, NsfwLevel.VALUE_TYPE)
    vampytest.assert_instance(instance.nsfw, bool)
