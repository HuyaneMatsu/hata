__all__ = ()

from ..activity import Activity, ActivityType
from ..application import Application
from ..events import IntentFlag
from ..field_validators import bool_validator_factory, entity_id_validator_factory, flag_validator_factory
from ..user import ClientUserBase

# activity

def validate_activity(activity):
    """
    Validates the given client activity.
    
    Parameters
    ----------
    activity : ``Activity``
        Client activity.
    
    Returns
    -------
    activity : ``Activity``
    
    Raises
    ------
    TypeError
        - If `activity`'s type is incorrect.
    ValueError
        - if `activity` is a custom activity.
    """
    if not isinstance(activity, Activity):
        raise TypeError(
            f'`activity` can be `{Activity.__name__}`, got {activity.__class__.__name__}; {activity!r}.'
        )
    
    if (activity.type is ActivityType.custom):
        raise ValueError(
            f'`activity` cannot be {ActivityType.custom.name}, got {activity!r}.'
        )
    
    return activity

# additional owners

def validate_additional_owner_ids(additional_owner_ids):
    """
    Validates the given client additional owners.
    
    Parameters
    ----------
    additional_owner_ids : `None`, `int`, ``ClientUserBase``, `iterable` of (`int`, ``ClientUserBase``)
        Additional users to return `True` for by ``Client.is_owner`.
    
    Returns
    -------
    additional_owner_ids : `None`, `set` of `int`.
    
    Raises
    ------
    TypeError
        - If `additional_owner_ids`'s type is incorrect.
    """
    if additional_owner_ids is None:
        return None
    
    if isinstance(additional_owner_ids, ClientUserBase):
        return {additional_owner_ids.id}
    
    if type(additional_owner_ids) is int:
        return {additional_owner_ids}
    
    if isinstance(additional_owner_ids, int):
        return {int(additional_owner_ids)}
    
    if (getattr(additional_owner_ids, '__iter__', None) is None):
        raise TypeError(
            f'`additional_owner_ids` can be `None`, `int`, `{ClientUserBase.__name__}`, `iterable` of'
            f'(`int`, `{ClientUserBase.__name__}`), got {additional_owner_ids.__class__.__name__}; '
            f'{additional_owner_ids!r}.'
        )
    
    additional_owner_ids_validated = None
    
    for additional_owner in additional_owner_ids:
        if type(additional_owner) is int:
            user_id = additional_owner
        
        elif isinstance(additional_owner, int):
            user_id = int(additional_owner)
            
        elif isinstance(additional_owner, ClientUserBase):
            user_id = additional_owner.id
            
        else:
            raise TypeError(
                f'`additional_owner_ids` can contain `int`, `{ClientUserBase.__name__}` elements, got '
                f'{additional_owner.__class__.__name__}; {additional_owner!r}; '
                f'additional_owner_ids = {additional_owner!r}.'
            )
        
        if additional_owner_ids_validated is None:
            additional_owner_ids_validated = set()
            
        additional_owner_ids_validated.add(user_id)
    
    return additional_owner_ids_validated

# application_id

validate_application_id = entity_id_validator_factory('application_id', Application)

# client_id

validate_client_id = entity_id_validator_factory('client_id')

# extensions

def validate_extensions(extensions):
    """
    Validates the given http client debug options.
    
    Parameters
    ----------
    extensions : `None`, `str`, `iterable` of `str`
        Http client debug options.
    
    Returns
    -------
    extensions : `None`, `set` of `str`
    
    Raises
    ------
    TypeError
        - If `extensions`'s type is incorrect.
    """
    if extensions is None:
        return None

    if isinstance(extensions, str):
        if type(extensions) is not str:
            extensions = str(extensions)
        
        return {extensions}
    
    if (getattr(extensions, '__iter__', None) is None):
        raise TypeError(
            f'`extensions` can be `None`, `str`, `iterable` of `str`, got '
            f'{extensions.__class__.__name__}; {extensions!r}.'
        )
    
    extensions_validated = None
    
    for extension in extensions:
        
        if type(extension) is str:
            pass
        elif isinstance(extension, str):
            extension = str(extension)
        else:
            raise TypeError(
                f'{extensions} contains a non `str`, got '
                f'{extensions.__class__.__name__}; {extensions!r}.'
            )
        
        if extensions_validated is None:
            extensions_validated = set()
        
        extensions_validated.add(extension)
    
    return extensions_validated

