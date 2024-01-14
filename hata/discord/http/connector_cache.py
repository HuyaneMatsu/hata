__all__ = ()

from scarletio.http_client import TCPConnector

from ..core import KOKORO


CONNECTOR = None


def get_connector():
    """
    Gets tcp connector. If already retrieved once returns that instead.
    
    Returns
    -------
    connector : ``TCPConnector`` 
    """
    global CONNECTOR
    if (CONNECTOR is None) or CONNECTOR.closed:
        CONNECTOR = TCPConnector(KOKORO)
    
    return CONNECTOR
