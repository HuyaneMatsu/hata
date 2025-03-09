import vampytest

from ..event_base import EventBase

from .test__EventBase__constructor import _assert_fields_set


def test__EventBase__from_data():
    """
    Tests whether ``EventBase.from_data`` works as intended.
    """
    data = {}
    
    event_base = EventBase.from_data(data)
    _assert_fields_set(event_base)


def test__EventBase__to_data():
    """
    Tests whether ``EventBase.to_data`` works as intended.
    """
    event_base = EventBase()
    
    data = event_base.to_data(defaults = True)
    
    vampytest.assert_eq(data, {})
