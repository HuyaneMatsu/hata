import vampytest

from ....core import BUILTIN_EMOJIS
from ....user import User

from ..poll_answer import PollAnswer

from .test__PollAnswer__constructor import _assert_fields_set


def test__PollAnswer__clean_copy():
    """
    Tests whether ``PollAnswer.clean_copy`` works as intended.
    """
    user = User.precreate(202404100000, name = 'koishi')
    
    emoji = BUILTIN_EMOJIS['heart']
    text = user.mention
    
    poll_answer = PollAnswer(emoji = emoji, text = text)
    copy = poll_answer.clean_copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(poll_answer, copy)
    
    vampytest.assert_is(copy.emoji, emoji)
    vampytest.assert_eq(copy.text, f'@{user.name}')


def test__PollAnswer__copy():
    """
    Tests whether ``PollAnswer.copy`` works as intended.
    """
    emoji = BUILTIN_EMOJIS['heart']
    text = 'orin'
    
    poll_answer = PollAnswer(emoji = emoji, text = text)
    copy = poll_answer.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(poll_answer, copy)
    
    vampytest.assert_eq(poll_answer, copy)


def test__PollAnswer__copy_with__no_fields():
    """
    Tests whether ``PollAnswer.copy_with`` works as intended.
    
    Case: No fields given.
    """
    emoji = BUILTIN_EMOJIS['heart']
    text = 'orin'
    
    poll_answer = PollAnswer(emoji = emoji, text = text)
    copy = poll_answer.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(poll_answer, copy)
    
    vampytest.assert_eq(poll_answer, copy)


def test__PollAnswer__copy_with__all_fields():
    """
    Tests whether ``PollAnswer.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_emoji = BUILTIN_EMOJIS['heart']
    old_text = 'orin'
    
    new_emoji = BUILTIN_EMOJIS['x']
    new_text = 'rin'
    
    poll_answer = PollAnswer(emoji = old_emoji, text = old_text)
    copy = poll_answer.copy_with(
        emoji = new_emoji,
        text = new_text,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(poll_answer, copy)
    
    vampytest.assert_is(copy.emoji, new_emoji)
    vampytest.assert_eq(copy.text, new_text)


def _iter_options__contents():
    emoji = BUILTIN_EMOJIS['heart']
    text = 'orin'
    
    yield {}, set()
    yield {'text': text}, {text}
    yield {'emoji': emoji}, set()
    yield {'text': text, 'emoji': emoji}, {text}


@vampytest._(vampytest.call_from(_iter_options__contents()).returning_last())
def test__PollAnswer__contents(keyword_parameters):
    """
    Tests whether ``PollAnswer.contents`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the poll answer with.
    
    Returns
    -------
    output : `set<str>`
    """
    poll_answer = PollAnswer(**keyword_parameters)
    output = poll_answer.contents
    vampytest.assert_instance(output, list)
    return {*output}


def _iter_options__iter_contents():
    emoji = BUILTIN_EMOJIS['heart']
    text = 'orin'
    
    yield {}, set()
    yield {'text': text}, {text}
    yield {'emoji': emoji}, set()
    yield {'text': text, 'emoji': emoji}, {text}


@vampytest._(vampytest.call_from(_iter_options__iter_contents()).returning_last())
def test__PollAnswer__iter_contents(keyword_parameters):
    """
    Tests whether ``PollAnswer.iter_contents`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the poll answer with.
    
    Returns
    -------
    output : `set<str>`
    """
    poll_answer = PollAnswer(**keyword_parameters)
    return {*poll_answer.iter_contents()}
