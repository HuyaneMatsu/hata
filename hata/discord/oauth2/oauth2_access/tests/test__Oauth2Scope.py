import vampytest

from ..preinstanced import Oauth2Scope


@vampytest.call_from(Oauth2Scope.INSTANCES.values())
def test__Oauth2Scope__instances(instance):
    """
    Tests whether ``Oauth2Scope`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``Oauth2Scope``
        The instance to test.
    """
    vampytest.assert_instance(instance, Oauth2Scope)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, Oauth2Scope.VALUE_TYPE)
