import vampytest

from ..footer import EmbedFooter


def _assert_fields_set(embed_footer):
    """
    Checks whether every fields of the given embed footer are set.
    
    Parameters
    ----------
    embed_footer : ``EmbedFooter``
        The field to check.
    """
    vampytest.assert_instance(embed_footer, EmbedFooter)
    vampytest.assert_instance(embed_footer.icon_url, str, nullable = True)
    vampytest.assert_instance(embed_footer.icon_proxy_url, str, nullable = True)
    vampytest.assert_instance(embed_footer.text, str, nullable = True)


def test__EmbedFooter__new__no_fields():
    """
    Tests whether ``EmbedFooter.__new__`` works as intended.
    
    Case: Minimal amount of parameters.
    """
    embed_footer = EmbedFooter()
    _assert_fields_set(embed_footer)


def test__EmbedFooter__new__all_field():
    """
    Tests whether ``EmbedFooter.__new__`` works as intended.
    
    Case: Maximal amount of parameters.
    """
    icon_url = 'attachment://orin.png'
    text = 'orin'
    
    embed_footer = EmbedFooter(text = text, icon_url = icon_url)
    _assert_fields_set(embed_footer)
    
    vampytest.assert_eq(embed_footer.icon_url, icon_url)
    vampytest.assert_eq(embed_footer.text, text)


def test__EmbedFooter__new__string_conversion():
    """
    Tests whether ``EmbedFooter.__new__`` works as intended.
    
    Case: text conversion check.
    """
    text = 123
    
    embed_footer = EmbedFooter(text = text)
    _assert_fields_set(embed_footer)
    
    vampytest.assert_eq(embed_footer.text, str(text))
