import vampytest

from ..unicode_type import Unicode


def test__Unicode__constructor_0():
    """
    Tests whether ``Unicode``'s `__repr__` works as intended.
    """
    name = 'owo'
    value_raw = b'56'
    value =  '56'
    variation_selector_16 = False
    emoticons = ('anya',)
    aliases = ('got', 'banned')
    
    unicode = Unicode(name, value_raw, variation_selector_16, emoticons, aliases)
    
    vampytest.assert_eq(unicode.name, name)
    vampytest.assert_eq(unicode.value, value)
    vampytest.assert_eq(unicode.variation_selector_16, variation_selector_16)
    vampytest.assert_eq(unicode.emoticons, emoticons)
    vampytest.assert_eq(unicode.aliases, aliases)
