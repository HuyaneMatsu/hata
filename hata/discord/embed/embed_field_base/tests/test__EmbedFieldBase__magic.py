import vampytest

from ..base import EmbedFieldBase


def test__EmbedFieldBase__repr():
    """
    Tests whether ``EmbedFieldBase.__repr__`` works as intended.
    """
    field_base = EmbedFieldBase()
    vampytest.assert_instance(repr(field_base), str)


def test__EmbedFieldBase__hash():
    """
    Tests whether ``EmbedFieldBase.__hash__`` works as intended.
    """
    field_base = EmbedFieldBase()
    vampytest.assert_instance(hash(field_base), int)


def _iter_options__eq():
    keyword_parameters = {}
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__EmbedFieldBase__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``EmbedFieldBase.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    guild_profile_0 = EmbedFieldBase(**keyword_parameters_0)
    guild_profile_1 = EmbedFieldBase(**keyword_parameters_1)
    
    output = guild_profile_0 == guild_profile_1
    vampytest.assert_instance(output, bool)
    return output


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
    field_base = EmbedFieldBase(**keyword_parameters)
    output = bool(field_base)
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__len():
    yield {}, 0


@vampytest._(vampytest.call_from(_iter_options__len()).returning_last())
def test__EmbedFieldBase__len(keyword_parameters):
    """
    Tests whether ``EmbedFieldBase.__len__`` works as intended.
    """
    field_base = EmbedFieldBase(**keyword_parameters)
    output = len(field_base)
    vampytest.assert_instance(output, int)
    return output
