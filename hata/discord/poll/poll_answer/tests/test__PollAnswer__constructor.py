import vampytest

from ....core import BUILTIN_EMOJIS
from ....emoji import Emoji

from ..poll_answer import PollAnswer


def _assert_fields_set(poll_answer):
    """
    Checks whether the poll answer has all of its fields set.
    
    Parameters
    ----------
    poll_answer : ``PollAnswer``
        The poll answer to check.
    """
    vampytest.assert_instance(poll_answer, PollAnswer)
    vampytest.assert_instance(poll_answer.emoji, Emoji, nullable = True)
    vampytest.assert_instance(poll_answer.id, int)
    vampytest.assert_instance(poll_answer.text, str, nullable = True)


def test__PollAnswer__new__no_fields():
    """
    Tests whether ``PollAnswer.__new__`` works as intended.
    
    Case: No fields given.
    """
    poll_answer = PollAnswer()
    _assert_fields_set(poll_answer)


def test__PollAnswer__new__all_fields():
    """
    Tests whether ``PollAnswer.__new__`` works as intended.
    
    Case: All fields given.
    """
    emoji = BUILTIN_EMOJIS['heart']
    text = 'orin'
    
    poll_answer = PollAnswer(emoji = emoji, text = text)
    _assert_fields_set(poll_answer)
    
    vampytest.assert_is(poll_answer.emoji, emoji)
    vampytest.assert_eq(poll_answer.text, text)


def test__PollAnswer__precreate__no_fields():
    """
    Tests whether ``PollAnswer.precreate`` works as intended.
    
    Case: No fields given.
    """
    answer_id = 202404130010 
    
    poll_answer = PollAnswer.precreate(answer_id)
    _assert_fields_set(poll_answer)
    
    vampytest.assert_eq(poll_answer.id, answer_id)


def test__PollAnswer__precreate__all_fields():
    """
    Tests whether ``PollAnswer.precreate`` works as intended.
    
    Case: All fields given.
    """
    emoji = BUILTIN_EMOJIS['heart']
    text = 'orin'
    answer_id = 202404130011
    
    poll_answer = PollAnswer.precreate(answer_id, emoji = emoji, text = text)
    _assert_fields_set(poll_answer)
    
    vampytest.assert_is(poll_answer.emoji, emoji)
    vampytest.assert_eq(poll_answer.text, text)
    vampytest.assert_eq(poll_answer.id, answer_id)
