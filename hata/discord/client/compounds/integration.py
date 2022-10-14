__all__ = ()

from scarletio import Compound
from ....env import API_VERSION

from ...bases import maybe_snowflake
from ...http import DiscordHTTPClient
from ...integration import Integration
from ..request_helpers import get_guild_id


class ClientCompoundIntegrationEndpoints(Compound):
    
    http : DiscordHTTPClient
    
    
    #TODO: decide if we should store integrations at Guild objects
    if API_VERSION > 7:
        async def integration_get_all(self, guild):
            """
            Requests the integrations of the given guild.
            
            This method is a coroutine.
            
            Parameters
            ----------
            guild : ``Guild``, `int`
                The guild, what's integrations will be requested.
            
            Returns
            -------
            integrations : `list` of ``Integration``
            
            Raises
            ------
            TypeError
                If `guild` was not given neither as ``Guild`` nor `int`.
            ConnectionError
                No internet connection.
            DiscordException
                If any exception was received from the Discord API.
            """
            guild_id = get_guild_id(guild)
            
            integration_datas = await self.http.integration_get_all(guild_id, None)
            return [Integration.from_data(integration_data) for integration_data in integration_datas]
    
    else:
        async def integration_get_all(self, guild):
            """
            Requests the integrations of the given guild.
            
            This method is a coroutine.
            
            Parameters
            ----------
            guild : ``Guild``, `int`
                The guild, what's integrations will be requested.
            
            Returns
            -------
            integrations : `list` of ``Integration``
            
            Raises
            ------
            TypeError
                If `guild` was not given neither as ``Guild`` nor `int`.
            ConnectionError
                No internet connection.
            DiscordException
                If any exception was received from the Discord API.
            """
            guild_id = get_guild_id(guild)
            
            integration_datas = await self.http.integration_get_all(guild_id, {'include_applications': True})
            return [Integration.from_data(integration_data) for integration_data in integration_datas]
    
    
    async def integration_create(self, guild, integration_id, type_):
        """
        Creates an integration at the given guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild to what the integration will be attached to.
        integration_id : ``int``
            The integration's id.
        type_ : `str`
            The integration's type (`'twitch'`, `'youtube'`, etc.).
        
        Returns
        -------
        integration : ``Integration``
            The created integrated.
        
        Raises
        ------
        TypeError
            - If `guild` was not given neither as ``Guild`` nor `int`.
            - If `integration_id` was not given as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If `type_` is not given as `str`.
        """
        guild_id = get_guild_id(guild)
        
        integration_id_value = maybe_snowflake(integration_id)
        if integration_id_value is None:
            raise TypeError(
                f'`integration_id` can be `int`, got {integration_id.__class__.__name__}; {integration_id!r}.'
            )
        
        if __debug__:
            if not isinstance(type_, str):
                raise AssertionError(
                    f'`type_` can be `str`, got {type_.__class__.__name__}; {type_!r}.'
                )
        
        data = {
            'id'   : integration_id_value,
            'type' : type_,
        }
        
        data = await self.http.integration_create(guild_id, data)
        return Integration.from_data(data)
    
    
    async def integration_edit(
        self, integration, *, expire_behavior=..., expire_grace_period=..., enable_emojis=...
    ):
        """
        Edits the given integration.
        
        This method is a coroutine.
        
        Parameters
        ----------
        integration : ``Integration``
            The integration to edit.
        expire_behavior : `int`, Optional (Keyword only)
            Can be `0` for kick or `1` for role  remove.
        expire_grace_period : `int`, Optional (Keyword only)
            The time in days, after the subscription will be ignored. Can be any of `(1, 3, 7, 14, 30)`.
        enable_emojis : `bool`, Optional (Keyword only)
            Whether the users can use the integration's emojis in Discord.
        
        Raises
        ------
        TypeError
            - If `expire_behavior` was not passed as `int`.
            - If `expire_grace_period` was not passed as `int`.
            - If `enable_emojis` was not passed as `bool`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `integration` was not given as ``Integration``.
            - If `expire_behavior` was not given neither as `None` nor as `int`.
            - If `expire_grace_period` was not given neither as `None` nor as `int`.
            - If `expire_behavior` is not any of: `(0, 1)`.
            - If `expire_grace_period` is not any of `(1, 3, 7, 14, 30)`.
            - If `enable_emojis` is neither `None`, `bool`.
        """
        if __debug__:
            if not isinstance(integration, Integration):
                raise AssertionError(
                    f'`integration` can be `{Integration.__name__}`, got '
                    f'{integration.__class__.__name__}; {integration!r}.'
                )
        
        detail = integration.detail
        if detail is None:
            return
        
        role = detail.role
        if role is None:
            return
        
        data = {}
        
        if expire_behavior is not ...:
            if __debug__:
                if not isinstance(expire_behavior, int):
                    raise AssertionError(
                        f'`expire_behavior` can be `None`, `int`, got '
                        f'{expire_behavior.__class__.__name__}; {expire_behavior!r}.'
                    )
                
                if expire_behavior not in (0, 1):
                    raise AssertionError(
                        f'`expire_behavior` should be 0 for kick, 1 for remove role, got {expire_behavior!r}.'
                    )
            
            data['expire_behavior'] = expire_behavior
        
        if expire_grace_period is not ...:
            if __debug__:
                if not isinstance(expire_grace_period, int):
                    raise AssertionError(
                        f'`expire_grace_period` can be `None`, `int`, got '
                        f'{expire_grace_period.__class__.__name__}.'
                    )
                
                if expire_grace_period not in (1, 3, 7, 14, 30):
                    raise AssertionError(
                        f'`expire_grace_period` can be one of `(1, 3, 7, 14, 30)`, got {expire_grace_period!r}.'
                    )
                
            data['expire_grace_period'] = expire_grace_period
   
        
        if (enable_emojis is not ...):
            if __debug__:
                if not isinstance(enable_emojis, bool):
                    raise AssertionError(
                        f'`enable_emojis` can be `None`, `bool`, got '
                        f'{enable_emojis.__class__.__name__}; {enable_emojis!r}.'
                    )
            
            data['enable_emoticons'] = enable_emojis
        
        await self.http.integration_edit(role.guild_id, integration.id, data)
    
    
    async def integration_delete(self, integration):
        """
        Deletes the given integration.
        
        This method is a coroutine.
        
        Parameters
        ----------
        integration : ``Integration``
            The integration what will be deleted.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If `integration` was not given as ``Integration``.
        """
        if __debug__:
            if not isinstance(integration, Integration):
                raise AssertionError(
                    f'`integration` can be `{Integration.__name__}`, got {integration.__class__.__name__}; '
                    f'{integration!r}.'
                )
        
        detail = integration.detail
        if detail is None:
            return
        
        role = detail.role
        if role is None:
            return
        
        await self.http.integration_delete(role.guild_id, integration.id)
    
    
    async def integration_sync(self, integration):
        """
        Sync the given integration's state.
        
        This method is a coroutine.
        
        Parameters
        ----------
        integration : ``Integration``
            The integration to sync.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If `integration` was not given as ``Integration``.
        """
        if __debug__:
            if not isinstance(integration, Integration):
                raise AssertionError(
                    f'`integration` can be `{Integration.__name__}`, got {integration.__class__.__name__}; '
                    f'{integration!r}.'
                )
        
        detail = integration.detail
        if detail is None:
            return
        
        role = detail.role
        if role is None:
            return
        
        await self.http.integration_sync(role.guild_id, integration.id)
