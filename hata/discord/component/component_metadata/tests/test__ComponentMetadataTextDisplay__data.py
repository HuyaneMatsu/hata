import vampytest

from ..text_display import ComponentMetadataTextDisplay

from .test__ComponentMetadataTextDisplay__constructor import _assert_fields_set


def test__ComponentMetadataTextDisplay__from_data():
    """
    Tests whether ``ComponentMetadataTextDisplay.from_data`` works as intended.
    """
    content = 'hey sister'
    
    data = {
        'content': content,
    }
    
    component_metadata = ComponentMetadataTextDisplay.from_data(data)
    _assert_fields_set(component_metadata)
    vampytest.assert_eq(component_metadata.content, content)


def test__ComponentMetadataTextDisplay__to_data():
    """
    Tests whether ``ComponentMetadataTextDisplay.to_data`` works as intended.
    
    Case: include defaults and internals.
    """
    content = 'hey sister'
    
    component_metadata = ComponentMetadataTextDisplay(
        content = content,
    )
    
    vampytest.assert_eq(
        component_metadata.to_data(
            defaults = True,
            include_internals = True,
        ),
        {
            'content': content,
        },
    )
