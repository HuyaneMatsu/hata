import vampytest

from ..text import ComponentMetadataText


def _assert_fields_set(component_metadata):
    """
    Checks whether the given component metadata has all of its fields set.
    
    Parameters
    ----------
    component_metadata : ``ComponentMetadataText``
    """
    vampytest.assert_instance(component_metadata, ComponentMetadataText)
    vampytest.assert_instance(component_metadata.content, str, nullable = True)


def test__ComponentMetadataText__new__no_fields():
    """
    Tests whether ``ComponentMetadataText.__new__`` works as intended.
    
    Case: No fields.
    """
    component_metadata = ComponentMetadataText()
    _assert_fields_set(component_metadata)


def test__ComponentMetadataText__new__all_fields():
    """
    Tests whether ``ComponentMetadataText.__new__`` works as intended.
    
    Case: All fields.
    """
    content = 'hey sister'
    
    component_metadata = ComponentMetadataText(
        content = content,
    )
    _assert_fields_set(component_metadata)
    vampytest.assert_eq(component_metadata.content, content)


def test__ComponentMetadataText__from_keyword_parameters__no_fields():
    """
    Tests whether ``ComponentMetadataText.from_keyword_parameters`` works as intended.
    
    Case: No fields.
    """
    keyword_parameters = {}
    
    component_metadata = ComponentMetadataText.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)


def test__ComponentMetadataText__from_keyword_parameters__all_fields():
    """
    Tests whether ``ComponentMetadataText.from_keyword_parameters`` works as intended.
    
    Case: All fields.
    """
    content = 'hey sister'
    
    keyword_parameters = {
        'content': content,
    }
    
    component_metadata = ComponentMetadataText.from_keyword_parameters(keyword_parameters)
    _assert_fields_set(component_metadata)
    vampytest.assert_eq(component_metadata.content, content)
