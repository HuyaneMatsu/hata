import vampytest

from ..provider import EmbedProvider


def _assert_fields_set(field):
    """
    Checks whether every fields of the given activity field are set.
    
    Parameters
    ----------
    field : ``EmbedProvider``
        The field to check.
    """
    vampytest.assert_instance(field, EmbedProvider)
    vampytest.assert_instance(field.name, str, nullable = True)
    vampytest.assert_instance(field.url, str, nullable = True)


def test__EmbedProvider__new__0():
    """
    Tests whether ``EmbedProvider.__new__`` works as intended.
    
    Case: Minimal amount of parameters.
    """
    field = EmbedProvider()
    _assert_fields_set(field)


def test__EmbedProvider__new__1():
    """
    Tests whether ``EmbedProvider.__new__`` works as intended.
    
    Case: Maximal amount of parameters.
    """
    name = 'orin'
    url = 'https://orindance.party/'
    
    field = EmbedProvider(name = name, url = url)
    _assert_fields_set(field)
    
    vampytest.assert_eq(field.name, name)
    vampytest.assert_eq(field.url, url)


def test__EmbedProvider__new__2():
    """
    Tests whether ``EmbedProvider.__new__`` works as intended.
    
    Case: name conversion check.
    """
    name = 123
    
    field = EmbedProvider(name = name)
    _assert_fields_set(field)
    
    vampytest.assert_eq(field.name, str(name))
