import vampytest

from ....core import BUILTIN_EMOJIS

from ..button import ComponentMetadataButton
from ..preinstanced import ButtonStyle


def test__ComponentMetadataButton__repr__0():
    """
    Tests whether ``ComponentMetadataButton.__repr__`` works as intended.
    """
    button_style = ButtonStyle.green
    custom_id = 'orin'
    emoji = BUILTIN_EMOJIS['heart']
    enabled = False
    label = 'frost'
    url = None
    
    keyword_parameters = {
        'button_style': button_style,
        'custom_id': custom_id,
        'emoji': emoji,
        'enabled': enabled,
        'label': label,
        'url': url,
    }
    
    component_metadata = ComponentMetadataButton(keyword_parameters)
    
    vampytest.assert_instance(repr(component_metadata), str)


def test__ComponentMetadataButton__repr__1():
    """
    Tests whether ``ComponentMetadataButton.__repr__`` works as intended.
    
    Case: url.
    """
    url = 'https://orindance.party/'
    
    keyword_parameters = {
        'url': url,
    }
    
    component_metadata = ComponentMetadataButton(keyword_parameters)
    
    vampytest.assert_instance(repr(component_metadata), str)




def test__ComponentMetadataButton__hash__0():
    """
    Tests whether ``ComponentMetadataButton.__hash__`` works as intended.
    """
    button_style = ButtonStyle.green
    custom_id = 'orin'
    emoji = BUILTIN_EMOJIS['heart']
    enabled = False
    label = 'frost'
    url = None
    
    keyword_parameters = {
        'button_style': button_style,
        'custom_id': custom_id,
        'emoji': emoji,
        'enabled': enabled,
        'label': label,
        'url': url,
    }
    
    component_metadata = ComponentMetadataButton(keyword_parameters)
    
    vampytest.assert_instance(hash(component_metadata), int)



def test__ComponentMetadataButton__hash__1():
    """
    Tests whether ``ComponentMetadataButton.__hash__`` works as intended.
    
    Case: url.
    """
    url = 'https://orindance.party/'
    
    keyword_parameters = {
        'url': url,
    }
    
    component_metadata = ComponentMetadataButton(keyword_parameters)
    
    vampytest.assert_instance(hash(component_metadata), int)


def test__ComponentMetadataButton__eq__0():
    """
    Tests whether ``ComponentMetadataButton.__eq__`` works as intended.
    """
    button_style = ButtonStyle.green
    custom_id = 'orin'
    emoji = BUILTIN_EMOJIS['heart']
    enabled = False
    label = 'frost'
    url = None
    
    keyword_parameters = {
        'button_style': button_style,
        'custom_id': custom_id,
        'emoji': emoji,
        'enabled': enabled,
        'label': label,
        'url': url,
    }
    
    component_metadata = ComponentMetadataButton(keyword_parameters)
    
    vampytest.assert_eq(component_metadata, component_metadata)
    vampytest.assert_ne(component_metadata, object())
    
    for field_name, field_value in (
        ('button_style', ButtonStyle.red),
        ('custom_id', 'okuu'),
        ('emoji', BUILTIN_EMOJIS['knife']),
        ('enabled', True),
        ('label', 'fragment'),
        ('url', None),
    ):
        test_component_metadata = ComponentMetadataButton({**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(component_metadata, test_component_metadata)


def test__ComponentMetadataButton__eq__1():
    """
    Tests whether ``ComponentMetadataButton.__eq__`` works as intended.
    
    Case: url.
    """
    url = 'https://orindance.party/'
    
    keyword_parameters = {
        'url': url,
    }
    
    component_metadata = ComponentMetadataButton(keyword_parameters)
    
    vampytest.assert_eq(component_metadata, component_metadata)
    vampytest.assert_ne(component_metadata, object())
    
    for field_name, field_value in (
        ('url', 'https://www.astil.dev/'),
    ):
        test_component_metadata = ComponentMetadataButton({**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(component_metadata, test_component_metadata)