# http_debug_options

def validate_http_debug_options(http_debug_options):
    """
    Validates the given http client debug options.
    
    Parameters
    ----------
    http_debug_options : `None`, `str`, `iterable` of `str`
        Http client debug options.
    
    Returns
    -------
    http_debug_options : `None`, `set` of `str`
    
    Raises
    ------
    TypeError
        - If `http_debug_options`'s type is incorrect.
    """
    if http_debug_options is None:
        return None

    if isinstance(http_debug_options, str):
        if type(http_debug_options) is not str:
            http_debug_options = str(http_debug_options)
        
        if not http_debug_options.islower():
            http_debug_options = http_debug_options.lower()
        
        return {http_debug_options}
    
    if (getattr(http_debug_options, '__iter__', None) is None):
        raise TypeError(
            f'`http_debug_options` can be `None`, `str`, `iterable` of `str`, got '
            f'{http_debug_options.__class__.__name__}; {http_debug_options!r}.'
        )
    
    http_debug_options_validated = None
    
    for http_debug_option in http_debug_options:
        
        if type(http_debug_option) is str:
            pass
        elif isinstance(http_debug_option, str):
            http_debug_option = str(http_debug_option)
        else:
            raise TypeError(
                f'{http_debug_options} contains a non `str`, got '
                f'{http_debug_options.__class__.__name__}; {http_debug_options!r}.'
            )
        
        if not http_debug_option.islower():
            http_debug_option = http_debug_option.lower()
        
        if http_debug_options_validated is None:
            http_debug_options_validated = set()
        
        http_debug_options_validated.add(http_debug_option)
    
    return http_debug_options_validated

# intents

validate_intents = flag_validator_factory('intents', IntentFlag)

# secret

def validate_secret(secret):
    """
    Validates the given client secret.
    
    Parameters
    ----------
    secret : `str`
        Client secret.
    
    Returns
    -------
    secret : `str`
    
    Raises
    ------
    TypeError
        - If `secret`'s type is incorrect.
    """
    if type(secret) is str:
        pass
    elif isinstance(secret, str):
        secret = str(secret)
    else:
        raise TypeError(
            f'`secret` can be `str`, got `{secret.__class__.__name__}`; {secret!r}.'
        )
    
    return secret

# should_request_users

validate_should_request_users = bool_validator_factory('should_request_users', True)

# shard_count

def validate_shard_count(shard_count):
    """
    Validates the client's shard count.
    
    Parameters
    ----------
    shard_count : `int`
       The client's shard count.
    
    Returns
    -------
    shard_count : `int`
    
    Raises
    ------
    TypeError
        - If `shard_count`'s type is incorrect.
    """
    if (type(shard_count) is int):
        pass
    elif isinstance(shard_count, int):
        shard_count = int(shard_count)
    else:
        raise TypeError(
            f'`shard_count` can be `int`, got {shard_count.__class__.__name__}; {shard_count!r}.'
        )
    
    if shard_count < 0:
        shard_count = 0
    
    # Default shard count to `0` if we received `1`.
    elif shard_count == 1:
        shard_count = 0
    
    return shard_count

# token

def validate_token(token):
    """
    Validates the given client token.
    
    Parameters
    ----------
    token : `str`
        Client token.
    
    Returns
    -------
    token : `str`
    
    Raises
    ------
    TypeError
        - If `token`'s type is incorrect.
    """
    if (type(token) is str):
        pass
    elif isinstance(token, str):
        token = str(token)
    else:
        raise TypeError(
            f'`token` can be `str`, got {token.__class__.__name__}; {token!r}.'
        )
    
    return token
