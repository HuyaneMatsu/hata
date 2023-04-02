import vampytest

from ..base import EmbedFieldBase


def test__EmbedFieldBase__repr():
    """
    Tests whether ``EmbedFieldBase.__repr__`` works as intended.
    """
    field = EmbedFieldBase()
    vampytest.assert_instance(repr(field), str)


def test__EmbedFieldBase__hash():
    """
    Tests whether ``EmbedFieldBase.__hash__`` works as intended.
    """
    field = EmbedFieldBase()
    vampytest.assert_instance(hash(field), int)


def test__EmbedFieldBase__eq():
    """
    Tests whether ``EmbedFieldBase.__eq__`` works as intended.
    """
    keyword_parameters = {}
    
    field = EmbedFieldBase(**keyword_parameters)
    
    vampytest.assert_eq(field, field)
    vampytest.assert_ne(field, object())
    
    for field_name, field_value in (
    ):
        test_field = EmbedFieldBase(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(field, test_field)


def test__EmbedFieldBase__bool():
    """
    Tests whether ``EmbedFieldBase.__bool__`` works as intended.
    """
    for field, expected_output in (
        (EmbedFieldBase(), False),
    ):
        vampytest.assert_eq(bool(field), expected_output)


def test__EmbedFieldBase__len():
    """
    Tests whether ``EmbedFieldBase.__len__`` works as intended.
    """
    for field, expected_output in (
        (EmbedFieldBase(), 0),
    ):
        vampytest.assert_eq(len(field), expected_output)
