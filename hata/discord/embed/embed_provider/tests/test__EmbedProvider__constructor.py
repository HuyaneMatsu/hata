import vampytest

from ..provider import EmbedProvider


def _assert_fields_set(embed_provider):
    """
    Checks whether every fields of the given embed provider are set.
    
    Parameters
    ----------
    embed_provider : ``EmbedProvider``
        The field to check.
    """
    vampytest.assert_instance(embed_provider, EmbedProvider)
    vampytest.assert_instance(embed_provider.name, str, nullable = True)
    vampytest.assert_instance(embed_provider.url, str, nullable = True)


def test__EmbedProvider__new__no_fields():
    """
    Tests whether ``EmbedProvider.__new__`` works as intended.
    
    Case: Minimal amount of parameters.
    """
    embed_provider = EmbedProvider()
    _assert_fields_set(embed_provider)


def test__EmbedProvider__new__all_fields():
    """
    Tests whether ``EmbedProvider.__new__`` works as intended.
    
    Case: Maximal amount of parameters.
    """
    name = 'orin'
    url = 'https://orindance.party/'
    
    embed_provider = EmbedProvider(name = name, url = url)
    _assert_fields_set(embed_provider)
    
    vampytest.assert_eq(embed_provider.name, name)
    vampytest.assert_eq(embed_provider.url, url)


def test__EmbedProvider__new__string_conversion():
    """
    Tests whether ``EmbedProvider.__new__`` works as intended.
    
    Case: name conversion check.
    """
    name = 123
    
    embed_provider = EmbedProvider(name = name)
    _assert_fields_set(embed_provider)
    
    vampytest.assert_eq(embed_provider.name, str(name))
