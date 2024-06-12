import vampytest

from ..text import ComponentMetadataText

from .test__ComponentMetadataText__constructor import _assert_fields_set


def test__ComponentMetadataText__from_data():
    """
    Tests whether ``ComponentMetadataText.from_data`` works as intended.
    """
    content = 'hey sister'
    
    data = {
        'content': content,
    }
    
    component_metadata = ComponentMetadataText.from_data(data)
    _assert_fields_set(component_metadata)
    vampytest.assert_eq(component_metadata.content, content)


def test__ComponentMetadataText__to_data():
    """
    Tests whether ``ComponentMetadataText.to_data`` works as intended.
    
    Case: include defaults.
    """
    content = 'hey sister'
    
    component_metadata = ComponentMetadataText(
        content = content,
    )
    
    vampytest.assert_eq(
        component_metadata.to_data(
            defaults = True,
        ),
        {
            'content': content,
        },
    )
