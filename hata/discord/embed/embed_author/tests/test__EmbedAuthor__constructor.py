import vampytest

from ..author import EmbedAuthor


def _assert_fields_set(embed_author):
    """
    Checks whether every fields of the given embed author are set.
    
    Parameters
    ----------
    embed_author : ``EmbedAuthor``
        The field to check.
    """
    vampytest.assert_instance(embed_author, EmbedAuthor)
    vampytest.assert_instance(embed_author.icon_url, str, nullable = True)
    vampytest.assert_instance(embed_author.icon_proxy_url, str, nullable = True)
    vampytest.assert_instance(embed_author.name, str, nullable = True)
    vampytest.assert_instance(embed_author.url, str, nullable = True)


def test__EmbedAuthor__new__no_fields():
    """
    Tests whether ``EmbedAuthor.__new__`` works as intended.
    
    Case: Minimal amount of parameters.
    """
    embed_author = EmbedAuthor()
    _assert_fields_set(embed_author)


def test__EmbedAuthor__new__all_fields():
    """
    Tests whether ``EmbedAuthor.__new__`` works as intended.
    
    Case: Maximal amount of parameters.
    """
    icon_url = 'attachment://orin.png'
    name = 'orin'
    url = 'https://orindance.party/'
    
    embed_author = EmbedAuthor(name = name, icon_url = icon_url, url = url)
    _assert_fields_set(embed_author)
    
    vampytest.assert_eq(embed_author.icon_url, icon_url)
    vampytest.assert_eq(embed_author.name, name)
    vampytest.assert_eq(embed_author.url, url)


def test__EmbedAuthor__new__string_conversion():
    """
    Tests whether ``EmbedAuthor.__new__`` works as intended.
    
    Case: string conversion check.
    """
    name = 123
    
    embed_author = EmbedAuthor(name = name)
    _assert_fields_set(embed_author)
    
    vampytest.assert_eq(embed_author.name, str(name))
