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
    
    
    async def auto_moderation_rule_create(self, guild, auto_moderation_rule):
        """
        Creates an auto moderation rule at the given guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild or it's identifier.
        auto_moderation_rule : ``AutoModerationRule``
            The auto moderation rule to create one like.
        
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
    
    async def auto_moderation_rule_edit(self, old_auto_moderation_rule, new_auto_moderation_rule):
        """
        Edits the specified auto moderation rule
        
        This method is a coroutine.
        
        Parameters
        ----------
        old_auto_moderation_rule : ``AutoModerationRule``, `tuple` (`int`, `int`)
            The auto moderation rule to edit, or a `guild-id`, `rule-id` pair representing it.
        new_auto_moderation_rule : ``AutoModerationRule``
            The auto moderation rule to edit the current to.
        
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
    
    
    async def auto_moderation_rule_delete(self, auto_moderation_rule):
        """
        Deletes the specified auto moderation rule.
        
        This method is a coroutine.
        
        Parameters
        ----------
        auto_moderation_rule : ``AutoModerationRule``, `tuple` (`int`, `int`)
            The auto moderation rule to delete, or a `guild-id`, `rule-id` pair representing it.
        
        Raises
        ------
        TypeError
            If `auto_moderation_rule` was not given neither as ``AutoModerationRule`` nor `tuple` (`int`, `int`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
