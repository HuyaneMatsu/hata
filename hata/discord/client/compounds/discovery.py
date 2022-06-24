__all__ = ()


from scarletio import Compound

from ...bases import maybe_snowflake
from ...core import DISCOVERY_CATEGORIES
from ...guild import DiscoveryCategory, Guild, GuildDiscovery
from ...http import DiscordHTTPClient, rate_limit_groups

from ..functionality_helpers import DiscoveryCategoryRequestCacher, DiscoveryTermRequestCacher
from ..request_helpers import get_guild_discovery_and_guild_id


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
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_discovery_data = await self.http.guild_discovery_get(guild.id)
        return GuildDiscovery(guild_discovery_data, guild)
    
    
    async def guild_discovery_edit(self, guild, *, primary_category=..., keywords=..., emoji_discovery=...):
        """
        Edits the guild's discovery metadata.
        
        The client must have `manage_guild` permission to execute this method.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, ``GuildDiscovery``, `int`
            The guild what's discovery metadata will be edited or an existing discovery metadata object.
        primary_category : `None`, ``DiscoveryCategory``, `int`, Optional (Keyword only)
            The guild discovery's new primary category's id. Can be given as a ``DiscoveryCategory`` object as well.
            If given as `None`, then resets the guild discovery's primary category id to it's default, what is `0`.
        keywords : `None`, (`iterable` of `str`), Optional (Keyword only)
            The guild discovery's new keywords. Can be given as `None` to reset to the default value, what is `None`,
            or as an `iterable` of strings.
        emoji_discovery : `None`, `bool`, Optional (Keyword only)
            Whether the guild info should be shown when the respective guild's emojis are clicked. If passed as `None`
            then will reset the guild discovery's `emoji_discovery` value to it's default, what is `True`.
        
        Returns
        -------
        guild_discovery : ``GuildDiscovery``
            Updated guild discovery object.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        TypeError
            - If `guild` was neither given as ``Guild``, ``GuildDiscovery``, `int`.
            - If `primary_category_id` was not given neither as `None`, `int`, ``DiscoveryCategory``.
            - If `keywords` was not passed neither as `None`, `iterable` of `str`.
            - If `emoji_discovery` was not given as `None`, `bool`.
        ValueError
            - If `primary_category_id` was given as not primary ``DiscoveryCategory`` object.
            - If `emoji_discovery` was given as `int`, but not as `0`, `1`.
        DiscordException
            If any exception was received from the Discord API.
        """
        if isinstance(guild, Guild):
            guild_id = guild.id
        
        elif isinstance(guild, GuildDiscovery):
            guild_id = guild.guild.id
        
        else:
            guild_id = maybe_snowflake(guild)
            if guild_id is None:
                raise TypeError(
                    f'`guild` can be `{Guild.__name__}`, `{GuildDiscovery.__name__}`, `int`, got '
                    f'{guild.__class__.__name__}; {guild!r}.'
                )
        
        data = {}
        
        if (primary_category is not ...):
            if (primary_category is None):
                primary_category_id = None
            else:
                primary_category_type = primary_category.__class__
                if primary_category_type is DiscoveryCategory:
                    # If name is set means that we should know whether the category is loaded, or just it's `.id`
                    # is known.
                    if (primary_category.name and (not primary_category.primary)):
                        raise ValueError(
                            f'The given `primary_category_id` is not a primary `{DiscoveryCategory.__name__}`, '
                            f'got {primary_category!r}.'
                        )
                    primary_category_id = primary_category.id
                
                elif primary_category_type is int:
                    primary_category_id = primary_category
                
                elif issubclass(primary_category_type, int):
                    primary_category_id = int(primary_category)
                
                else:
                    raise TypeError(
                        f'`primary_category` can be `None`, `int`, `{DiscoveryCategory.__name__}`, '
                        f'got {primary_category_type.__name__}; {primary_category!r}.'
                    )
            
            data['primary_category_id'] = primary_category_id
        
        if (keywords is not ...):
            if (keywords is None):
                pass
            elif (not isinstance(keywords, str)) and hasattr(type(keywords), '__iter__'):
                keywords_processed = set()
                index = 0
                for keyword in keywords:
                    if (type(keyword) is str):
                        pass
                    
                    elif isinstance(keyword, str):
                        keyword = str(keyword)
                    
                    else:
                        raise TypeError(
                            f'`keywords[{index}]` is not `str`, got {keyword.__class__.__name__}; {keyword!r}; '
                            f'keywords={keyword!r}.'
                        )
                    
                    keywords_processed.add(keyword)
                    index += 1
                
                keywords = keywords_processed
            else:
                raise TypeError(
                    f'`keywords` can be `None`, `iterable` of `str`, got {keywords.__class__.__name__}; {keywords!r}.'
                )
            
            data['keywords'] = keywords
        
        if (emoji_discovery is not ...):
            if (emoji_discovery is not None) and (not isinstance(emoji_discovery, bool)):
                raise TypeError(
                    f'`emoji_discovery` can be `None`, `bool`, got {emoji_discovery.__class__.__name__}; '
                    f'{emoji_discovery!r}.'
                )
            
            data['emoji_discoverability_enabled'] = emoji_discovery
        
        guild_discovery_data = await self.http.guild_discovery_edit(guild_id, data)
        
        if isinstance(guild, Guild):
            guild_discovery = GuildDiscovery(guild_discovery_data, guild)
        
        else:
            guild_discovery = guild
            guild_discovery._update_attributes(guild_discovery_data)
        
        return guild_discovery
    
    
    async def guild_discovery_add_subcategory(self, guild, category):
        """
        Adds a discovery subcategory to the guild.
        
        The client must have `manage_guild` permission to execute this method.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, ``GuildDiscovery``, `int`
            The guild to what the discovery subcategory will be added.
        category : ``DiscoveryCategory``, `int`
            The discovery category or it's id what will be added as a subcategory.
        
        Raises
        ------
        TypeError
            - If `guild` was not given neither as ``Guild``, ``GuildDiscovery``, neither as `int`.
            - If `category` was not passed neither as ``DiscoveryCategory``, `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        A guild can have maximum `5` discovery subcategories.
        
        If `guild` was given as ``GuildDiscovery``, then it will be updated.
        """
        guild_discovery, guild_id = get_guild_discovery_and_guild_id(guild)
        
        category_type = category.__class__
        if category_type is DiscoveryCategory:
            category_id = category.id
        elif category_type is int:
            category_id = category
        elif issubclass(category_type, int):
            category_id = int(category)
        else:
            raise TypeError(
                f'`category` can be `int`, `{DiscoveryCategory.__name__}`, got {category_type.__name__}; {category!r}.'
            )
        
        await self.http.guild_discovery_add_subcategory(guild_id, category_id)
        
        if (guild_discovery is not None):
            guild_discovery.sub_categories.add(category_id)
    
    
    async def guild_discovery_delete_subcategory(self, guild, category):
        """
        Removes a discovery subcategory of the guild.
        
        The client must have `manage_guild` permission to execute this method.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, ``GuildDiscovery``, `int`
            The guild to what the discovery subcategory will be removed from.
        category : ``DiscoveryCategory``, `int`
            The discovery category or it's id what will be removed from the subcategories.
        
        Raises
        ------
        TypeError
            - If `guild` was not given neither as ``Guild``, ``GuildDiscovery``, neither as `int`.
            - If `category` was not passed neither as ``DiscoveryCategory``, `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        A guild can have maximum `5` discovery subcategories.
        
        If `guild` was given as ``GuildDiscovery``, then it will be updated.
        """
        guild_discovery, guild_id = get_guild_discovery_and_guild_id(guild)
        
        category_type = category.__class__
        if category_type is DiscoveryCategory:
            category_id = category.id
        elif category_type is int:
            category_id = category
        elif issubclass(category_type, int):
            category_id = int(category)
        else:
            raise TypeError(
                f'`category` can be `int`, `{DiscoveryCategory.__name__}`, got {category_type.__name__}; {category!r}.'
            )
        
        await self.http.guild_discovery_delete_subcategory(guild_id, category_id)
        
        if (guild_discovery is not None):
            guild_discovery.sub_categories.discard(category_id)
    
    
    async def _discovery_category_get_all(self):
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
        discovery_category_datas = await self.http.discovery_category_get_all()
        return [DiscoveryCategory.from_data(discovery_category_data)
            for discovery_category_data in discovery_category_datas]
    
    
    # Add cached, so even tho the first request fails with `ConnectionError` will not be raised.
    discovery_category_get_all = DiscoveryCategoryRequestCacher(
        _discovery_category_get_all,
        3600.0,
        list(DISCOVERY_CATEGORIES.values()),
    )
    
    
    async def discovery_validate_term(self, term):
        """
        Checks whether the given discovery search term is valid.
        
        This method is a coroutine.
        
        Parameters
        ----------
        term : `str`
        
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
