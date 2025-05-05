import vampytest

from ....guild import Guild

from ..base import ComponentMetadataBase

from .test__ComponentMetadataBase__constructor import _assert_fields_set


def test__ComponentMetadataBase__clean_copy():
    """
    Tests whether ``ComponentMetadataBase.clean_copy`` works as intended.
    """
    guild_id = 202505030011
    guild = Guild.precreate(guild_id)
    
    component_metadata = ComponentMetadataBase()
    copy = component_metadata.clean_copy(guild)
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, component_metadata)
    vampytest.assert_eq(copy, component_metadata)


def test__ComponentMetadataBase__copy():
    """
    Tests whether ``ComponentMetadataBase.copy`` works as intended.
    """
    component_metadata = ComponentMetadataBase()
    copy = component_metadata.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, component_metadata)
    vampytest.assert_eq(copy, component_metadata)
    

def test__ComponentMetadataBase__copy_with__no_fields():
    """
    Tests whether ``ComponentMetadataBase.copy_with`` works as intended.
    
    Case: No fields given.
    """
    component_metadata = ComponentMetadataBase()
    copy = component_metadata.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, component_metadata)
    vampytest.assert_eq(copy, component_metadata)


def test__ComponentMetadataBase__copy_with_keyword_parameters__no_fields():
    """
    Tests whether ``ComponentMetadataBase.copy_with_keyword_parameters`` works as intended.
    
    Case: No fields given.
    """
    component_metadata = ComponentMetadataBase()
    copy = component_metadata.copy_with_keyword_parameters({})
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(copy, component_metadata)
    vampytest.assert_eq(copy, component_metadata)


def _iter_options__iter_contents():
    yield (
        {},
        [],
    )


@vampytest._(vampytest.call_from(_iter_options__iter_contents()).returning_last())
def test__ComponentMetadataBase__iter_contents(keyword_parameters):
    """
    Tests whether ``ComponentMetadataBase.iter_contents`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `list<str>`
    """
    component_metadata = ComponentMetadataBase(**keyword_parameters)
    output = [*component_metadata.iter_contents()]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return output
