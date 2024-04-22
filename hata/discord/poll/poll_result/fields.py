__all__ = ()

from ...field_parsers import entity_id_parser_factory, int_parser_factory
from ...field_putters import entity_id_putter_factory, int_putter_factory
from ...field_validators import entity_id_validator_factory, int_conditional_validator_factory
from ...user import ClientUserBase


# answer_id

parse_answer_id = entity_id_parser_factory('id')
put_answer_id_into = entity_id_putter_factory('id')
validate_answer_id = entity_id_validator_factory('answer_id')


# count

parse_count = int_parser_factory('count', 0)
put_count_into = int_putter_factory('count')
validate_count = int_conditional_validator_factory(
    'count',
    0,
    (lambda count : count >= 0),
    '>= 0',
)


# users

def validate_users(users):
    """
    Validates the input users of a poll result.
    
    Parameters
    ----------
    users : `None`, `iterable` of ``ClientUserBase``
        The users to validate.
    
    Returns
    -------
    users : `None | set<ClientUserBase>`
    
    Raises
    ------
    TypeError
        - `users`'s type is invalid.
    """
    if users is None:
        return None
    
    if (getattr(users, '__iter__', None) is None):
        raise TypeError(
            f'`users` can be either `None`  or `iterable` of `{ClientUserBase.__name__}` elements, got {users!r}.'
        )
    
    validated_users = None
    
    
    for user in users:
        if not isinstance(user, ClientUserBase):
            raise TypeError(
                f'`users` can have `{ClientUserBase.__name__}` elements, got '
                f'{type(user).__name__}; {user!r}; users = {users!r}.'
            )
        
        if validated_users is None:
            validated_users = set()
        
        validated_users.add(user)
        continue
        
    
    return validated_users
