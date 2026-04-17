import vampytest

from ..event_base import EventBase


def test__EventBase__repr():
    """
    Tests whether ``EventBase.__repr__`` works as intended.
    """
    event_base = EventBase()
    
    output = repr(event_base)
    
    vampytest.assert_instance(output, str)
    vampytest.assert_in(type(event_base).__name__, output)


def test__EventBase__unpack():
    """
    Tests whether ``EventBase`` unpacking works as intended.
    """
    event_base = EventBase()
    
    vampytest.assert_eq(
        len([*event_base]),
        len(event_base),
    )


def test__EventBase__hash():
    """
    Tests whether ``EventBase.__hash__`` works as intended.
    """
    event_base = EventBase()
    
    output = hash(event_base)
    
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    keyword_parameters = {}
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__EventBase__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``EventBase.__eq__`` works as intended.
    
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
    event_base_0 = EventBase(**keyword_parameters_0)
    event_base_1 = EventBase(**keyword_parameters_1)
    
    output = event_base_0 == event_base_1
    vampytest.assert_instance(output, bool)
    return output
