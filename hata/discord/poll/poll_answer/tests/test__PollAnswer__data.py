import vampytest

from ....core import BUILTIN_EMOJIS

from ..poll_answer import PollAnswer

from .test__PollAnswer__constructor import _assert_fields_set


def test__PollAnswer__from_data():
    """
    Tests whether ``PollAnswer.from_data`` works as intended.
    """
    emoji = BUILTIN_EMOJIS['heart']
    text = 'orin'
    answer_id = 202404130012
    
    data = {
        'poll_media': {
            'emoji': {
                'name': emoji.unicode,
            },
            'text': text,
        },
        'answer_id': str(answer_id),
    }
    
    poll_answer = PollAnswer.from_data(data)
    _assert_fields_set(poll_answer)
    
    vampytest.assert_is(poll_answer.emoji, emoji)
    vampytest.assert_eq(poll_answer.text, text)
    vampytest.assert_eq(poll_answer.id, answer_id)


def test__PollAnswer__to_data():
    """
    Tests whether ``PollAnswer.to_data`` works as intended.
    
    Case: Include defaults & internals.
    """
    emoji = BUILTIN_EMOJIS['heart']
    text = 'orin'
    answer_id = 202404130013
    
    poll_answer = PollAnswer.precreate(
        answer_id,
        emoji = emoji,
        text = text,
    )
    
    expected_output = {
        'poll_media': {
            'emoji': {
                'name': emoji.unicode,
            },
            'text': text,
        },
        'answer_id': str(answer_id),
    }
    
    vampytest.assert_eq(
        poll_answer.to_data(defaults = True, include_internals = True),
        expected_output,
    )
