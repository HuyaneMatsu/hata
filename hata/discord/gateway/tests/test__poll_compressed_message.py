import vampytest
from scarletio import Task

from ...core import KOKORO

from ..client_shard import _poll_compressed_message

from .helpers_web_socket_client import TestWebSocketClient


async def test__poll_compressed_message__chunked():
    """
    Tests whether ``_poll_compressed_message`` works as intended.
    
    Case: Chunked.
    
    This function is a coroutine.
    """
    web_socket = await TestWebSocketClient(
        KOKORO,
        '',
        in_operations = [
            ('receive', False, b'ab'),
            ('receive', False, b'cd'),
            ('receive', False, b'ef\x00\x00\xff\xff'),
        ],
    )
    task = Task(KOKORO, _poll_compressed_message(web_socket))
    task.apply_timeout(0.01)
    output = await task
    
    vampytest.assert_instance(output, bytes)
    vampytest.assert_eq(output, b'abcdef\x00\x00\xff\xff')


async def test__poll_compressed_message__single():
    """
    Tests whether ``_poll_compressed_message`` works as intended.
    
    Case: Single.
    
    This function is a coroutine.
    """
    web_socket = await TestWebSocketClient(
        KOKORO,
        '',
        in_operations = [
            ('receive', False, b'ef\x00\x00\xff\xff'),
        ],
    )
    
    task = Task(KOKORO, _poll_compressed_message(web_socket))
    task.apply_timeout(0.01)
    output = await task
    
    vampytest.assert_instance(output, bytes)
    vampytest.assert_eq(output, b'ef\x00\x00\xff\xff')
