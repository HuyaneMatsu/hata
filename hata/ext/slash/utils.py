# -*- coding: utf-8 -*-
from ...backend.futures import sleep
from ...discord.client_core import KOKORO

from .command import Slasher

async def _do_initial_sync(client):
    """
    `ready` event handler added to the respective client by the ``setup_ext_slash`` function.
    
    On the first ready event syncs the slasher's commands. If the sync is successful, removes itself.
    
    This method is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who has the extension setuped and received the ready event.
    """
    slasher = getattr(client, 'slasher', None)
    if (slasher is not None) and isinstance(slasher, Slasher):
        success = await slasher.do_initial_sync(client)
        if not success:
            return
    
    # If the client's extension disappeared or if initial sync passed, remove the event handler.
    client.events.remove(_do_initial_sync, 'ready', count=1)


async def _application_command_create_watcher(client, guild, application_command):
    """
    `application_command_create` event handler.
    
    Tries to register the command at the respective slash command processor as a guild-bound or non-global command.
    
    This method is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The respective client instance.
    guild : `Guild``
        The guild to where the command was added.
    application_command : ``ApplicationCommand``
        The added application command.
    """
    slasher = getattr(client, 'slasher', None)
    if (slasher is not None) and isinstance(slasher, Slasher):
        slasher._maybe_register_guild_command(application_command, guild.id)


async def _application_command_delete_watcher(client, guild, application_command):
    """
    `application_command_delete` event handler added to the respective client by the ``setup_ext_slash`` function.
    
    Tries to remove the command from the respective slash command processor.
    
    This method is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The respective client instance.
    guild : `Guild``
        The guild to where the command was deleted from.
    application_command : ``ApplicationCommand``
        The deleted application command.
    """
    slasher = getattr(client, 'slasher', None)
    if (slasher is not None) and isinstance(slasher, Slasher):
        slasher._maybe_unregister_guild_command(application_command, guild.id)


async def delay_immediate_start_initial_sync(client, slasher):
    slash_command_count = len(slasher.registered_commands)
    while True:
        await sleep(0.2, KOKORO)
        slash_command_new_count = len(slasher.registered_commands)
        if slash_command_count == slash_command_new_count:
            break
        
        slash_command_count = slash_command_new_count
        continue
    
    await slasher.do_initial_sync(client)
    # Ignore method return, will be called by ``_do_initial_sync`` anyways.

