import vampytest

from ..author import EmbedAuthor

from .test__EmbedAuthor__constructor import _assert_fields_set


def test__EmbedAuthor__from_data():
    """
    Tests whether ``EmbedAuthor.from_data`` works as intended.
    """
    icon_url = 'attachment://orin.png'
    icon_proxy_url = 'https://www.astil.dev/project/hata/'
    name = 'orin'
    url = 'https://orindance.party/'
    
    data = {
        'icon_url': icon_url,
        'proxy_icon_url': icon_proxy_url,
        'name': name,
        'url': url,
    }
    
    embed_author = EmbedAuthor.from_data(data)
    _assert_fields_set(embed_author)
    
    vampytest.assert_eq(embed_author.icon_url, icon_url)
    vampytest.assert_eq(embed_author.icon_proxy_url, icon_proxy_url)
    vampytest.assert_eq(embed_author.name, name)
    vampytest.assert_eq(embed_author.url, url)


def test__EmbedAuthor__to_data():
    """
    Tests whether ``EmbedAuthor.to_data`` works as intended.
    
    Case: Include defaults & internals.
    """
    icon_url = 'attachment://orin.png'
    icon_proxy_url = 'https://www.astil.dev/project/hata/'
    name = 'orin'
    url = 'https://orindance.party/'
    
    data = {
        'icon_url': icon_url,
        'proxy_icon_url': icon_proxy_url,
        'name': name,
        'url': url,
    }
    
    embed_author = EmbedAuthor.from_data(data)
    
    expected_output = data
    
    vampytest.assert_eq(
        embed_author.to_data(defaults = True, include_internals = True),
        expected_output,
    )
