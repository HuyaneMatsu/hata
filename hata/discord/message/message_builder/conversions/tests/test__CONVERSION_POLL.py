import vampytest

from .....poll import Poll, PollQuestion

from ..poll import CONVERSION_POLL


def _iter_options__set_validator():
    poll = Poll(question = PollQuestion(text = 'hey mister'))
    
    yield object(), []
    yield None, [None]
    yield poll, [poll]


@vampytest._(vampytest.call_from(_iter_options__set_validator()).returning_last())
def test__CONVERSION_POLL__set_validator(input_value):
    """
    Tests whether ``CONVERSION_POLL.set_validator`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test.
    
    Returns
    -------
    output : `list<None | Poll>`
    """
    return [*CONVERSION_POLL.set_validator(input_value)]


def _iter_options__serializer_optional():
    poll = Poll(question = PollQuestion(text = 'hey mister'))
    
    yield None, []
    yield poll, [poll.to_data()]


@vampytest._(vampytest.call_from(_iter_options__serializer_optional()).returning_last())
def test__CONVERSION_POLL__serializer_optional(input_value):
    """
    Tests whether ``CONVERSION_POLL.serializer_optional`` works as intended.
    
    Parameters
    ----------
    input_value : `None | Poll`
        Value to test.
    
    Returns
    -------
    output : `list<Poll>`
    """
    return [*CONVERSION_POLL.serializer_optional(input_value)]


def _iter_options__serializer_required():
    poll = Poll(question = PollQuestion(text = 'hey mister'))
    
    yield None, None
    yield poll, poll.to_data()


@vampytest._(vampytest.call_from(_iter_options__serializer_required()).returning_last())
def test__CONVERSION_POLL__serializer_required(input_value):
    """
    Tests whether ``CONVERSION_POLL.serializer_required`` works as intended.
    
    Parameters
    ----------
    input_value : `None | Poll`
        Value to test.
    
    Returns
    -------
    output : `Poll`
    """
    return CONVERSION_POLL.serializer_required(input_value)
