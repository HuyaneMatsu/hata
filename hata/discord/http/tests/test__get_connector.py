import vampytest
from scarletio.http_client import TCPConnector

from ..connector_cache import get_connector


def test__get_connector():
    """
    Tests whether ``get_connector`` works as intended.
    """
    output_0 = get_connector()
    vampytest.assert_instance(output_0, TCPConnector)
    
    output_1 = get_connector()
    vampytest.assert_is(output_0, output_1)
