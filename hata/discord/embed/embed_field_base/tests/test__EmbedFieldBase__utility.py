import vampytest

from ..base import EmbedFieldBase

from .test__EmbedFieldBase__constructor import _assert_fields_set


def test__EmbedFieldBase__clean_copy():
    """
    Tests whether ``EmbedFieldBase.clean_copy`` works as intended.
    """
    field = EmbedFieldBase()
    copy = field.clean_copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(field, copy)


def test__EmbedFieldBase__copy():
    """
    Tests whether ``EmbedFieldBase.copy`` works as intended.
    """
    field = EmbedFieldBase()
    copy = field.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(field, copy)
    
    vampytest.assert_eq(field, copy)


def test__EmbedFieldBase__copy_with__0():
    """
    Tests whether ``EmbedFieldBase.copy_with`` works as intended.
    
    Case: No fields given.
    """
    field = EmbedFieldBase()
    copy = field.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(field, copy)
    
    vampytest.assert_eq(field, copy)


def test__EmbedFieldBase__contents():
    """
    Tests whether ``EmbedFieldBase.contents`` works as intended.
    """
    for field, expected_output in (
        (EmbedFieldBase(), set()),
    ):
        output = field.contents
        vampytest.assert_instance(output, list)
        vampytest.assert_eq({*output}, expected_output)


def test__EmbedFieldBase__iter_contents():
    """
    Tests whether ``EmbedFieldBase.iter_contents`` works as intended.
    """
    for field, expected_output in (
        (EmbedFieldBase(), set()),
    ):
        vampytest.assert_eq({*field.iter_contents()}, expected_output)
