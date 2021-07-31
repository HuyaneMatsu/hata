__all__ = ()

from sys import platform as PLATFORM
from os.path import join as join_path
from os import listdir as list_directory, environ as ENVIRONMENTAL_VARIABLES
from tempfile import gettempdir as get_temporary_directory

from ...backend.utils import set_docs

from .constants import PAYLOAD_KEY_EVENT, EVENT_ERROR, PAYLOAD_KEY_DATA
from. exceptions import DiscordRPCError

if PLATFORM in ('linux', 'darwin'):
    TEMPORARY_DIRECTORY = ENVIRONMENTAL_VARIABLES.get('XDG_RUNTIME_DIR', None)
    if (TEMPORARY_DIRECTORY is None):
        TEMPORARY_DIRECTORY = ENVIRONMENTAL_VARIABLES.get('TMPDIR', None)
        if (TEMPORARY_DIRECTORY is None):
            TEMPORARY_DIRECTORY = ENVIRONMENTAL_VARIABLES.get('TMP', None)
            if (TEMPORARY_DIRECTORY is None):
                TEMPORARY_DIRECTORY = ENVIRONMENTAL_VARIABLES.get('TEMP', None)
                if (TEMPORARY_DIRECTORY is None):
                    TEMPORARY_DIRECTORY = get_temporary_directory()
    
    def get_ipc_path(pipe):
        ipc = f'discord-ipc-{pipe}'
        
        for path in (None, 'snap.discord', 'app/com.discordapp.Discord'):
            if path is None:
                full_path = TEMPORARY_DIRECTORY
            else:
                full_path = join_path(TEMPORARY_DIRECTORY)
            
            for node_name in list_directory(full_path):
                if node_name.startswith(ipc):
                    return join_path(full_path, node_name)
        
        return None

elif PLATFORM == 'win32':
    TEMPORARY_DIRECTORY = '\\\\?\\pipe'
    
    def get_ipc_path(pipe):
        ipc = f'discord-ipc-{pipe}'
        
        for node_name in list_directory(TEMPORARY_DIRECTORY):
            if node_name.startswith(ipc):
                return join_path(TEMPORARY_DIRECTORY, node_name)
        
        return None

else:
    def get_ipc_path(pipe):
        return None


set_docs(get_ipc_path,
    """
    Gets Discord inter process communication path.
    
    Parameters
    ----------
    pipe : `None` or `str`
        # TODO
    
    Returns
    -------
    path : `None` or `str`
    """)


def check_for_error(data):
    """
    Checks whether the given data contains an errors.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Data received from Discord.
    
    Raises
    ------
    DiscordRPCError
    """
    try:
        event = data[PAYLOAD_KEY_EVENT]
    except KeyError:
        pass
    else:
        if event == EVENT_ERROR:
            error_data = data[PAYLOAD_KEY_DATA]
            error_code = error_data['code']
            error_message = error_data['message']
            
            raise DiscordRPCError(error_code, error_message)


