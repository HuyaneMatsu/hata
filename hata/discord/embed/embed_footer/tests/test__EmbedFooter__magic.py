import vampytest

from ..footer import EmbedFooter


def test__EmbedFooter__repr():
    """
    Tests whether ``EmbedFooter.__repr__`` works as intended.
    """
    icon_url = 'attachment://orin.png'
    text = 'orin'
    
    field = EmbedFooter(text = text, icon_url = icon_url)
    vampytest.assert_instance(repr(field), str)


def test__EmbedFooter__hash():
    """
    Tests whether ``EmbedFooter.__hash__`` works as intended.
    """
    icon_url = 'attachment://orin.png'
    text = 'orin'
    url = 'https://orindance.party/'
    
    field = EmbedFooter(text = text, icon_url = icon_url)
    vampytest.assert_instance(hash(field), int)


def test__EmbedFooter__eq():
    """
    Tests whether ``EmbedFooter.__eq__`` works as intended.
    """
    icon_url = 'attachment://orin.png'
    text = 'orin'
    
    keyword_parameters = {
        'icon_url': icon_url,
        'text': text,
    }
    
    field = EmbedFooter(**keyword_parameters)
    
    vampytest.assert_eq(field, field)
    vampytest.assert_ne(field, object())
    
    for field_name, field_value in (
        ('icon_url', 'attachment://rin.png'),
        ('text', 'rin'),
    ):
        test_field = EmbedFooter(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(field, test_field)


def test__EmbedFooter__bool():
    """
    Tests whether ``EmbedFooter.__bool__`` works as intended.
    """
    icon_url = 'attachment://orin.png'
    text = 'orin'
    
    for field, expected_output in (
        (EmbedFooter(), False),
        (EmbedFooter(text = text), True),
        (EmbedFooter(icon_url = icon_url), True),
        (EmbedFooter(icon_url = icon_url, text = text), True),
    ):
        vampytest.assert_eq(bool(field), expected_output)



def test__EmbedFooter__len():
    """
    Tests whether ``EmbedFooter.__len__`` works as intended.
    """
    icon_url = 'attachment://orin.png'
    text = 'orin'
    
    for field, expected_output in (
        (EmbedFooter(), 0),
        (EmbedFooter(text = text), len(text)),
        (EmbedFooter(icon_url = icon_url), 0),
        (EmbedFooter(icon_url = icon_url, text = text), len(text)),
    ):
        vampytest.assert_eq(len(field), expected_output)
