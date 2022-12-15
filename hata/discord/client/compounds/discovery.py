__all__ = ()

import warnings

from scarletio import Compound

from ...guild import DiscoveryCategory, Guild, GuildDiscovery
from ...guild.discovery.utils import GUILD_DISCOVERY_FIELD_CONVERTERS
from ...http import DiscordHTTPClient, rate_limit_groups
from ...payload_building import build_edit_payload

from ..functionality_helpers import DiscoveryCategoryRequestCacher, DiscoveryTermRequestCacher
from ..request_helpers import get_guild_id


class ClientCompoundDiscoveryEndpoints(Compound):
    
    http : DiscordHTTPClient
    
    
    async def guild_discovery_get(self, guild):
        """
        Requests and returns the guild's discovery metadata.
        
        The client must have `manage_guild` permission to execute this method.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``
            The guild what's discovery will be requested.
        
        Returns
        -------
        guild_discovery : ``GuildDiscovery``
        
        Raises
        ------
        TypeError
            - If `guild` is not ``Guild``, `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id = get_guild_id(guild)
        guild_discovery_data = await self.http.guild_discovery_get(guild_id)
        return GuildDiscovery.from_data(guild_discovery_data)
    
    
    async def guild_discovery_edit(self, guild, discovery_template = None, **keyword_parameters):
        """
        Edits the guild's discovery metadata.
        
        The client must have `manage_guild` permission to execute this method.
        
        This method is a coroutine.
        
        
        > To modify sub-categories use the ``.guild_discovery_add_sub_category`` and the
        > ``.guild_discovery_delete_sub_category`` methods.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild what's discovery metadata will be edited or an existing discovery metadata object.
        
        discovery_template : `None`, ``GuildDiscovery`` = `None`, Optional
            Guild discovery to use as a template.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters to define which fields should be modified.
        
        Other Parameters
        ----------------
        emoji_discovery : `bool`, Optional (Keyword only)
            Whether guild info is shown when the respective guild's emojis are clicked.
        keywords : `None`, `iterable` of `str`, Optional (Keyword only)
            The set discovery search keywords for the guild.
        primary_category : ``DiscoveryCategory``, `int`, Optional (Keyword only)
            The primary discovery category of the guild.
        
        Returns
        -------
        guild_discovery : ``GuildDiscovery``
        
        Raises
        ------
        TypeError
            - If `guild` is not ``Guild``, `int`.
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id = get_guild_id(guild)
        data = build_edit_payload(None, discovery_template, GUILD_DISCOVERY_FIELD_CONVERTERS, keyword_parameters)
        guild_discovery_data = await self.http.guild_discovery_edit(guild_id, data)
        return GuildDiscovery.from_data(guild_discovery_data)
    
    
    async def guild_discovery_add_subcategory(self, *positional_parameters, **keyword_parameters):
        """
        ``Client.guild_discovery_add_subcategory`` is deprecated and will be removed in 2023 Mar.
        Please use ``.guild_discovery_add_sub_category`` instead.
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.guild_discovery_add_subcategory` is deprecated and will be removed in '
                f'2023 Mar. Please use `.guild_discovery_add_sub_category` instead.'
            ),
            FutureWarning
        )
        
        return await self.guild_discovery_add_sub_category(*positional_parameters, **keyword_parameters)
    
    
    async def guild_discovery_add_sub_category(self, guild, category):
        """
        Adds a discovery subcategory to the guild.
        
        The client must have `manage_guild` permission to execute this method.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild to what the discovery subcategory will be added.
        category : ``DiscoveryCategory``, `int`
            The discovery category or it's id what will be added as a subcategory.
        
        Raises
        ------
        TypeError
            - If `guild` is not ``Guild``, `int`.
            - If `category`is not ``DiscoveryCategory``, `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        A guild can have maximum `5` discovery subcategories.
        """
        guild_id = get_guild_id(guild)
        
        if isinstance(category, DiscoveryCategory):
            category_id = category.id
        elif isinstance(category, DiscoveryCategory.VALUE_TYPE):
            category_id = category
        else:
            raise TypeError(
                f'`category` can be `{DiscoveryCategory.__name__}`, `{DiscoveryCategory.VALUE_TYPE.__name__}`, '
                f'got {category.__class__.__name__}; {category!r}.'
            )
        
        await self.http.guild_discovery_add_sub_category(guild_id, category_id)
    
    
    async def guild_discovery_delete_subcategory(self, *positional_parameters, **keyword_parameters):
        """
        ``Client.guild_discovery_delete_subcategory`` is deprecated and will be removed in 2023 Mar.
        Please use ``.guild_discovery_delete_sub_category`` instead.
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.guild_discovery_delete_subcategory` is deprecated and will be removed in '
                f'2023 Mar. Please use `.guild_discovery_delete_sub_category` instead.'
            ),
            FutureWarning
        )
        
        return await self.guild_discovery_delete_sub_category(*positional_parameters, **keyword_parameters)
    
    
    async def guild_discovery_delete_sub_category(self, guild, category):
        """
        Removes a discovery subcategory of the guild.
        
        The client must have `manage_guild` permission to execute this method.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild to what the discovery subcategory will be removed from.
        category : ``DiscoveryCategory``, `int`
            The discovery category or it's id what will be removed from the subcategories.
        
        Raises
        ------
        TypeError
            - If `guild` is not ``Guild``, `int`.
            - If `category`is not ``DiscoveryCategory``, `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        A guild can have maximum `5` discovery subcategories.
        """
        guild_id = get_guild_id(guild)
        
        if isinstance(category, DiscoveryCategory):
            category_id = category.id
        elif isinstance(category, DiscoveryCategory.VALUE_TYPE):
            category_id = category
        else:
            raise TypeError(
                f'`category` can be `{DiscoveryCategory.__name__}`, `{DiscoveryCategory.VALUE_TYPE.__name__}`, '
                f'got {category.__class__.__name__}; {category!r}.'
            )
        
        await self.http.guild_discovery_delete_sub_category(guild_id, category_id)
    
    
    async def discovery_category_get_all(self):
        """
        Returns a list of discovery categories, which can be used when editing guild discovery.
        
        This method is a coroutine.
        
        Returns
        -------
        discovery_categories : `list` of ``DiscoveryCategory``
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        discovery_category_datas = await self.http.discovery_category_get_all(None)
        return [
            DiscoveryCategory.from_data(discovery_category_data)
            for discovery_category_data in discovery_category_datas
        ]
    
    
    # Add cached, so even tho the first request fails with `ConnectionError` will not be raised.
    discovery_category_get_all = DiscoveryCategoryRequestCacher(
        discovery_category_get_all,
        3600.0,
        [*DiscoveryCategory.INSTANCES.values()],
    )
    
    
    async def discovery_validate_term(self, term):
        """
        Checks whether the given discovery search term is valid.
        
        This method is a coroutine.
        
        Parameters
        ----------
        term : `str`
            Discovery term to validate.
        
        Returns
        -------
        valid : `bool`
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        data = await self.http.discovery_validate_term({'term': term})
        return data['valid']
    
    
    discovery_validate_term = DiscoveryTermRequestCacher(
        discovery_validate_term,
        86400.0,
        rate_limit_groups.discovery_validate_term,
    )
