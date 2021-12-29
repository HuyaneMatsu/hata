from ..settings import load_settings_from_current_working_directory
from ..utils import create_file_structure


CONVERT_TO_UNDERSCORE = frozenset((
    '\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<',
    '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', '}',
))

UNDERSCORE = '_'

def prepare_bot_name(bot_name):
    """
    Prepares bot name.
    
    Parameters
    ----------
    bot_name : `str`
        The bot name to prepare.
    
    Returns
    -------
    bot_name : `str`
    """
    is_last_underscore = True
    new_name_characters = []
    
    for character in bot_name:
        if character in CONVERT_TO_UNDERSCORE:
            if not is_last_underscore:
                is_last_underscore = True
                new_name_characters.append(UNDERSCORE)
        else:
            new_name_characters.append(character)
            is_last_underscore = False
    
    if is_last_underscore:
        while True:
            if not new_name_characters:
                break
            
            del new_name_characters[-1]
            
            if new_name_characters[-1] == UNDERSCORE:
                continue
            
            break
    
    return ''.join(new_name_characters)


def convert_bot_name_to_directory_name(bot_name):
    """
    Coverts the given bot name to directory name.
    
    Parameters
    ----------
    bot_name : `str`
        The bot name to convert.
    
    Return
    ------
    directory_name : `str`
    """
    return bot_name.lower()


def convert_bot_name_to_environmental_name(bot_name):
    """
    Coverts the given bot name to environmental variable name.
    
    Parameters
    ----------
    bot_name : `str`
        The bot name to convert.
    
    Return
    ------
    environmental_name : `str`
    """
    return bot_name.lower()


def command(parameters):
    """
    Preparation to call the command.
    
    Parameters
    ----------
    parameters : `dict` of (`str`, `Any`)
        Command parameters
    
    Returns
    -------
    command_result : `str`
    """
    settings = load_settings_from_current_working_directory()
    bot_name = parameters['bot_name']
    
    return add_bot(settings, bot_name)


def format_bot_init(bot_name, bot_directory_name, environmental_variable_prefix):
    return (
        f'from hata import Client\n'
        f'from hata.ext.extension_loader import EXTENSION_LOADER\n'
        f'from hata.ext.management import get_client_application_id, get_client_id, get_client_secret, '
        f'get_client_token\n'
        f'\n'
        f'\n'
        f'CLIENT_ENV = \'{environmental_variable_prefix}\'\n'
        f'\n'
        f'{bot_name} = Client(\n'
        f'    get_client_token(CLIENT_ENV),\n'
        f'    application_id = get_client_application_id(CLIENT_ENV),\n'
        f'    client_id = get_client_id(CLIENT_ENV),\n'
        f'    secret = get_client_secret(CLIENT_ENV),\n'
        f'    extensions = (), # List used extensions here\n'
        f')\n'
        f'\n'
        f'\n'
        f'EXTENSION_LOADER.add_default_variable({bot_name} = {bot_name})\n'
        f'EXTENSION_LOADER.add(\'{bot_directory_name}.modules\')\n'
        f''
    )


def add_bot(settings, bot_name):
    """
    Parameters
    ----------
    settings : ``ProjectSettings``
        The project's settings.
    bot_name : `str`
        The bot's name.
    
    Returns
    -------
    command_result : `str`
    
    Raises
    ------
    RuntimeError
        - If received empty bot name.
        - If there is already a bot registered with the given name.
    """
    bot_name = prepare_bot_name(bot_name)
    if not bot_name:
        raise RuntimeError(
            f'Received empty bot name.'
        )
    
    bot_directory_name = convert_bot_name_to_directory_name(bot_name)
    
    bot_directories = settings.bot_directories
    if (bot_directories is not None) and (bot_directory_name in bot_directories):
        raise RuntimeError(
            f'There is already a bot registered with the given name.'
        )
    
    environmental_variable_prefix = convert_bot_name_to_environmental_name(bot_name)
    
    structure = (
        (
            (bot_directory_name, '__init__.py'),
            format_bot_init(bot_name, bot_directory_name, environmental_variable_prefix),
        ), (
            (bot_directory_name, 'modules', None),
            None,
        )
    )
    
    create_file_structure(settings.directory_path, structure)
