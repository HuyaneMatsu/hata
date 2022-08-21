import vampytest

from ..unicodes import UNICODES


def test__UNICODES():
    """
    Tests whether all unicodes are structured as expected.
    """
    for unicode in UNICODES:
        vampytest.assert_instance(unicode.name, str)
        vampytest.assert_instance(unicode.value, str)
        vampytest.assert_instance(unicode.variation_selector_16, bool)
        
        if unicode.variation_selector_16:
            vampytest.assert_is(unicode.aliases, None)
            vampytest.assert_is(unicode.emoticons, None)
        else:
            vampytest.assert_instance(unicode.aliases, tuple, nullable=True)
            vampytest.assert_instance(unicode.emoticons, tuple, nullable=True)
        
        for alternative_name in unicode.iter_alternative_names():
            vampytest.assert_instance(alternative_name, str)
