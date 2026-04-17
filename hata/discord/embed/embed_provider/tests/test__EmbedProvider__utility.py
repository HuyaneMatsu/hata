import vampytest

from ....user import User

from ..provider import EmbedProvider

from .test__EmbedProvider__constructor import _assert_fields_set


def test__EmbedProvider__clean_copy():
    """
    Tests whether ``EmbedProvider.clean_copy`` works as intended.
    """
    user = User.precreate(202303310004, name = 'koishi')
    
    name = user.mention
    url = 'https://orindance.party/'
    
    embed_provider = EmbedProvider(name = name, url = url)
    copy = embed_provider.clean_copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(embed_provider, copy)
    
    vampytest.assert_eq(copy.name, f'@{user.name}')
    vampytest.assert_eq(copy.url, url)


def test__EmbedProvider__copy():
    """
    Tests whether ``EmbedProvider.copy`` works as intended.
    """
    name = 'orin'
    url = 'https://orindance.party/'
    
    embed_provider = EmbedProvider(name = name, url = url)
    copy = embed_provider.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(embed_provider, copy)
    
    vampytest.assert_eq(embed_provider, copy)


def test__EmbedProvider__copy_with__no_fields():
    """
    Tests whether ``EmbedProvider.copy_with`` works as intended.
    
    Case: No fields given.
    """
    name = 'orin'
    url = 'https://orindance.party/'
    
    embed_provider = EmbedProvider(name = name, url = url)
    copy = embed_provider.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(embed_provider, copy)
    
    vampytest.assert_eq(embed_provider, copy)


def test__EmbedProvider__copy_with__all_fields():
    """
    Tests whether ``EmbedProvider.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_name = 'orin'
    old_url = 'https://orindance.party/'
    
    new_name = 'rin'
    new_url = 'https://www.astil.dev/'
    
    embed_provider = EmbedProvider(name = old_name, url = old_url)
    copy = embed_provider.copy_with(
        name = new_name,
        url = new_url,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(embed_provider, copy)
    
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.url, new_url)


def _iter_options__contents():
    url = 'https://orindance.party/'
    name = 'orin'
    
    yield {}, set()
    yield {'name': name}, {name}
    yield {'url': url}, set()
    yield {'name': name, 'url': url}, {name}


@vampytest._(vampytest.call_from(_iter_options__contents()).returning_last())
def test__EmbedProvider__contents(keyword_parameters):
    """
    Tests whether ``EmbedProvider.contents`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the embed provider with.
    
    Returns
    -------
    output : `set<str>`
    """
    embed_provider = EmbedProvider(**keyword_parameters)
    output = embed_provider.contents
    vampytest.assert_instance(output, list)
    return {*output}


def _iter_options__iter_contents():
    url = 'https://orindance.party/'
    name = 'orin'
    
    yield {}, set()
    yield {'name': name}, {name}
    yield {'url': url}, set()
    yield {'name': name, 'url': url}, {name}


@vampytest._(vampytest.call_from(_iter_options__iter_contents()).returning_last())
def test__EmbedProvider__iter_contents(keyword_parameters):
    """
    Tests whether ``EmbedProvider.iter_contents`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the embed provider with.
    
    Returns
    -------
    output : `set<str>`
    """
    embed_provider = EmbedProvider(**keyword_parameters)
    return {*embed_provider.iter_contents()}
