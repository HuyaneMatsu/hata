import vampytest

from ..author import EmbedAuthor


def _assert_fields_set(field):
    """
    Checks whether every fields of the given activity field are set.
    
    Parameters
    ----------
    field : ``EmbedAuthor``
        The field to check.
    """
    vampytest.assert_instance(field, EmbedAuthor)
    vampytest.assert_instance(field.icon_url, str, nullable = True)
    vampytest.assert_instance(field.icon_proxy_url, str, nullable = True)
    vampytest.assert_instance(field.name, str, nullable = True)
    vampytest.assert_instance(field.url, str, nullable = True)


def test__EmbedAuthor__new__0():
    """
    Tests whether ``EmbedAuthor.__new__`` works as intended.
    
    Case: Minimal amount of parameters.
    """
    field = EmbedAuthor()
    _assert_fields_set(field)


def test__EmbedAuthor__new__1():
    """
    Tests whether ``EmbedAuthor.__new__`` works as intended.
    
    Case: Maximal amount of parameters.
    """
    icon_url = 'attachment://orin.png'
    name = 'orin'
    url = 'https://orindance.party/'
    
    field = EmbedAuthor(name = name, icon_url = icon_url, url = url)
    _assert_fields_set(field)
    
    vampytest.assert_eq(field.icon_url, icon_url)
    vampytest.assert_eq(field.name, name)
    vampytest.assert_eq(field.url, url)


def test__EmbedAuthor__new__2():
    """
    Tests whether ``EmbedAuthor.__new__`` works as intended.
    
    Case: name conversion check.
    """
    name = 123
    
    field = EmbedAuthor(name = name)
    _assert_fields_set(field)
    
    vampytest.assert_eq(field.name, str(name))
