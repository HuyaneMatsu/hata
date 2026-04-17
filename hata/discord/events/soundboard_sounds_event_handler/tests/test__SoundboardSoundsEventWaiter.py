import vampytest

from scarletio import Future

from ..soundboard_sounds_event_waiter import SoundboardSoundsEventWaiter


def _assert_fields_set(waiter):
    """
    Asserts whether every fields aer set of the given soundboard sound event waiter.
    
    Parameters
    ----------
    waiter : ``SoundboardSoundsEventWaiter``
        The waiter to check.
    """
    vampytest.assert_instance(waiter, SoundboardSoundsEventWaiter)
    vampytest.assert_instance(waiter.counter, int)
    vampytest.assert_instance(waiter.future, Future)


def test__SoundboardSoundsEventWaiter__new():
    """
    Tests whether ``SoundboardSoundsEventWaiter.__new__`` works as intended.
    """
    waiter = SoundboardSoundsEventWaiter()
    _assert_fields_set(waiter)
    # Counter should be 1 by default
    vampytest.assert_eq(waiter.counter, 1)


def test__SoundboardSoundsEventWaiter__repr():
    """
    Tests whether ``SoundboardSoundsEventWaiter.__repr__`` works as intended.
    """
    waiter = SoundboardSoundsEventWaiter()
    vampytest.assert_instance(repr(waiter), str)
