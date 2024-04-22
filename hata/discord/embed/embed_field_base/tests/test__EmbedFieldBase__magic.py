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


def _iter_options__bool():
    yield {}, False


@vampytest._(vampytest.call_from(_iter_options__bool()).returning_last())
def test__EmbedFieldBase__bool(keyword_parameters):
    """
    Tests whether ``EmbedFieldBase.__bool__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the embed field with.
    
    Returns
    -------
    output : `bool`
    """
    field = EmbedFieldBase(**keyword_parameters)
    output = bool(field)
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__len():
    yield {}, 0


@vampytest._(vampytest.call_from(_iter_options__len()).returning_last())
def test__EmbedFieldBase__len(keyword_parameters):
    """
    Tests whether ``EmbedFieldBase.__len__`` works as intended.
    """
    field = EmbedFieldBase(**keyword_parameters)
    output = len(field)
    vampytest.assert_instance(output, int)
    return output
