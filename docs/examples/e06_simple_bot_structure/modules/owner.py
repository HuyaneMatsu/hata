import os
from hata import Client
from hata.ext.commands_v2 import checks

Sakuya: Client


@Sakuya.commands
@checks.owner_only()
async def quit_(ctx):
    """Shuts the bot down."""
    await ctx.reply('Shutting down!')
    # A little bit brute force, but works on windows as well :')
    os._exit(0)
