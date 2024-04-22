import vampytest

from ..footer import EmbedFooter


def _assert_fields_set(field):
    """
    Checks whether every fields of the given embed footer are set.
    
    Parameters
    ----------
    field : ``EmbedFooter``
        The field to check.
    """
    vampytest.assert_instance(field, EmbedFooter)
    vampytest.assert_instance(field.icon_url, str, nullable = True)
    vampytest.assert_instance(field.icon_proxy_url, str, nullable = True)
    vampytest.assert_instance(field.text, str, nullable = True)


def test__EmbedFooter__new__no_fields():
    """
    Tests whether ``EmbedFooter.__new__`` works as intended.
    
    Case: Minimal amount of parameters.
    """
    field = EmbedFooter()
    _assert_fields_set(field)


def test__EmbedFooter__new__all_field():
    """
    Tests whether ``EmbedFooter.__new__`` works as intended.
    
    Case: Maximal amount of parameters.
    """
    icon_url = 'attachment://orin.png'
    text = 'orin'
    
    field = EmbedFooter(text = text, icon_url = icon_url)
    _assert_fields_set(field)
    
    vampytest.assert_eq(field.icon_url, icon_url)
    vampytest.assert_eq(field.text, text)


def test__EmbedFooter__new__string_conversion():
    """
    Tests whether ``EmbedFooter.__new__`` works as intended.
    
    Case: text conversion check.
    """
    text = 123
    
    field = EmbedFooter(text = text)
    _assert_fields_set(field)
    
    vampytest.assert_eq(field.text, str(text))
