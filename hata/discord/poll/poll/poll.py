__all__ = ('Poll',)

from scarletio import RichAttributeErrorBaseType

from ...bases import maybe_snowflake
from ...utils import DATETIME_FORMAT_CODE

from ..poll_answer import PollAnswer
from ..poll_result import PollResult
from ..poll_result.utils import poll_result_sort_key

from .constants import DURATION_DEFAULT
from .fields import (
    parse_allow_multiple_choices, parse_answers, parse_duration, parse_expires_at, parse_finalized, parse_layout,
    parse_question, parse_results, put_allow_multiple_choices_into, put_answers_into, put_duration_into,
    put_expires_at_into, put_finalized_into, put_layout_into, put_question_into, put_results_into,
    validate_allow_multiple_choices, validate_answers, validate_duration, validate_expires_at, validate_finalized,
    validate_layout, validate_question, validate_results
)
from .preinstanced import PollLayout


class Poll(RichAttributeErrorBaseType):
    """
    Represents a poll.
    
    Attributes
    ----------
    allow_multiple_choices : `bool`
        The poll's allow_multiple_choices.
    answers : `None`, `tuple` of ``PollAnswer``
        The poll's answers.
    duration : `int`
        After how much time is the poll expiring. Should be multiple of 3600.
    expires_at : `None | DateTime`
        When the poll expires.
    finalized : `bool`
        Whether the poll is manually ended.
    layout : ``PollLayout``
        The poll's layout.
    question : `None`, ``PollQuestion``
        The poll's question.
    results : `None | list<PollResult>`
        The poll's results.
    """
    __slots__ = (
        'allow_multiple_choices', 'answers', 'duration', 'expires_at', 'finalized', 'layout', 'question', 'results'
    )
    
    def __new__(
        cls,
        *,
        allow_multiple_choices = ...,
        answers = ...,
        duration = ...,
        expires_at = ...,
        finalized = ...,
        layout = ...,
        question = ...,
        results = ...,
    ):
        """
        Creates a new poll with the given parameters.
        
        Parameters
        ----------
        allow_multiple_choices : `None`, `bool`, Optional (Keyword only)
            Whether selecting multiple answers is allowed.
        answers :  `None`, `iterable` of ``PollAnswer```, `iterable` of `str`, Optional (Keyword only)
            The poll's answers.
        duration : `int`, Optional (Keyword only)
            After how much time is the poll expiring. Should be multiple of 3600.
        expires_at : `None | DateTime`, Optional (Keyword only)
            When the poll expires.
        finalized : `bool`, Optional (Keyword only)
            Whether the poll is manually ended.
        layout : ``PollLayout``, `int`, Optional (Keyword only)
            The poll's layout.
        question : `None`, ``PollQuestion``, `str`, Optional (Keyword only)
            The poll's question.
        results : `None`, `iterable` of ``PollResult``, Optional (Keyword only)
            The poll's results.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # allow_multiple_choices
        if allow_multiple_choices is ...:
            allow_multiple_choices = False
        else:
            allow_multiple_choices = validate_allow_multiple_choices(allow_multiple_choices)
        
        # answers
        if answers is ...:
            answers = None
        else:
            answers = validate_answers(answers)
        
        # duration
        if duration is ...:
            duration = DURATION_DEFAULT
        else:
            duration = validate_duration(duration)
        
        # expires_at
        if expires_at is ...:
            expires_at = None
        else:
            expires_at = validate_expires_at(expires_at)
        
        # finalized
        if finalized is ...:
            finalized = False
        else:
            finalized = validate_finalized(finalized)
        
        # layout
        if layout is ...:
            layout = PollLayout.default
        else:
            layout = validate_layout(layout)
        
        # question
        if question is ...:
            question = None
        else:
            question = validate_question(question)
        
        # results
        if results is ...:
            results = None
        else:
            results = validate_results(results)
        
        # Construct
        self = object.__new__(cls)
        self.allow_multiple_choices = allow_multiple_choices
        self.answers = answers
        self.duration = duration
        self.expires_at = expires_at
        self.finalized = finalized
        self.layout = layout
        self.question = question
        self.results = results
        
        return self
    
    
    @classmethod
    def _create_empty(cls):
        """
        Creates an empty poll.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.allow_multiple_choices = False
        self.answers = None
        self.duration = DURATION_DEFAULT
        self.expires_at = None
        self.finalized = False
        self.layout = PollLayout.default
        self.question = None
        self.results = None
        return self
    
    
    def __len__(self):
        """Returns the poll's length."""
        length = 0
        
        # allow_multiple_choices
        # does not count
        
        # answers
        for answer in self.iter_answers():
            length += len(answer)
        
        # duration
        # does not count
        
        # expires_at
        # does not count
        
        # finalized
        # does not count
        
        # layout
        # does not count
        
        # question
        question = self.question
        if (question is not None):
            length += len(question)
        
        # results
        # does not count
        
        return length
    
    
    def __bool__(self):
        """Returns whether the poll has any fields set."""
        # allow_multiple_choices
        if self.allow_multiple_choices:
            return True
        
        # answers
        if self.answers is not None:
            return True
        
        # duration
        if self.duration != DURATION_DEFAULT:
            return True
        
        # expires_at
        if self.expires_at is not None:
            return True
        
        # finalized
        if self.finalized:
            return True
        
        # layout
        layout = self.layout
        if layout is not PollLayout.none and layout is not PollLayout.default:
            return True
        
        # question
        if self.question is not None:
            return True
        
        # results
        # does not count
        return False
    
    
    def __repr__(self):
        repr_parts = ['<', type(self).__name__]
        
        field_added = False
        
        # allow_multiple_choices
        allow_multiple_choices = self.allow_multiple_choices
        if allow_multiple_choices:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' allow_multiple_choices = ')
            repr_parts.append(repr(allow_multiple_choices))
        
        # answers
        answers = self.answers
        if (answers is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' answers = ')
            repr_parts.append(repr(answers))
        
        # duration
        duration = self.duration
        if (duration != DURATION_DEFAULT):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' duration = ')
            repr_parts.append(repr(duration))
        
        # expires_at
        expires_at = self.expires_at
        if (expires_at is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' expires_at = ')
            repr_parts.append(format(expires_at, DATETIME_FORMAT_CODE))
        
        # finalized
        finalized = self.finalized
        if finalized:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' finalized = ')
            repr_parts.append(repr(finalized))
        
        # layout
        layout = self.layout
        if layout is not PollLayout.none and layout is not PollLayout.default:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' layout = ')
            repr_parts.append(layout.name)
            repr_parts.append(' ~ ')
            repr_parts.append(repr(layout.value))
        
        # question
        question = self.question
        if (question is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' question = ')
            repr_parts.append(repr(question))
        
        # results
        results = self.results
        if (results is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' results = ')
            repr_parts.append(repr(results))
            
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the poll's hash value."""
        hash_value = 0
        
        # allow_multiple_choice
        hash_value ^= self.allow_multiple_choices << 8
        
        # answers
        answers = self.answers
        if (answers is not None):
            hash_value ^= len(answers)
            
            for answer in answers:
                hash_value ^= hash(answer)
        
        # duration
        duration = self.duration
        if (duration != DURATION_DEFAULT):
            hash_value ^= duration
        
        # expires_at
        expires_at = self.expires_at
        if (expires_at is not None):
            hash_value ^= hash(expires_at)
        
        # finalized
        hash_value ^= self.finalized << 12
        
        # layout
        hash_value ^= hash(self.layout)
        
        # question
        question = self.question
        if (question is not None):
            hash_value ^= hash(question)
        
        # results | order does not matter
        results = self.results
        if (results is not None):
            hash_value ^= len(results) << 4
            
            for result in results:
                hash_value ^= hash(result)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two polls are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # allow_multiple_choices
        if self.allow_multiple_choices != other.allow_multiple_choices:
            return False
        
        # answers
        if self.answers != other.answers:
            return False
        
        # duration
        if self.duration != other.duration:
            return False
        
        # expires_at
        if self.expires_at != other.expires_at:
            return False
        
        # finalized
        if self.finalized != other.finalized:
            return False
        
        # layout
        if self.layout is not other.layout:
            return False
        
        # question
        if self.question != other.question:
            return False
        
        # results | order matters
        self_results = self.results
        if (self_results is not None):
            self_results.sort(key = poll_result_sort_key)
        
        other_results = other.results
        if (other_results is not None):
            other_results.sort(key = poll_result_sort_key)
        
        if self_results != other_results:
            return False
        
        return True
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new poll instance from the given json data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Data to create poll from.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.allow_multiple_choices = parse_allow_multiple_choices(data)
        self.answers = parse_answers(data)
        self.duration = parse_duration(data)
        self.expires_at = parse_expires_at(data)
        self.finalized = parse_finalized(data)
        self.layout = parse_layout(data)
        self.question = parse_question(data)
        self.results = parse_results(data)
        return self
    
    
    def _update_attributes(self, data):
        """
        Updates the poll's attributes with the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Data to update the poll with.
        """
        self.allow_multiple_choices = parse_allow_multiple_choices(data)
        self.answers = parse_answers(data)
        self.duration = parse_duration(data)
        self.expires_at = parse_expires_at(data)
        self.finalized = parse_finalized(data)
        self.layout = parse_layout(data)
        self.question = parse_question(data)
        self.results = parse_results(data, self.results)
    
    
    def _difference_update_attributes(self, data):
        """
        Updates the poll's attributes with the given data  and returns the changes in a
        `dict` of (`attribute-name`, `old-value`) items.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Data to update the poll with.
            
        Returns
        -------
        old_attributes : `dict` of (`str`, `object`) items
            All item in the returned dict is optional.
        
        Returned Data Structure
        -----------------------
        
        +---------------------------+-----------------------------------+
        | Keys                      | Values                            |
        +===========================+===================================+
        | allow_multiple_choices    | `bool`                            |
        +---------------------------+-----------------------------------+
        | answers                   | `None`, `tuple` of ``PollAnswer`` |
        +---------------------------+-----------------------------------+
        | duration                  | `int`                             |
        +---------------------------+-----------------------------------+
        | expires_at                | `None`, `DateTime`                |
        +---------------------------+-----------------------------------+
        | finalized                 | `bool`                            |
        +---------------------------+-----------------------------------+
        | layout                    | ``PollLayout``                    |
        +---------------------------+-----------------------------------+
        | question                  | `None`, ``PollQuestion``          |
        +---------------------------+-----------------------------------+
        """
        old_attributes = {}
        
        # allow_multiple_choices
        allow_multiple_choices = parse_allow_multiple_choices(data)
        if (allow_multiple_choices != self.allow_multiple_choices):
            old_attributes['allow_multiple_choices'] = self.allow_multiple_choices
            self.allow_multiple_choices = allow_multiple_choices
        
        # answers
        answers = parse_answers(data)
        if (answers != self.answers):
            old_attributes['answers'] = self.answers
            self.answers = answers
        
        # duration
        duration = parse_duration(data)
        if (duration != self.duration):
            old_attributes['duration'] = self.duration
            self.duration = duration
        
        # expires_at
        expires_at = parse_expires_at(data)
        if (expires_at != self.expires_at):
            old_attributes['expires_at'] = self.expires_at
            self.expires_at = expires_at
        
        # finalized
        finalized = parse_finalized(data)
        if (finalized != self.finalized):
            old_attributes['finalized'] = self.finalized
            self.finalized = finalized
        
        # layout
        layout = parse_layout(data)
        if (layout is not self.layout):
            old_attributes['layout'] = self.layout
            self.layout = layout
        
        # question
        question = parse_question(data)
        if (question != self.question):
            old_attributes['question'] = self.question
            self.question = question
        
        # results
        self.results = parse_results(data, self.results)
        
        return old_attributes
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Returns the poll as a json serializable representation.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with their default values should be included as well.
        
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether internal fields should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        
        put_allow_multiple_choices_into(self.allow_multiple_choices, data, defaults)
        put_answers_into(self.answers, data, defaults, include_internals = include_internals)
        put_layout_into(self.layout, data, defaults)
        put_question_into(self.question, data, defaults)
        
        if include_internals:
            put_expires_at_into(self.expires_at, data, defaults)
            put_finalized_into(self.finalized, data, defaults)
            put_results_into(self.results, data, defaults)
        else:
            put_duration_into(self.duration, data, defaults)
        
        return data
    
    
    def clean_copy(self, guild = None):
        """
        Creates a clean copy of the poll by removing the mentions in it's contents.
        
        Parameters
        ----------
        guild : `None`, ``Guild`` = `None`, Optional
            The respective guild as a context to look up guild specific names of entities.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.allow_multiple_choices = self.allow_multiple_choices
        
        answers = self.answers
        if (answers is not None):
            answers = (*(answer.clean_copy(guild) for answer in answers),)
        new.answers = answers
        
        new.duration = self.duration
        new.expires_at = self.expires_at
        new.finalized = self.finalized
        new.layout = self.layout
        
        question = self.question
        if (question is not None):
            question = question.clean_copy(guild)
        new.question = question
        
        results = self.results
        if (results is not None):
            results = [result.copy() for result in results]
        new.results = results
        
        return new
    
    
    def copy(self):
        """
        Copies the poll.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new.allow_multiple_choices = self.allow_multiple_choices
        
        answers = self.answers
        if (answers is not None):
            answers = (*(answer.copy() for answer in answers),)
        new.answers = answers
        
        new.duration = self.duration
        new.expires_at = self.expires_at
        new.finalized = self.finalized
        new.layout = self.layout
        
        question = self.question
        if (question is not None):
            question = question.copy()
        new.question = question
        
        results = self.results
        if (results is not None):
            results = [result.copy() for result in results]
        new.results = results
        
        return new
    
    
    def copy_with(
        self,
        *,
        allow_multiple_choices = ...,
        answers = ...,
        duration = ...,
        expires_at = ...,
        finalized = ...,
        layout = ...,
        question = ...,
        results = ...,
    ):
        """
        Copies the poll with the given parameters.
        
        Parameters
        ----------
        allow_multiple_choices : `bool`, Optional (Keyword only)
            Whether selecting multiple answers is allowed.
        answers :  `None`, `iterable` of ``PollAnswer```, `iterable` of `str`, Optional (Keyword only)
            The poll's answers.
        duration : `int`, Optional (Keyword only)
            After how much time is the poll expiring. Should be multiple of 3600.
        expires_at : `None | DateTime`, Optional (Keyword only)
            When the poll expires.
        finalized : `bool`, Optional (Keyword only)
            Whether the poll is manually ended.
        layout : ``PollLayout``, `int`, Optional (Keyword only)
            The poll's layout.
        question : `None`, ``PollQuestion``, `str`, Optional (Keyword only)
            The poll's question.
        results : `None`, `iterable` of ``PollResult``, Optional (Keyword only)
            The poll's results.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # allow_multiple_choices
        if allow_multiple_choices is ...:
            allow_multiple_choices = self.allow_multiple_choices
        else:
            allow_multiple_choices = validate_allow_multiple_choices(allow_multiple_choices)
        
        # answers
        if answers is ...:
            answers = self.answers
            if (answers is not None):
                answers = (*(answer.copy() for answer in answers),)
        else:
            answers = validate_answers(answers)
        
        # duration
        if duration is ...:
            duration = self.duration
        else:
            duration = validate_duration(duration)
        
        # expires_at
        if expires_at is ...:
            expires_at = self.expires_at
        else:
            expires_at = validate_expires_at(expires_at)
        
        # finalized
        if finalized is ...:
            finalized = self.finalized
        else:
            finalized = validate_finalized(finalized)
        
        # layout
        if layout is ...:
            layout = self.layout
        else:
            layout = validate_layout(layout)
        
        # question
        if question is ...:
            question = self.question
            if (question is not None):
                question = question.copy()
        else:
            question = validate_question(question)
        
        # results
        if results is ...:
            results = self.results
            if (results is not None):
                results = [result.copy() for result in results]
        else:
            results = validate_results(results)
        
        # Construct
        new = object.__new__(type(self))
        new.allow_multiple_choices = allow_multiple_choices
        new.answers = answers
        new.duration = duration
        new.expires_at = expires_at
        new.finalized = finalized
        new.layout = layout
        new.question = question
        new.results = results
        return new
    
    
    @property
    def contents(self):
        """
        Returns the contents of the poll.
        
        Returns
        -------
        contents : `list<str>`
        """
        return [*self.iter_contents()]
    
    
    def iter_contents(self):
        """
        Iterates over the contents of the poll.
        
        This method is an iterable generator.
        
        Yields
        ------
        content : `str`
        """
        question = self.question
        if (question is not None):
            yield from question.iter_contents()
        
        for answer in self.iter_answers():
            yield from answer.iter_contents()
    
    
    def iter_answers(self):
        """
        Iterates over the answers of the poll.
        
        This method is an iterable generator.
        
        Yields
        ------
        answer : ``PollAnswer``
        """
        answers = self.answers
        if (answers is not None):
            yield from answers
    
    
    def iter_results(self):
        """
        Iterates over the results of the poll.
        
        This method is an iterable generator.
        
        Yields
        ------
        result : ``PollResult``
        """
        # Order does not matter.
        results = self.results
        if (results is not None):
            yield from self.results
    
    
    def get_answer_id(self, poll_answer):
        """
        Gets the poll answer's identifier for an answer like the given one.
        
        Parameters
        ----------
        poll_answer : ``PollAnswer``
            The poll answer to gets identifier of.
        
        Returns
        -------
        answer_id : `int`
            Returns `0` on failure.
        """
        answer_emoji = poll_answer.emoji
        answer_text = poll_answer.text
        for answer in self.iter_answers():
            if (answer_emoji is answer.emoji) and (answer_text == answer.text):
                return answer.id
        
        return 0
    
    
    def __getitem__(self, key):
        """
        Gets the result for the given answer.
        
        Parameters
        ----------
        key : ``PollAnswer``
            
        Returns
        -------
        result : `None | PollAnswer`
        
        Raises
        ------
        TypeError
        """
        if isinstance(key, PollAnswer):
            answer_id = key.id
            if not answer_id:
                answer_id = self.get_answer_id(key)
                if not answer_id:
                    return None
        
        else:
            answer_id = maybe_snowflake(key)
            if answer_id is None:
                raise TypeError(
                    f'`key` can be `int`, `{PollAnswer.__name__}`, got {type(key).__name__}; {key!r}.'
                )
        
        for result in self.iter_results():
            if result.answer_id == answer_id:
                return result
        
        return None
    
    
    def _get_or_create_result(self, answer_id):
        """
        Gets result for the given `answer_id`. If not found creates a new one.
        
        Parameters
        ----------
        answer_id : `int`
            The answer's identifier.
        
        Returns
        -------
        result : ``PollResult``
        """
        results = self.results
        if results is None:
            result = PollResult._create_empty(answer_id)
            self.results = [result]
        else:
            for result in results:
                if answer_id == result.answer_id:
                    break
            
            else:
                result = PollResult._create_empty(answer_id)
                results.append(result)
        
        return result
    
    
    def _add_vote(self, answer_id, user):
        """
        Adds a vote on the poll.
        
        Parameters
        ----------
        answer_id : `int`
            The answer's identifier.
        user : ``ClientUserBase``
            The user who voted.
        
        Returns
        -------
        success : `bool`
        """
        result = self._get_or_create_result(answer_id)
        return result._add_vote(user)
    
    
    def _fill_some_votes(self, answer_id, users):
        """
        Fills out some voter users for the given `answer_id` on the poll.
        
        Parameters
        ----------
        answer_id : `int`
            The answer's identifier.
        users : `list` of ``ClientUserBase``
            The users who voted.
        """
        result = self._get_or_create_result(answer_id)
        result._fill_some_votes(users)
    
    
    def _fill_all_votes(self, answer_id, users):
        """
        Fills out all voter users for the given `answer_id` on the poll.
        
        Parameters
        ----------
        answer_id : `int`
            The answer's identifier.
        users : `list` of ``ClientUserBase``
            The users who voted.
        """
        result = self._get_or_create_result(answer_id)
        result._fill_all_votes(users)
    
    
    def _remove_vote(self, answer_id, user):
        """
        Removes a vote from the poll.
        
        Parameters
        ----------
        answer_id : `int`
            The answer's identifier.
        user : ``ClientUserBase``
            The user who removed their vote.
        
        Returns
        -------
        success : `bool`
        """
        results = self.results
        if results is None:
            return False
        
        for result in results:
            if answer_id == result.answer_id:
                break
        
        else:
            return False
        
        return result._remove_vote(user)
    
    
    def iter_items(self):
        """
        Iterates over `answer - result` pairs. If an answer does not have a result yet, creates it.
        
        This method is an iterable generator.
        
        Yields
        ------
        item : `(PollAnswer, PollResult)`
        """
        for answer in self.iter_answers():
            yield answer, self._get_or_create_result(answer.id)
