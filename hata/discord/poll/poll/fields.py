__all__ = ()

from ...field_parsers import (
    bool_parser_factory, int_postprocess_parser_factory, nullable_date_time_parser_factory,
    nullable_entity_parser_factory, preinstanced_parser_factory
)
from ...field_putters import (
    bool_optional_putter_factory, int_optional_postprocess_putter_factory, nullable_date_time_optional_putter_factory,
    nullable_entity_array_putter_factory, nullable_entity_putter_factory, preinstanced_optional_putter_factory
)
from ...field_validators import (
    bool_validator_factory, int_conditional_validator_factory, nullable_date_time_validator_factory,
    preinstanced_validator_factory
)

from ..poll_answer import PollAnswer
from ..poll_question import PollQuestion
from ..poll_result import PollResult
from ..poll_result.utils import merge_update_poll_results

from .constants import DURATION_DEFAULT, DURATION_MAX
from .preinstanced import PollLayout


# allow_multiple_choices

parse_allow_multiple_choices = bool_parser_factory('allow_multiselect', False)
put_allow_multiple_choices_into = bool_optional_putter_factory('allow_multiselect', False)
validate_allow_multiple_choices = bool_validator_factory('allow_multiple_choices', False)


# answers

def parse_answers(data):
    """
    Parses answers from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    answers : `None | tuple<PollAnswer>`
    """
    answer_datas = data.get('answers', None)
    if (answer_datas is None) or (not answer_datas):
        return None
    
    return (*(PollAnswer.from_data(answer_data) for answer_data in answer_datas),)    


put_answers_into = nullable_entity_array_putter_factory('answers', PollAnswer)


def validate_answers(answers):
    """
    Validates the given answers.
    
    Parameters
    ----------
    answers : `None | iterable<PollAnswer | str>`
        The answers to validate.
    
    Returns
    -------
    answers : `None | tuple<PollAnswer>`
    """
    if answers is None:
        return None
    
    if (getattr(answers, '__iter__', None) is None):
        raise TypeError(
            f'`answers` can be `None`, `iterable` of `{PollAnswer.__name__}`, `str`, got '
            f'{type(answers).__name__}; {answers!r}.'
        )
        
    answers_validated = None
    
    for answer in answers:
        if isinstance(answer, PollAnswer):
            pass
        
        elif isinstance(answer, str):
            answer = PollAnswer(text = answer)
        
        else:
            raise TypeError(
                f'`answers` can contain `{PollAnswer.__name__}`, `str` elements, got '
                f'{type(answer).__name__}; {answer!r}; answers = {answers!r}.'
            )
        
        if (answers_validated is None):
            answers_validated = []
        
        answers_validated.append(answer)
    
    if (answers_validated is not None):
        return tuple(answers_validated)

# duration

parse_duration = int_postprocess_parser_factory(
    'duration',
    DURATION_DEFAULT,
    (lambda duration: duration * 3600),
)
put_duration_into = int_optional_postprocess_putter_factory(
    'duration',
    DURATION_DEFAULT,
    (lambda duration: duration // 3600),
)
validate_duration = int_conditional_validator_factory(
    'duration',
    DURATION_DEFAULT,
    (lambda duration: duration > 0 and duration <= DURATION_MAX and duration % 3600 == 0),
    f'must be > 0 and <= and {DURATION_MAX} multiple of 3600'
)


# expires_at

parse_expires_at = nullable_date_time_parser_factory('expiry')
put_expires_at_into = nullable_date_time_optional_putter_factory('expiry')
validate_expires_at = nullable_date_time_validator_factory('expires_at')

# finalized


def parse_finalized(data):
    """
    Parses out the finalized value from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    finalized : `bool`
    """
    nested_data = data.get('results', None)
    if nested_data is None:
        return False
    
    finalized = nested_data.get('is_finalized', None)
    if finalized is None:
        return False
    
    return finalized


def put_finalized_into(finalized, data, defaults):
    """
    Serializes the finalized value into the given `data`.
    
    Parameters
    ----------
    finalized : `bool`
        Value to serialize.
    data : `dict<str, object>`
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    nested_data = data.get('results', None)
    if nested_data is None:
        nested_data = {}
        data['results'] = nested_data
    
    nested_data['is_finalized'] = finalized
    
    return data


validate_finalized = bool_validator_factory('finalized', False)

# layout

parse_layout = preinstanced_parser_factory('layout_type', PollLayout, PollLayout.default)
put_layout_into = preinstanced_optional_putter_factory('layout_type', PollLayout.default)
validate_layout = preinstanced_validator_factory('layout', PollLayout)


# question

parse_question = nullable_entity_parser_factory('question', PollQuestion)
put_question_into = nullable_entity_putter_factory('question', PollQuestion)


def validate_question(question):
    """
    Validates whether the given `question` is valid.
    
    Parameters
    ----------
    question : `None`, ``PollQuestion``, `str`
        The question to validate.
    
    Returns
    -------
    question : `None`, ``PollQuestion``
        The validated question.
    
    Raises
    ------
    TypeError
    ValueError
    """
    if question is None:
        return None
    
    if isinstance(question, PollQuestion):
        return question
    
    if isinstance(question, str):
        return PollQuestion(text = question)
    
    raise TypeError(
        f'`question` can be `None`, `{PollQuestion.__name__}`, `str`, got {type(question).__name__!s}; {question!r}.'
    )


# results

def parse_results(data, old_results = None):
    """
    Parses the poll results from the given data.
    
    Parameters
    ----------
    data : `dict<str, object>`
        Data to parse from.
    old_results : `None | list<PollResult>` = `None`, Optional
        Old results of the poll.
    
    Returns
    -------
    results : `None | list<PollResult>`
    """
    nested_data = data.get('results', None)
    if nested_data is None:
        return None
    
    result_datas = nested_data.get('answer_counts', None)
    if (result_datas is None) or (not result_datas):
        new_results = None
    else:
        new_results = [PollResult.from_data(result_data) for result_data in result_datas]
    return merge_update_poll_results(new_results, old_results)


def put_results_into(results, data, defaults):
    """
    Serializes poll results into the given `data`.
    
    Parameters
    ----------
    results : `None | list<PollResult>`
        Results to serialize.
    data : `dict<str, object>`
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    if results is None:
        result_datas = []
    else:
        result_datas = [result.to_data(defaults = defaults) for result in results]
    
    nested_data = data.get('results', None)
    if nested_data is None:
        nested_data = {}
        data['results'] = nested_data
    
    nested_data['answer_counts'] = result_datas
    
    return data


def validate_results(results):
    """
    Validates the given results.
    
    Parameters
    ----------
    results : `None | iterable<PollResult>`
        The results to validate.
    
    Returns
    -------
    results : `None | list<PollResult>`
    """
    if results is None:
        return None
    
    if (getattr(results, '__iter__', None) is None):
        raise TypeError(
            f'`results` can be `None`, `iterable` of `{PollResult.__name__}`, got '
            f'{type(results).__name__}; {results!r}.'
        )
        
    results_validated = None
    
    for result in results:
        if not isinstance(result, PollResult):
            raise TypeError(
                f'`results` can contain `{PollResult.__name__}` elements, got '
                f'{type(result).__name__}; {result!r}; results = {results!r}.'
            )
        
        if (results_validated is None):
            results_validated = []
        
        results_validated.append(result)
    
    return results_validated
