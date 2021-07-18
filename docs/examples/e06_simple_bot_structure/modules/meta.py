from hata import Client
from hata.ext.commands_v2 import checks

Sakuya: Client


@Sakuya.commands
@checks.owner_only()
async def ping():
    """Pongs."""
    return 'pong'
