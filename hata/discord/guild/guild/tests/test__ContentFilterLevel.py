import vampytest

from ..preinstanced import ContentFilterLevel


@vampytest.call_from(ContentFilterLevel.INSTANCES.values())
def test__ContentFilterLevel__instances(instance):
    """
    Tests whether ``ContentFilterLevel`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ContentFilterLevel``
        The instance to test.
    """
    vampytest.assert_instance(instance, ContentFilterLevel)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, ContentFilterLevel.VALUE_TYPE)
