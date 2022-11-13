"""
Lavalink extension for hata.

Named after okuu's theme:

```
Solar Sect of Mystic Wisdom ~ Nuclear Fusion
```
"""

from .client import *
from .constants import *
from .event_handler_plugin import *
from .event_handlers import *
from .event_types import *
from .exceptions import *
from .filters import *
from .node import *
from .parsers import *
from .player import *
from .player_base import *
from .route_planner import *
from .stats import *
from .track import *
from .track_end_reasons import *

from . import  track_end_reasons as TRACK_END_REASONS

__all__ = (
    'TRACK_END_REASONS',
    *client.__all__,
    *constants.__all__,
    *event_handler_plugin.__all__,
    *event_handlers.__all__,
    *event_types.__all__,
    *exceptions.__all__,
    *filters.__all__,
    *node.__all__,
    *parsers.__all__,
    *player.__all__,
    *player_base.__all__,
    *route_planner.__all__,
    *stats.__all__,
    *track.__all__,
    *track_end_reasons.__all__,
)

from .. import register_library_extension, register_setup_function

from .event_handlers import handle_voice_client_join, handle_voice_client_move, handle_voice_client_update, \
    handle_voice_client_leave, handle_voice_server_update, handle_voice_client_ghost, handle_voice_client_shutdown

def setup_ext_solarlink(client):
    """
    Setups the solarlink extension on the client.
    
    Parameters
    ----------
    client : ``Client``
        The client to setup the extension into.
    
    Returns
    -------
    solarlink : ``SolarClient``
        The solar client controlling lavalink nodes.
    
    Raises
    ------
    TypeError
        - If `client` is not ``Client``.
    RuntimeError
        - If any attribute of the extension, is already used by the client.
    
    """
    for attr_name in ('solarlink', ):
        if hasattr(client, attr_name):
            raise RuntimeError(f'The client already has an attribute named as `{attr_name}`.')
    
    solar_client = SolarClient(client)
    client.solarlink = solar_client
    
    client.events(handle_voice_client_join, name = 'voice_client_join', overwrite=True)
    client.events(handle_voice_client_move, name = 'voice_client_move', overwrite=True)
    client.events(handle_voice_client_update, name = 'voice_client_update', overwrite=True)
    client.events(handle_voice_client_leave, name = 'voice_client_leave', overwrite=True)
    client.events(handle_voice_server_update, name = 'voice_server_update', overwrite=True)
    client.events(handle_voice_client_ghost, name = 'voice_client_ghost', overwrite=True)
    client.events(handle_voice_client_shutdown, name = 'voice_client_shutdown', overwrite=True)
    
    return solar_client


register_library_extension('HuyaneMatsu.solarlink')

register_setup_function(
    'HuyaneMatsu.solarlink',
    setup_ext_solarlink,
    None,
    None,
)
