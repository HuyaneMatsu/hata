import vampytest

from ..poll_question import PollQuestion


def _assert_fields_set(poll_question):
    """
    Checks whether the poll question has every of its fields set.
    
    Parameters
    ----------
    poll_question : ``PollQuestion``
        The poll question to check.
    """
    vampytest.assert_instance(poll_question, PollQuestion)
    vampytest.assert_instance(poll_question.text, str, nullable = True)


def test__PollQuestion__new__no_fields():
    """
    Tests whether ``PollQuestion.__new__`` works as intended.
    
    Case: No fields given.
    """
    poll_question = PollQuestion()
    _assert_fields_set(poll_question)


def test__PollQuestion__new__all_fields():
    """
    Tests whether ``PollQuestion.__new__`` works as intended.
    
    Case: All fields given.
    """
    text = 'orin'
    
    poll_question = PollQuestion(text = text)
    _assert_fields_set(poll_question)
    
    vampytest.assert_eq(poll_question.text, text)
