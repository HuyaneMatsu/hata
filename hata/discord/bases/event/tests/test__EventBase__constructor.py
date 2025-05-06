import vampytest

from ..event_base import EventBase


def _assert_fields_set(event_base):
    """
    Asserts whether the given event base has all of its attributes set.
    
    Parameters
    ----------
    event_base : ``EventBase``
        The instance to test.
    """
    vampytest.assert_instance(event_base, EventBase)


def test__EventBase__new():
    """
    Tests whether ``EventBase.__new__`` works as intended.
    """
    event_base = EventBase()
    _assert_fields_set(event_base)


def test__EventBase__from_fields():
    """
    Tests whether ``EventBase.from_fields`` works as intended.
    """
    event_base = EventBase.from_fields()
    _assert_fields_set(event_base)
