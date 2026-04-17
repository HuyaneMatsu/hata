import vampytest

from ..footer import EmbedFooter

from .test__EmbedFooter__constructor import _assert_fields_set


def test__EmbedFooter__from_data():
    """
    Tests whether ``EmbedFooter.from_data`` works as intended.
    """
    icon_url = 'attachment://orin.png'
    icon_proxy_url = 'https://www.astil.dev/project/hata/'
    text = 'orin'
    
    data = {
        'icon_url': icon_url,
        'proxy_icon_url': icon_proxy_url,
        'text': text,
    }
    
    embed_footer = EmbedFooter.from_data(data)
    _assert_fields_set(embed_footer)
    
    vampytest.assert_eq(embed_footer.icon_url, icon_url)
    vampytest.assert_eq(embed_footer.icon_proxy_url, icon_proxy_url)
    vampytest.assert_eq(embed_footer.text, text)


def test__EmbedFooter__to_data():
    """
    Tests whether ``EmbedFooter.to_data`` works as intended.
    
    Case: Include defaults & internals.
    """
    icon_url = 'attachment://orin.png'
    icon_proxy_url = 'https://www.astil.dev/project/hata/'
    text = 'orin'
    
    data = {
        'icon_url': icon_url,
        'proxy_icon_url': icon_proxy_url,
        'text': text,
    }
    
    embed_footer = EmbedFooter.from_data(data)
    
    expected_output = data
    
    vampytest.assert_eq(
        embed_footer.to_data(defaults = True, include_internals = True),
        expected_output,
    )
