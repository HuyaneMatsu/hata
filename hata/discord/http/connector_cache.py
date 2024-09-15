__all__ = ()

from scarletio.http_client import ConnectorTCP

from ..core import KOKORO


CONNECTOR = None


def get_connector():
    """
    Gets tcp connector. If already retrieved once returns that instead.
    
    Returns
    -------
    connector : ``ConnectorTCP`` 
    """
    global CONNECTOR
    if (CONNECTOR is None) or CONNECTOR.closed:
        CONNECTOR = ConnectorTCP(KOKORO)
    
    return CONNECTOR
