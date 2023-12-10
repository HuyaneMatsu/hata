import vampytest

from ..unicode_type import Unicode


def test__Unicode__new():
    """
    Tests whether ``Unicode``'s `__repr__` works as intended.
    """
    name = 'owo'
    value = '56'
    variation_selector_16 = False
    emoticons = ('anya',)
    aliases = ('got', 'banned')
    unicode_aliases = ('54', '53')
    
    unicode = Unicode(name, value, variation_selector_16, aliases, emoticons, unicode_aliases)
    
    vampytest.assert_eq(unicode.name, name)
    vampytest.assert_eq(unicode.value, value)
    vampytest.assert_eq(unicode.variation_selector_16, variation_selector_16)
    vampytest.assert_eq(unicode.emoticons, emoticons)
    vampytest.assert_eq(unicode.aliases, aliases)
    vampytest.assert_eq(unicode.unicode_aliases, unicode_aliases)
