import vampytest

from ..provider import EmbedProvider


def test__EmbedProvider__repr():
    """
    Tests whether ``EmbedProvider.__repr__`` works as intended.
    """
    name = 'orin'
    url = 'https://orindance.party/'
    
    field = EmbedProvider(name = name, url = url)
    vampytest.assert_instance(repr(field), str)


def test__EmbedProvider__hash():
    """
    Tests whether ``EmbedProvider.__hash__`` works as intended.
    """
    name = 'orin'
    url = 'https://orindance.party/'
    
    field = EmbedProvider(name = name, url = url)
    vampytest.assert_instance(hash(field), int)


def test__EmbedProvider__eq():
    """
    Tests whether ``EmbedProvider.__eq__`` works as intended.
    """
    name = 'orin'
    url = 'https://orindance.party/'
    
    keyword_parameters = {
        'name': name,
        'url': url,
    }
    
    field = EmbedProvider(**keyword_parameters)
    
    vampytest.assert_eq(field, field)
    vampytest.assert_ne(field, object())
    
    for field_name, field_value in (
        ('name', 'rin'),
        ('url', 'https://www.astil.dev/'),
    ):
        test_field = EmbedProvider(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(field, test_field)



def _iter_options__bool():
    url = 'https://orindance.party/'
    name = 'orin'
    
    yield {}, False
    yield {'name': name}, True
    yield {'url': url}, True
    yield {'name': name, 'url': url}, True


@vampytest._(vampytest.call_from(_iter_options__bool()).returning_last())
def test__EmbedProvider__bool(keyword_parameters):
    """
    Tests whether ``EmbedProvider.__bool__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the embed provider with.
    
    Returns
    -------
    output : `bool`
    """
    field = EmbedProvider(**keyword_parameters)
    output = bool(field)
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__len():
    url = 'https://orindance.party/'
    name = 'orin'
    
    yield {}, 0
    yield {'name': name}, len(name)
    yield {'url': url}, 0
    yield {'name': name, 'url': url}, len(name)


@vampytest._(vampytest.call_from(_iter_options__len()).returning_last())
def test__EmbedProvider__len(keyword_parameters):
    """
    Tests whether ``EmbedProvider.__len__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the embed provider with.
    
    Returns
    -------
    output : `int`
    """
    field = EmbedProvider(**keyword_parameters)
    output = len(field)
    vampytest.assert_instance(output, int)
    return output
