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


def test__EmbedFieldBase__copy_with__no_fields():
    """
    Tests whether ``EmbedFieldBase.copy_with`` works as intended.
    
    Case: No fields given.
    """
    field = EmbedFieldBase()
    copy = field.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(field, copy)
    
    vampytest.assert_eq(field, copy)


def _iter_options__contents():
    yield {}, set()


@vampytest._(vampytest.call_from(_iter_options__contents()).returning_last())
def test__EmbedFieldBase__contents(keyword_parameters):
    """
    Tests whether ``EmbedFieldBase.contents`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the embed field with.
    
    Returns
    -------
    output : `set<str>`
    """
    field = EmbedFieldBase(**keyword_parameters)
    output = field.contents
    vampytest.assert_instance(output, list)
    return {*output}


def _iter_options__iter_contents():
    yield {}, set()


@vampytest._(vampytest.call_from(_iter_options__iter_contents()).returning_last())
def test__EmbedFieldBase__iter_contents(keyword_parameters):
    """
    Tests whether ``EmbedFieldBase.iter_contents`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the embed field with.
    
    Returns
    -------
    output : `set<str>`
    """
    field = EmbedFieldBase(**keyword_parameters)
    return {*field.iter_contents()}
