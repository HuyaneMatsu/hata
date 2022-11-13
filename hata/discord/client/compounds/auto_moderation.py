__all__ = ()

from scarletio import Compound

from ...auto_moderation import AutoModerationRule
from ...http import DiscordHTTPClient

from ..request_helpers import (
    get_auto_moderation_rule_and_guild_id_and_id, get_auto_moderation_rule_guild_id_and_id, get_guild_id
)


class ClientCompoundAutoModerationEndpoints(Compound):
    
    http : DiscordHTTPClient
    
    async def auto_moderation_rule_get(self, auto_moderation_rule):
        """
        Requests the specified auto moderation rule.
        
        This method is a coroutine.
        
        Parameters
        ----------
        auto_moderation_rule : ``AutoModerationRule``, `tuple` (`int`, `int`)
            The auto moderation rule to get, or a `guild-id`, `rule-id` pair representing it.
        
        Returns
        -------
        auto_moderation_rule : ``AutoModerationRule``
        
        Raises
        ------
        TypeError
            If `auto_moderation_rule` was not given neither as ``AutoModerationRule`` nor `tuple` (`int`, `int`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        auto_moderation_rule, guild_id, auto_moderation_rule_id = get_auto_moderation_rule_and_guild_id_and_id(
            auto_moderation_rule
        )
        
        auto_moderation_rule_data = await self.http.auto_moderation_rule_get(guild_id, auto_moderation_rule_id)
        
        if (auto_moderation_rule is None):
            auto_moderation_rule = AutoModerationRule.from_data(auto_moderation_rule_data)
        
        else:
            auto_moderation_rule._update_attributes(auto_moderation_rule_data)
        
        return auto_moderation_rule
    
    
    async def auto_moderation_rule_get_all(self, guild):
        """
        Requests all the auto moderation rules of the given guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild or it's identifier.
        
        Returns
        -------
        auto_moderation_rules : `list` of``AutoModerationRule``
        
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
        
        auto_moderation_rule_datas = await self.http.auto_moderation_rule_get_all(guild_id)
        
        return [
            AutoModerationRule.from_data(auto_moderation_rule_data)
            for auto_moderation_rule_data in auto_moderation_rule_datas
        ]
    
    
    async def auto_moderation_rule_create(self, guild, auto_moderation_rule, *, reason = None):
        """
        Creates an auto moderation rule at the given guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild or it's identifier.
        auto_moderation_rule : ``AutoModerationRule``
            The auto moderation rule to create one like.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Returns
        -------
        auto_moderation_rule : ``AutoModerationRule``
            The created auto moderation rule.
        
        Raises
        ------
        TypeError
            - If `guild` was not given neither as ``Guild`` nor `int`.
            - If `auto_moderation_rule` was not given as ``AutoModerationRule``.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id = get_guild_id(guild)
        
        if not isinstance(auto_moderation_rule, AutoModerationRule):
            raise TypeError(
                f'`auto_moderation_rule` can be {AutoModerationRule.__name__}, '
                f'got {auto_moderation_rule.__class__.__name__}; {auto_moderation_rule!r}.'
            )
        
        data = auto_moderation_rule.to_data()
        
        auto_moderation_rule_data = await self.http.auto_moderation_rule_create(guild_id, data, reason)
        
        return AutoModerationRule.from_data(auto_moderation_rule_data)
    
    
    async def auto_moderation_rule_edit(self, old_auto_moderation_rule, new_auto_moderation_rule, *, reason = None):
        """
        Edits the specified auto moderation rule
        
        This method is a coroutine.
        
        Parameters
        ----------
        old_auto_moderation_rule : ``AutoModerationRule``, `tuple` (`int`, `int`)
            The auto moderation rule to edit, or a `guild-id`, `rule-id` pair representing it.
        new_auto_moderation_rule : ``AutoModerationRule``
            The auto moderation rule to edit the current to.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Returns
        -------
        auto_moderation_rule : ``AutoModerationRule``
        
        Raises
        ------
        TypeError
            - If `old_auto_moderation_rule` was not given neither as ``AutoModerationRule`` nor `tuple` (`int`, `int`).
            - If `new_auto_moderation_rule` was not given as ``AutoModerationRule``.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id, auto_moderation_rule_id = get_auto_moderation_rule_guild_id_and_id(old_auto_moderation_rule)
    
        if not isinstance(new_auto_moderation_rule, AutoModerationRule):
            raise TypeError(
                f'`new_auto_moderation_rule` can be {AutoModerationRule.__name__}, '
                f'got {new_auto_moderation_rule.__class__.__name__}; {new_auto_moderation_rule!r}.'
            )
        
        data = new_auto_moderation_rule.to_data()
        
        await self.http.auto_moderation_rule_edit(guild_id, auto_moderation_rule_id, data, reason)
    
    
    async def auto_moderation_rule_delete(self, auto_moderation_rule, *, reason = None):
        """
        Deletes the specified auto moderation rule.
        
        This method is a coroutine.
        
        Parameters
        ----------
        auto_moderation_rule : ``AutoModerationRule``, `tuple` (`int`, `int`)
            The auto moderation rule to delete, or a `guild-id`, `rule-id` pair representing it.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            If `auto_moderation_rule` was not given neither as ``AutoModerationRule`` nor `tuple` (`int`, `int`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id, auto_moderation_rule_id = get_auto_moderation_rule_guild_id_and_id(auto_moderation_rule)
        await self.http.auto_moderation_rule_delete(guild_id, auto_moderation_rule_id, reason)
