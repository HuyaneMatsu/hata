import vampytest

from ..provider import EmbedProvider

from .test__EmbedProvider__constructor import _assert_fields_set


def test__EmbedProvider__from_data():
    """
    Tests whether ``EmbedProvider.from_data`` works as intended.
    """
    name = 'orin'
    url = 'https://orindance.party/'
    
    data = {
        'name': name,
        'url': url,
    }
    
    embed_provider = EmbedProvider.from_data(data)
    _assert_fields_set(embed_provider)
    
    vampytest.assert_eq(embed_provider.name, name)
    vampytest.assert_eq(embed_provider.url, url)


def test__EmbedProvider__to_data():
    """
    Tests whether ``EmbedProvider.to_data`` works as intended.
    
    Case: Include defaults & internals.
    """
    name = 'orin'
    url = 'https://orindance.party/'
    
    embed_provider = EmbedProvider(name = name, url = url)
    
    expected_output = {
        'name': name,
        'url': url,
    }
    
    vampytest.assert_eq(
        embed_provider.to_data(defaults = True, include_internals = True),
        expected_output,
    )
