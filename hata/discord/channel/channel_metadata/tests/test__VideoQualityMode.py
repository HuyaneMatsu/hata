import vampytest

from ..preinstanced import VideoQualityMode


@vampytest.call_from(VideoQualityMode.INSTANCES.values())
def test__VideoQualityMode__instances(instance):
    """
    Tests whether ``VideoQualityMode`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``VideoQualityMode``
        The instance to test.
    """
    vampytest.assert_instance(instance, VideoQualityMode)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, VideoQualityMode.VALUE_TYPE)
