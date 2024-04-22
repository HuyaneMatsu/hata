import vampytest

from ..poll_question import PollQuestion

from .test__PollQuestion__constructor import _assert_fields_set


def test__PollQuestion__from_data():
    """
    Tests whether ``PollQuestion.from_data`` works as intended.
    """
    text = 'orin'
    
    data = {
        'text': text,
    }
    
    poll_question = PollQuestion.from_data(data)
    _assert_fields_set(poll_question)
    
    vampytest.assert_eq(poll_question.text, text)


def test__PollQuestion__to_data():
    """
    Tests whether ``PollQuestion.to_data`` works as intended.
    
    Case: Include defaults & internals.
    """
    text = 'orin'
    
    data = {
        'text': text,
    }
    
    poll_question = PollQuestion.from_data(data)
    
    expected_output = data
    
    vampytest.assert_eq(
        poll_question.to_data(defaults = True, include_internals = True),
        expected_output,
    )
