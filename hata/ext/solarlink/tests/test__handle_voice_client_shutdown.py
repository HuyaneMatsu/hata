from .... import Client

from .. import handle_voice_client_shutdown


async def test__handle_voice_client_shutdown__0():
    """
    Tests whether ``handle_voice_client_shutdown`` runs without exception.
    
    Issue: `AttributeError` in `handle_voice_client_shutdown` (typo).
    
    Notes: When exception occurred no nodes where added.
    """
    client = Client(
        'token_20220722',
        extensions = 'solarlink'
    )
    
    try:
        await handle_voice_client_shutdown(client)
    finally:
        client._delete()
        client = None
