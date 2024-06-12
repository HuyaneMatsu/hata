import vampytest

from ..preinstanced import SeparatorSpacingSize


@vampytest.call_from(SeparatorSpacingSize.INSTANCES.values())
def test__SeparatorSpacingSize__instances(instance):
    """
    Tests whether ``SeparatorSpacingSize`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``SeparatorSpacingSize``
        The instance to test.
    """
    vampytest.assert_instance(instance, SeparatorSpacingSize)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, SeparatorSpacingSize.VALUE_TYPE)
