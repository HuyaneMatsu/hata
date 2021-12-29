__all__ = ('get_client_application_id', 'get_client_id', 'get_client_secret', 'get_client_token')

from ...env import get_str_env, get_int_env
from scarletio import RichAnalyzer
from ...discord.client import Client

CLIENT_ANALYZER_PARAMETERS = RichAnalyzer(Client.__new__).parameters

CLIENT_DEFAULT_PARAMETER_ID = CLIENT_ANALYZER_PARAMETERS.client_id
CLIENT_DEFAULT_PARAMETER_SECRET = CLIENT_ANALYZER_PARAMETERS.secret
CLIENT_DEFAULT_PARAMETER_APPLICATION_ID = CLIENT_ANALYZER_PARAMETERS.application_id

del CLIENT_ANALYZER_PARAMETERS


def get_client_token(environmental_variable_prefix):
    """
    Tries to get client token from environmental variables.
    
    Parameters
    ----------
    environmental_variable_prefix : `str`
        Environmental parameter prefix.
    
    Returns
    -------
    client_token : `str`
    
    Raises
    ------
    RuntimeError
        If token environmental variable could not be detected.
    """
    environmental_variable_name = environmental_variable_prefix+'_TOKEN'
    client_token = get_str_env(environmental_variable_name, warn_if_empty=False)
    if client_token is None:
        raise RuntimeError(
            f'Required `token` environmental variable with name: {environmental_variable_name!r} could not be '
            f'detected.'
        )
    
    return client_token


def get_client_id(environmental_variable_prefix):
    """
    Tries to get the client's identifier from environmental variables.
    
    Parameters
    ----------
    environmental_variable_prefix : `str`
        Environmental parameter prefix.
    
    Returns
    -------
    client_id : `int`
    """
    environmental_variable_name = environmental_variable_prefix+'_ID'
    return get_int_env(environmental_variable_name, CLIENT_DEFAULT_PARAMETER_ID, warn_if_empty=False)



def get_client_secret(environmental_variable_prefix):
    """
    Tries to get the client's secret from environmental variables.
    
    Parameters
    ----------
    environmental_variable_prefix : `str`
        Environmental parameter prefix.
    
    Returns
    -------
    client_secret : `int`
    """
    environmental_variable_name = environmental_variable_prefix+'_SECRET'
    return get_str_env(environmental_variable_name, CLIENT_DEFAULT_PARAMETER_SECRET)


def get_client_application_id(environmental_variable_prefix):
    """
    Tries to get the client's application's identifier from environmental variables.
    
    Parameters
    ----------
    environmental_variable_prefix : `str`
        Environmental parameter prefix.
    
    Returns
    -------
    application_id : `int`
    """
    environmental_variable_name = environmental_variable_prefix+'_APPLICATION_ID'
    return get_int_env(environmental_variable_name, CLIENT_DEFAULT_PARAMETER_APPLICATION_ID, warn_if_empty=False)
