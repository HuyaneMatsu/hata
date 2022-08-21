import vampytest

from ..helpers import get_localized_length
from ..preinstanced import Locale


def test__get_localized_length__0():
    """
    Tests whether ``get_localized_length`` handles `None` values as expected.
    """
    length = get_localized_length(None, None)
    
    vampytest.assert_eq(length, 0)


def test__get_localized_length__1():
    """
    Tests whether ``get_localized_length`` handles the case when the `value` is the longest correctly.
    """
    value_1 = 'hi'
    value_2 = 'hoi'
    value_3 = 'halo'
    
    length = get_localized_length(
        value_3,
        {
            Locale.thai: value_1,
            Locale.czech: value_2,
        },
    )
    
    expected_length = max(
        len(value) for value in (value_1, value_2, value_3)
    )
    
    vampytest.assert_eq(length, expected_length)


def test__get_localized_length__2():
    """
    Tests whether ``get_localized_length`` handles the case when a value of ``value_localizations`` is the longest.
    """
    value_1 = 'hi'
    value_2 = 'hoi'
    value_3 = 'halo'
    
    length = get_localized_length(
        value_1,
        {
            Locale.thai: value_3,
            Locale.czech: value_2,
        },
    )
    
    expected_length = max(
        len(value) for value in (value_1, value_2, value_3)
    )
    
    vampytest.assert_eq(length, expected_length)
