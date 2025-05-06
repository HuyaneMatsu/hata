__all__ = ()

from scarletio import Compound

from ...core import GUILDS
from ...emoji import Emoji
from ...emoji.emoji.utils import EMOJI_FIELD_CONVERTERS
from ...http import DiscordApiClient
from ...payload_building import build_create_payload, build_edit_payload
from ...utils import image_to_base64

from ..request_helpers import get_emoji_and_guild_id_and_id, get_emoji_guild_id_and_id, get_guild_and_id, get_guild_id


class ClientCompoundEmojiGuildEndpoints(Compound):
    
    api : DiscordApiClient
    
    async def emoji_get_guild(self, emoji, *, force_update = False):
        """
        Requests the emoji by it's id at the given guild.
        If the client's logging in is finished, then it should have all of its emojis loaded already.
        
        This method is a coroutine.
        
        Parameters
        ----------
        emoji : ``Emoji``, `(int, int)`
            The emoji, or 2 snowflake representing it.
        
        force_update : `bool` = `False`, Optional (Keyword only)
            Whether the emoji should be requested even if it supposed to be up to date.
        
        Returns
        -------
        emoji : ``Emoji``
        
        Raises
        ------
        TypeError
            - If `emoji` is given as incorrect type.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        emoji, guild_id, emoji_id = get_emoji_and_guild_id_and_id(emoji)
        
        # If the emoji has no linked guild, we cannot request it, so we return instantly.
        if not guild_id:
            # Create empty emoji instead of returning `None` to stop expected errors
            if emoji is None:
                emoji = Emoji.precreate(emoji_id)
            
            return emoji
        
        if (not force_update) and (emoji is not None) and (not emoji.partial):
            return emoji
        
        emoji_data = await self.api.emoji_get_guild(guild_id, emoji_id)
        
        if (emoji is None):
            emoji = Emoji.from_data(emoji_data, guild_id)
        else:
            emoji._set_attributes(emoji_data, guild_id)
        
        return emoji
    
    
    async def emoji_get_all_guild(self, guild):
        """
        Requests the given guild's emojis.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``int | Guild``
            The guild, what's emojis will be synced.
        
        Returns
        -------
        emojis : `list` of ``Emoji``
            The guild's emojis.
        
        Raises
        ------
        TypeError
            - If `guild`'s type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild, guild_id = get_guild_and_id(guild)
        
        emoji_datas = await self.api.emoji_get_all_guild(guild_id)
        
        if guild is None:
            # Do not create a partial guild, because it would have been garbage collected after leaving the function
            # anyways
            guild = GUILDS.get(guild_id, None)
        
        if guild is None:
            emojis = [Emoji.from_data(emoji_data, guild_id) for emoji_data in emoji_datas]
        else:
            guild._update_emojis(emoji_datas)
            emojis = [*guild.iter_emojis()]
        
        return emojis
    
    
    async def emoji_create_guild(self, guild, image, emoji_template = None, *, reason = None, **keyword_parameters):
        """
        Creates an emoji at the given guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``int | Guild``
            The guild where the emoji will be created.
        
        image : `bytes-like`
            The emoji's icon. Up to 256 kB.
        
        emoji_template : `None`, ``Emoji`` = `None`, Optional
            Emoji entity to use as a template.
        
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the `guild`'s audit logs.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters to create the emoji with.
        
        Other attributes
        ----------------
        name : `str`, Optional (Keyword only)
            The emoji's name. It's length can be between `2` and `32`.
        
        role_ids : `None | iterable<int> | iterable<Role>` = `None`, Optional (Keyword only)
            Whether the created emoji should be limited only to users with any of the specified roles.
        
        roles : `None | iterable<int> | iterable<Role>` = `None`, Optional (Keyword only)
            Alias for `role_ids`.
        
        Returns
        -------
        emoji : ``Emoji``
            The created emoji.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        Only some characters can be in the emoji's name, so every other character is filtered out.
        """
        guild_id = get_guild_id(guild)
        data = build_create_payload(emoji_template, EMOJI_FIELD_CONVERTERS, keyword_parameters)
        data['image'] = image_to_base64(image)
        emoji_data = await self.api.emoji_create_guild(guild_id, data, reason)
        return Emoji.from_data(emoji_data, guild_id)
    
    
    async def emoji_edit_guild(self, emoji, emoji_template = None, *, reason = None, **keyword_parameters):
        """
        Edits the given (guild) emoji.
        
        This method is a coroutine.
        
        Parameters
        ----------
        emoji : ``Emoji``, `(int, int)`
            The emoji to edit.
        
        emoji_template : `None`, ``Emoji`` = `None`, Optional
            A emoji to use as a template.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters either to define the template, or to overwrite specific fields' values.
        
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Other attributes
        ----------------
        name : `str`, Optional (Keyword only)
            The emoji's name. It's length can be between `2` and `32`.
        
        role_ids : `None | iterable<int> | iterable<Role>` = `None`, Optional (Keyword only)
            Whether the created emoji should be limited only to users with any of the specified roles.
        
        roles : `None | iterable<int> | iterable<Role>` = `None`, Optional (Keyword only)
            Alias for `role_ids`.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        emoji, guild_id, emoji_id = get_emoji_and_guild_id_and_id(emoji)
        
        # Cannot edit partially loaded emojis.
        if not guild_id:
            return
        
        data = build_edit_payload(emoji, emoji_template, EMOJI_FIELD_CONVERTERS, keyword_parameters)
        
        if data:
            await self.api.emoji_edit_guild(guild_id, emoji_id, data, reason)
    
    
    async def emoji_delete_guild(self, emoji, *, reason = None):
        """
        Deletes the given emoji.
        
        This method is a coroutine.
        
        Parameters
        ----------
        emoji : ``Emoji``, `(int, int)`
            The emoji to delete.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Will show up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            - If emoji is given as incorrect type.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id, emoji_id = get_emoji_guild_id_and_id(emoji)
        
        # Cannot delete partially loaded emoji.
        if not guild_id:
            return
        
        await self.api.emoji_delete_guild(guild_id, emoji_id, reason)
    
    
    emoji_create = emoji_create_guild
    emoji_edit = emoji_edit_guild
    emoji_delete = emoji_delete_guild
