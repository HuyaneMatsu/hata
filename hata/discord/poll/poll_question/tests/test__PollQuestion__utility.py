import vampytest

from ....user import User

from ..poll_question import PollQuestion

from .test__PollQuestion__constructor import _assert_fields_set


def test__PollQuestion__clean_copy():
    """
    Tests whether ``PollQuestion.clean_copy`` works as intended.
    """
    user = User.precreate(202404100000, name = 'koishi')
    
    text = user.mention
    
    poll_question = PollQuestion(text = text)
    copy = poll_question.clean_copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(poll_question, copy)
    
    vampytest.assert_eq(copy.text, f'@{user.name}')


def test__PollQuestion__copy():
    """
    Tests whether ``PollQuestion.copy`` works as intended.
    """
    text = 'orin'
    
    poll_question = PollQuestion(text = text)
    copy = poll_question.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(poll_question, copy)
    
    vampytest.assert_eq(poll_question, copy)


def test__PollQuestion__copy_with__no_fields():
    """
    Tests whether ``PollQuestion.copy_with`` works as intended.
    
    Case: No fields given.
    """
    text = 'orin'
    
    poll_question = PollQuestion(text = text)
    copy = poll_question.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(poll_question, copy)
    
    vampytest.assert_eq(poll_question, copy)


def test__PollQuestion__copy_with__all_fields():
    """
    Tests whether ``PollQuestion.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_text = 'orin'
    
    new_text = 'rin'
    
    poll_question = PollQuestion(text = old_text)
    copy = poll_question.copy_with(
        text = new_text,
    )
    _assert_fields_set(copy)
    vampytest.assert_is_not(poll_question, copy)
    
    vampytest.assert_eq(copy.text, new_text)



def _iter_options__contents():
    text = 'orin'
    
    yield {}, set()
    yield {'text': text}, {text}


@vampytest._(vampytest.call_from(_iter_options__contents()).returning_last())
def test__PollQuestion__contents(keyword_parameters):
    """
    Tests whether ``PollQuestion.contents`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the poll question with.
    
    Returns
    -------
    output : `set<str>`
    """
    poll_question = PollQuestion(**keyword_parameters)
    output = poll_question.contents
    vampytest.assert_instance(output, list)
    return {*output}


def _iter_options__iter_contents():
    text = 'orin'
    
    yield {}, set()
    yield {'text': text}, {text}


@vampytest._(vampytest.call_from(_iter_options__iter_contents()).returning_last())
def test__PollQuestion__iter_contents(keyword_parameters):
    """
    Tests whether ``PollQuestion.iter_contents`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create the poll question with.
    
    Returns
    -------
    output : `set<str>`
    """
    poll_question = PollQuestion(**keyword_parameters)
    return {*poll_question.iter_contents()}
