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
    
    field = EmbedProvider.from_data(data)
    _assert_fields_set(field)
    
    vampytest.assert_eq(field.name, name)
    vampytest.assert_eq(field.url, url)


def test__EmbedProvider__to_data():
    """
    Tests whether ``EmbedProvider.to_data`` works as intended.
    
    Case: Include defaults & internals.
    """
    name = 'orin'
    url = 'https://orindance.party/'
    
    field = EmbedProvider(name = name, url = url)
    
    expected_output = {
        'name': name,
        'url': url,
    }
    
    vampytest.assert_eq(
        field.to_data(defaults = True, include_internals = True),
        expected_output,
    )
