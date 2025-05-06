import vampytest

from ....core import BUILTIN_EMOJIS

from ..button import ComponentMetadataButton
from ..preinstanced import ButtonStyle


def test__ComponentMetadataButton__repr__default():
    """
    Tests whether ``ComponentMetadataButton.__repr__`` works as intended.
    
    Case: default.
    """
    button_style = ButtonStyle.green
    custom_id = 'orin'
    emoji = BUILTIN_EMOJIS['heart']
    enabled = False
    label = 'frost'
    sku_id = 0
    url = None
    
    component_metadata = ComponentMetadataButton(
        button_style = button_style,
        custom_id = custom_id,
        emoji = emoji,
        enabled = enabled,
        label = label,
        sku_id = sku_id,
        url = url,
    )
    
    vampytest.assert_instance(repr(component_metadata), str)


def test__ComponentMetadataButton__repr__url():
    """
    Tests whether ``ComponentMetadataButton.__repr__`` works as intended.
    
    Case: url.
    """
    url = 'https://orindance.party/'
    
    component_metadata = ComponentMetadataButton(
        url = url,
    )
    
    vampytest.assert_instance(repr(component_metadata), str)


def test__ComponentMetadataButton__repr__sku_id():
    """
    Tests whether ``ComponentMetadataButton.__repr__`` works as intended.
    
    Case: sku id.
    """
    sku_id = 202405180077
    
    component_metadata = ComponentMetadataButton(
        sku_id = sku_id,
    )
    
    vampytest.assert_instance(repr(component_metadata), str)


def test__ComponentMetadataButton__hash__default():
    """
    Tests whether ``ComponentMetadataButton.__hash__`` works as intended.
    
    Case: default.
    """
    button_style = ButtonStyle.green
    custom_id = 'orin'
    emoji = BUILTIN_EMOJIS['heart']
    enabled = False
    label = 'frost'
    url = None
    
    component_metadata = ComponentMetadataButton(
        button_style = button_style,
        custom_id = custom_id,
        emoji = emoji,
        enabled = enabled,
        label = label,
        url = url,
    )
    
    vampytest.assert_instance(hash(component_metadata), int)


def test__ComponentMetadataButton__hash__url():
    """
    Tests whether ``ComponentMetadataButton.__hash__`` works as intended.
    
    Case: url.
    """
    url = 'https://orindance.party/'
    
    component_metadata = ComponentMetadataButton(
        url = url,
    )
    
    vampytest.assert_instance(hash(component_metadata), int)


def test__ComponentMetadataButton__hash__sku_id():
    """
    Tests whether ``ComponentMetadataButton.__hash__`` works as intended.
    
    Case: sku_id.
    """
    sku_id = 202405180078
    
    component_metadata = ComponentMetadataButton(
        sku_id = sku_id,
    )
    
    vampytest.assert_instance(hash(component_metadata), int)


def test__ComponentMetadataButton__eq__different_type():
    """
    Tests whether ``ComponentMetadataButton.__eq__`` works as intended.
    
    Case: Different type.
    """
    component_metadata = ComponentMetadataButton()
    
    vampytest.assert_ne(component_metadata, object())


def _iter_options__eq__same_type():
    button_style = ButtonStyle.green
    custom_id = 'orin'
    emoji = BUILTIN_EMOJIS['heart']
    enabled = False
    label = 'frost'
    url = 'https://www.orindance.party/'
    
    keyword_parameters = {
        'button_style': button_style,
        'custom_id': custom_id,
        'emoji': emoji,
        'enabled': enabled,
        'label': label,
        'url': url,
    }


    yield (
        {
            **keyword_parameters,
            'url': None,
            'sku_id': 0,
        },
        {
            **keyword_parameters,
            'url': None,
            'sku_id': 0,
        },
        True,
    )
    
    yield (
        {
            **keyword_parameters,
            'url': None,
            'sku_id': 0,
        },
        {
            **keyword_parameters,
            'url': None,
            'sku_id': 0,
            'button_style': ButtonStyle.red,
        },
        False,
    )
    
    yield (
        {
            **keyword_parameters,
            'url': None,
            'sku_id': 0,
        },
        {
            **keyword_parameters,
            'url': None,
            'sku_id': 0,
            'custom_id': 'okuu',
        },
        False,
    )
    
    yield (
        {
            **keyword_parameters,
            'url': None,
            'sku_id': 0,
        },
        {
            **keyword_parameters,
            'url': None,
            'sku_id': 0,
            'emoji': None,
        },
        False,
    )
    
    yield (
        {
            **keyword_parameters,
            'url': None,
            'sku_id': 0,
        },
        {
            **keyword_parameters,
            'url': None,
            'sku_id': 0,
            'enabled': True,
        },
        False,
    )
    
    yield (
        {
            **keyword_parameters,
            'url': None,
            'sku_id': 0,
        },
        {
            **keyword_parameters,
            'url': None,
            'sku_id': 0,
            'label': 'fragment',
        },
        False,
    )
    
    yield (
        {
            **keyword_parameters,
            'button_style': ButtonStyle.link,
            'custom_id': None,
            'sku_id': 0,
        },
        {
            **keyword_parameters,
            'button_style': ButtonStyle.link,
            'custom_id': None,
            'sku_id': 0,
        },
        True,
    )
    
    yield (
        {
            **keyword_parameters,
            'button_style': ButtonStyle.link,
            'custom_id': None,
            'sku_id': 0,
        },
        {
            **keyword_parameters,
            'button_style': ButtonStyle.link,
            'custom_id': None,
            'sku_id': 0,
            'url': 'https://www.astil.dev/',
        },
        False,
    )
    
    yield (
        {
            **keyword_parameters,
            'button_style': ButtonStyle.subscription,
            'custom_id': None,
            'url': None,
            'sku_id': 202405180081,
        },
        {
            **keyword_parameters,
            'button_style': ButtonStyle.subscription,
            'custom_id': None,
            'url': None,
            'sku_id': 202405180081,
        },
        True,
    )
    
    yield (
        {
            **keyword_parameters,
            'button_style': ButtonStyle.subscription,
            'custom_id': None,
            'url': None,
        },
        {
            **keyword_parameters,
            'button_style': ButtonStyle.subscription,
            'custom_id': None,
            'url': None,
            'sku_id': 202405180080,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq__same_type()).returning_last())
def test__ComponentMetadataButton__eq__same_type(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ComponentMetadataButton.__eq__`` works as intended.
    
    Case: same type.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    component_metadata_0 = ComponentMetadataButton(**keyword_parameters_0)
    component_metadata_1 = ComponentMetadataButton(**keyword_parameters_1)
    output = component_metadata_0 == component_metadata_1
    
    vampytest.assert_instance(output, bool)
    return output
