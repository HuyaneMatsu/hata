__all__ = ()

from .slasher import Slasher


async def _do_initial_sync(client):
    """
    `ready` event handler added to the respective client by the ``setup_ext_slash`` function.
    
    On the first ready event syncs the slasher's commands. If the sync is successful, removes itself.
    
    This method is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who has the extension setupped and received the ready event.
    """
    slasher = getattr(client, 'slasher', None)
    if (slasher is not None) and isinstance(slasher, Slasher):
        success = await slasher.sync()
        if not success:
            return
    
    # If the client's extension disappeared or if initial sync passed, remove the event handler.
    client.events.remove(_do_initial_sync, 'launch', count=1)


async def _application_command_create_watcher(client, guild_id, application_command):
    """
    `application_command_create` event handler.
    
    Tries to register the command at the respective slash command processor as a guild-bound or non-global command.
    
    This method is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The respective client instance.
    guild_id : `int`
        The guild's identifier to where the command was added.
    application_command : ``ApplicationCommand``
        The added application command.
    """
    slasher = getattr(client, 'slasher', None)
    if (slasher is not None) and isinstance(slasher, Slasher):
        slasher._maybe_register_guild_command(application_command, guild_id)


async def _application_command_delete_watcher(client, guild_id, application_command):
    """
    `application_command_delete` event handler added to the respective client by the ``setup_ext_slash`` function.
    
    Tries to remove the command from the respective slash command processor.
    
    This method is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The respective client instance.
    guild_id : `int`
        The guild's identifier to where the command was deleted from.
    application_command : ``ApplicationCommand``
        The deleted application command.
    """
    slasher = getattr(client, 'slasher', None)
    if (slasher is not None) and isinstance(slasher, Slasher):
        slasher._maybe_unregister_guild_command(application_command, guild_id)


async def _application_command_permission_update_watcher(client, permission):
    """
    `application_command_permission_update` event handler.
    
    Whenever an application command's permissions is updated, will notify the client's ``Slasher`` about it.
    
    This method is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The respective client instance.
    permission : ``ApplicationCommandPermission``
        The updated application command's permissions.
    """
    slasher = getattr(client, 'slasher', None)
    if (slasher is not None) and isinstance(slasher, Slasher):
        slasher._maybe_store_application_command_permission(permission)
