from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..message_call import MessageCall


def test__MessageCall__repr():
    """
    Tests whether ``MessageCall.__repr__`` works as intended.
    """
    ended_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    user_ids = [202304280006, 202304280007]
    
    message_call = MessageCall(
        ended_at = ended_at,
        user_ids = user_ids,
    )
    
    vampytest.assert_instance(repr(message_call), str)


def test__MessageCall__hash():
    """
    Tests whether ``MessageCall.__hash__`` works as intended.
    """
    ended_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    user_ids = [202304280008, 202304280009]
    
    message_call = MessageCall(
        ended_at = ended_at,
        user_ids = user_ids,
    )
    
    vampytest.assert_instance(hash(message_call), int)


def _iter_options__eq__different_type():
    yield object(), False


@vampytest._(vampytest.call_from(_iter_options__eq__different_type()).returning_last())
def test__messageCall__eq__different_type(other):
    """
    Tests whether ``MessageCall.__eq__`` works as intended.
    
    Case: Different type.
    
    Parameters
    ----------
    other : `object`
        Object to compare to.
    
    Returns
    -------
    output : `bool`
    """
    ended_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    user_ids = [202304280008, 202304280009]
    
    message_call = MessageCall(
        ended_at = ended_at,
        user_ids = user_ids,
    )
    
    output = message_call == other
    vampytest.assert_instance(output, bool)
    return output



def _iter_options__eq__same_type():
    ended_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    user_ids = [202304280063, 202304280064]
    
    keyword_parameters = {
        'ended_at': ended_at,
        'user_ids': user_ids,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'ended_at': DateTime(2016, 5, 15, tzinfo = TimeZone.utc),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'user_ids': [202304280065, 202304280066],
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq__same_type()).returning_last())
def test__messageCall__eq__same_type(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``MessageCall.__eq__`` works as intended.
    
    Case: Different type.
    
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
    message_call_0 = MessageCall(**keyword_parameters_0)
    message_call_1 = MessageCall(**keyword_parameters_1)
    
    output = message_call_0 == message_call_1
    vampytest.assert_instance(output, bool)
    return output
