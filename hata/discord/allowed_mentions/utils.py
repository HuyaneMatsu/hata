__all__ = ('is_allowed_mentions_valid', 'parse_allowed_mentions')

from scarletio import include

from ..role import Role
from ..user import UserBase

from .constants import STATE_ALLOW_REPLIED_USER_FALSE, STATE_ALLOW_REPLIED_USER_NONE, STATE_ALLOW_REPLIED_USER_TRUE


AllowedMentionProxy = include('AllowedMentionProxy')


def is_allowed_mentions_element_valid(element):
    """
    Returns whether the given allowed mentions element is valid.
    
    Parameters
    ----------
    element : `object`
        The element to check.
    
    Returns
    -------
    is_valid : `bool`
    """
    if isinstance(element, str):
        return element in {'everyone', 'users', 'roles', 'replied_user', '!replied_user'}
    
    if isinstance(element, UserBase):
        return True
    
    if isinstance(element, Role):
        return True
    
    return False


def is_allowed_mentions_valid(allowed_mentions):
    """
    Returns whether the given value is valid as an `allowed_mentions` parameter.
    
    Parameters
    ----------
    allowed_mentions : `None`,  `str`, ``UserBase``, ``Role``, ``AllowedMentionProxy``, (`list`, `tuple`, `set`) of \
            (`str`, ``UserBase``, ``Role`` )
        Which user or role can the message ping (or everyone).
    
    Returns
    -------
    is_valid : `bool`
    """
    if allowed_mentions is None:
        return True
    
    if isinstance(allowed_mentions, AllowedMentionProxy):
        return True
    
    if isinstance(allowed_mentions, (list, set, tuple)):
        return all(is_allowed_mentions_element_valid(element) for element in allowed_mentions)
    
    return False


def parse_allowed_mentions(allowed_mentions):
    """
    If `allowed_mentions` is passed as `None`, then returns a `dict`, what will cause all mentions to be disabled.
    
    If passed as an `iterable`, then it's elements will be checked. They can be either type `str`
    (any value from `('everyone', 'users', 'roles')`), ``UserBase``, ``Role``-s.
    
    Passing `everyone` will allow the message to mention `@everyone` (permissions can overwrite this behaviour).
    
    Passing `'users'` will allow the message to mention all the users, meanwhile passing ``UserBase``-s.
    allow to mentioned the respective users. Using `users` and ``UserBase``-s. is mutually exclusive,
    and the wrapper will register only `users` to avoid getting ``DiscordException``.
    
    `'roles'` and ``Role``-s. follow the same rules as `'users'` and the ``UserBase``-s.
    
    By passing `'!replied_user'` you can disable mentioning the replied user, or by passing`'replied_user'` you can
    re-enable mentioning the replied user.
    
    Parameters
    ----------
    allowed_mentions : `None`,  `str`, ``UserBase``, ``Role``, ``AllowedMentionProxy``, (`list`, `tuple`, `set`) of \
            (`str`, ``UserBase``, ``Role`` )
        Which user or role can the message ping (or everyone).
    
    Returns
    -------
    allowed_mentions : `dict` of (`str`, `object`) items
    
    Raises
    ------
    TypeError
        If `allowed_mentions` contains an element of invalid type.
    ValueError
        If `allowed_mentions` contains en element of correct type, but an invalid value.
    """
    if (allowed_mentions is None):
        return {'parse': []}
    
    if isinstance(allowed_mentions, AllowedMentionProxy):
        return allowed_mentions.to_data()
    
    if isinstance(allowed_mentions, list):
        if (not allowed_mentions):
            return {'parse': []}
    
    elif isinstance(allowed_mentions, (set, tuple)):
        if (not allowed_mentions):
            return {'parse': []}
        
        allowed_mentions = [*allowed_mentions]
    
    else:
        allowed_mentions = [allowed_mentions]
    
    allow_replied_user = STATE_ALLOW_REPLIED_USER_NONE
    allow_everyone = 0
    allow_users = 0
    allow_roles = 0
    
    allowed_users = None
    allowed_roles = None
    
    for element in allowed_mentions:
        if isinstance(element, str):
            if element == '!replied_user':
                allow_replied_user = STATE_ALLOW_REPLIED_USER_FALSE
                continue
            
            if element == 'replied_user':
                allow_replied_user = STATE_ALLOW_REPLIED_USER_TRUE
                continue
            
            if element == 'everyone':
                allow_everyone = 1
                continue
            
            if element == 'users':
                allow_users = 1
                continue
            
            if element == 'roles':
                allow_roles = 1
                continue
            
            raise ValueError(
                f'`allowed_mentions` contains a not valid `str` element: `{element!r}`. `str` '
                f'elements can be any of: (\'everyone\', \'users\', \'roles\', \'replied_user\', '
                f'\'!replied_user\').'
            )
        
        if isinstance(element, UserBase):
            if allowed_users is None:
                allowed_users = []
            
            allowed_users.append(str(element.id))
            continue
        
        if isinstance(element, Role):
            if allowed_roles is None:
                allowed_roles = []
            
            allowed_roles.append(str(element.id))
            continue
        
        raise TypeError(
            f'`allowed_mentions` can contain `str`, `{Role.__name__}`, `{UserBase.__name__}` elements, got '
            f' {type(element).__name__}; {element!r}; allowed_mentions = {allowed_mentions!r}.'
        )
    
    
    result = {}
    parse_all_of = None
    
    if allow_replied_user != STATE_ALLOW_REPLIED_USER_NONE:
        result['replied_user'] = (allow_replied_user == STATE_ALLOW_REPLIED_USER_TRUE)
    
    if allow_everyone:
        if parse_all_of is None:
            parse_all_of = []
            result['parse'] = parse_all_of
        
        parse_all_of.append('everyone')
    
    if allow_users:
        if parse_all_of is None:
            parse_all_of = []
            result['parse'] = parse_all_of
        
        parse_all_of.append('users')
    else:
        if (allowed_users is not None):
            result['users'] = allowed_users
    
    if allow_roles:
        if parse_all_of is None:
            parse_all_of = []
            result['parse'] = parse_all_of
        
        parse_all_of.append('roles')
    else:
        if (allowed_roles is not None):
            result['roles'] = allowed_roles
    
    return result
