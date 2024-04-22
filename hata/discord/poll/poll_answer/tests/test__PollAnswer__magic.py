import vampytest

from ....core import BUILTIN_EMOJIS

from ..poll_answer import PollAnswer


def test__PollAnswer__repr():
    """
    Tests whether ``PollAnswer.__repr__`` works as intended.
    """
    emoji = BUILTIN_EMOJIS['heart']
    text = 'orin'
    answer_id = 202404130014
    
    poll_answer = PollAnswer.precreate(answer_id, emoji = emoji, text = text)
    vampytest.assert_instance(repr(poll_answer), str)


def test__PollAnswer__hash():
    """
    Tests whether ``PollAnswer.__hash__`` works as intended.
    """
    emoji = BUILTIN_EMOJIS['heart']
    text = 'orin'
    answer_id = 202404130013
    
    poll_answer = PollAnswer.precreate(answer_id, emoji = emoji, text = text)
    vampytest.assert_instance(hash(poll_answer), int)


def test__PollAnswer__eq():
    """
    Tests whether ``PollAnswer.__eq__`` works as intended.
    """
    emoji = BUILTIN_EMOJIS['heart']
    text = 'orin'
    answer_id_0 = 202404130015
    answer_id_1 = 202404130016
    
    keyword_parameters = {
        'emoji': emoji,
        'text': text,
    }
    
    poll_answer = PollAnswer.precreate(answer_id_0, **keyword_parameters)
    
    vampytest.assert_eq(poll_answer, poll_answer)
    vampytest.assert_ne(poll_answer, object())
    
    test_poll_answer = PollAnswer(**keyword_parameters)
    vampytest.assert_eq(poll_answer, test_poll_answer)
    
    test_poll_answer = PollAnswer.precreate(answer_id_1, **keyword_parameters)
    vampytest.assert_ne(poll_answer, test_poll_answer)
    
    for poll_answer_name, poll_answer_value in (
        ('emoji', BUILTIN_EMOJIS['x']),
        ('text', 'rin'),
    ):
        test_poll_answer = PollAnswer(**{**keyword_parameters, poll_answer_name: poll_answer_value})
        vampytest.assert_ne(poll_answer, test_poll_answer)


def _iter_options__bool():
    emoji = BUILTIN_EMOJIS['heart']
    text = 'orin'
    
    yield {}, False
    yield {'text': text}, True
    yield {'emoji': emoji}, True
    yield {'text': text, 'emoji': emoji}, True


@vampytest._(vampytest.call_from(_iter_options__bool()).returning_last())
def test__PollAnswer__bool(keyword_parameters):
    """
    Tests whether ``PollAnswer.__bool__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the poll answer with.
    
    Returns
    -------
    output : `bool`
    """
    poll_answer = PollAnswer(**keyword_parameters)
    output = bool(poll_answer)
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__len():
    emoji = BUILTIN_EMOJIS['heart']
    text = 'orin'
    
    yield {}, 0
    yield {'text': text}, len(text)
    yield {'emoji': emoji}, 0
    yield {'text': text, 'emoji': emoji}, len(text)


@vampytest._(vampytest.call_from(_iter_options__len()).returning_last())
def test__PollAnswer__len(keyword_parameters):
    """
    Tests whether ``PollAnswer.__len__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the poll answer with.
    
    Returns
    -------
    output : `int`
    """
    poll_answer = PollAnswer(**keyword_parameters)
    output = len(poll_answer)
    vampytest.assert_instance(output, int)
    return output
