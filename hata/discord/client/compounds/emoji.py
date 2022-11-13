__all__ = ()

import re, warnings

from scarletio import Compound

from ...bases import maybe_snowflake, maybe_snowflake_pair
from ...core import EMOJIS, GUILDS
from ...emoji import Emoji
from ...http import DiscordHTTPClient
from ...role import Role
from ...utils import image_to_base64
from ..request_helpers import get_guild_and_id, get_guild_id, get_emoji_guild_id_and_id

_VALID_NAME_CHARS = re.compile('([0-9A-Za-z_]+)')


class ClientCompoundEmojiEndpoints(Compound):
    
    http : DiscordHTTPClient
    
    
    async def emoji_get(self, emoji, *deprecated_parameters, force_update=False):
        """
        Requests the emoji by it's id at the given guild. If the client's logging in is finished, then it should have
        it's every emoji loaded already.
        
        This method is a coroutine.
        
        Parameters
        ----------
        emoji : ``Emoji``, `tuple` (`int`, `int`) items
            The emoji, or 2 snowflake representing it.
        *deprecated_parameters : Additional parameters, Optional
            Old style parameter passing, as `guild` and `emoji`.
            
            Please pass either an ``Emoji``, or a snowflake pair (`guild_id`, `emoji_id`).
        
        force_update : `bool` = `False`, Optional (Keyword only)
            Whether the emoji should be requested even if it supposed to be up to date.
        
        Returns
        -------
        emoji : ``Emoji``
        
        Raises
        ------
        TypeError
            If `emoji` was not given as ``Emoji``, `tuple` (`int`, `int`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        # Check for old-style deprecated
        if deprecated_parameters:
            if len(deprecated_parameters) > 1:
                raise TypeError(
                    f'`{self.__class__.__name__}.emoji_get` accepts up to `2` positional parameters, got '
                    f'{len(deprecated_parameters) + 1}.'
                )
            
            warnings.warn(
                (
                    f'2nd parameter of `{self.__class__.__name__}.emoji_get` is deprecated and will be '
                    f'removed in 2022 Jun. Please pass just an `{Emoji.__name__}` or a pair of snowflake.'
                ),
                FutureWarning,
                stacklevel = 2,
            )
            
            guild, emoji, = emoji, *deprecated_parameters
            
            guild_id = get_guild_id(guild)
            
            if isinstance(emoji, Emoji):
                emoji_id = emoji.id
            else:
                emoji_id = maybe_snowflake(emoji)
                if emoji_id is None:
                    raise TypeError(
                        f'`emoji` can be `{Emoji.__name__}`, `int`, got {emoji.__class__.__name__}; {emoji!r}.'
                    )
                
                emoji = EMOJIS.get(emoji_id, None)
        
        else:
            if isinstance(emoji, Emoji):
                guild_id = emoji.guild_id
                emoji_id = emoji.id
            else:
                snowflake_pair = maybe_snowflake_pair(emoji)
                if snowflake_pair is None:
                    raise TypeError(
                        f'`emoji` can be `{Emoji.__name__}`, `tuple` (`int`, `int`), '
                        f'got {emoji.__class__.__name__}; {emoji!r}.'
                    )
                
                guild_id, emoji_id = snowflake_pair
                emoji = EMOJIS.get(emoji_id, None)
        
        
        # If the emoji has no linked guild, we cannot request it, so we return instantly.
        if not guild_id:
            # Create empty emoji instead of returning `None` to stop expected errors
            if emoji is None:
                emoji = Emoji.precreate(emoji_id)
            
            return emoji
        
        if (emoji is not None) and (not emoji.partial) and (not force_update):
            return emoji
        
        emoji_data = await self.http.emoji_get(guild_id, emoji_id)
        
        if (emoji is None):
            emoji = Emoji(emoji_data, guild_id)
        else:
            emoji._set_attributes(emoji_data, guild_id)
        
        return emoji
    
    
    async def emoji_guild_get_all(self, guild):
        """
        Syncs the given guild's emojis with the wrapper.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, what's emojis will be synced.
        
        Returns
        -------
        emojis : `list` of ``Emoji``
            The guild's emojis.
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as ``Guild`` nor as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild, guild_id = get_guild_and_id(guild)
        
        emoji_datas = await self.http.emoji_guild_get_all(guild_id)
        
        if guild is None:
            # Do not create a partial guild, because it would have been garbage collected after leaving the function
            # anyways
            guild = GUILDS.get(guild_id, None)
        
        if guild is None:
            emojis = [Emoji(emoji_data, guild_id) for emoji_data in emoji_datas]
        else:
            guild._sync_emojis(emoji_datas)
            emojis = list(guild.emojis.values())
        
        return emojis
    
    
    async def guild_sync_emojis(self, guild):
        """
        Deprecated and will be removed in 2022 Jun. Please use ``.emoji_guild_get_all`` instead.
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.guild_sync_emojis` is deprecated and will be '
                f'removed in 2022 Jun. Please use `.emoji_guild_get_all` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        return await self.emoji_guild_get_all(guild)
    
    
    async def emoji_create(self, guild, name, image, *, roles=None, reason = None):
        """
        Creates an emoji at the given guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, where the emoji will be created.
        name : `str`
            The emoji's name. It's length can be between `2` and `32`.
        image : `bytes-like`
            The emoji's icon.
        roles : `None`, (`list`, `set`, `tuple`) of (``Role``, `int`) = `None`, Optional (Keyword only)
            Whether the created emoji should be limited only to users with any of the specified roles.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Will show up at the guild's audit logs.
        
        Returns
        -------
        emoji : ``Emoji``
            The created emoji.
        
        Raises
        ------
        TypeError
            If `guild` was not given neither as ``Guild`` nor as `int`.
            If `roles` contains a non ``Role``, `int` element.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `name` was not given as `str`.
            - If `name` length is out of the expected range [1:32].
            - If `roles` was not given neither as `None`, `list`, `tuple`, `set`.
        Notes
        -----
        Only some characters can be in the emoji's name, so every other character is filtered out.
        """
        guild_id = get_guild_id(guild)
        
        if __debug__:
            if not isinstance(name, str):
                raise AssertionError(
                    f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
                )
        
        name = ''.join(_VALID_NAME_CHARS.findall(name))
        
        if __debug__:
            name_length = len(name)
            if name_length < 2 or name_length > 32:
                raise AssertionError(
                    f'`name` length can be in range [2:32], got {name_length!r}; {name!r}.'
                )
        
        role_ids = set()
        if (roles is not None):
            if __debug__:
                if not isinstance(roles, (list, set, tuple)):
                    raise AssertionError(
                        f'`roles` can be `None`, `list`, `set`, `tuple`, got {roles.__class__.__name__}; {roles!r}.'
                    )
            
            for role in roles:
                if isinstance(role, Role):
                    role_id = role.id
                else:
                    role_id = maybe_snowflake(role)
                    if role_id is None:
                        raise TypeError(
                            f'`roles` contains not `{Role.__name__}`, `int` element, '
                            f'got {role.__class__.__name__}; {role!r}; roles={roles!r}.'
                        )
                
                role_ids.add(role_id)
            
        image = image_to_base64(image)
        
        data = {
            'name': name,
            'image': image,
            'roles': role_ids
        }
        
        data = await self.http.emoji_create(guild_id, data, reason)
        
        emoji = Emoji(data, guild_id)
        emoji.user = self
        return emoji
    
    
    async def emoji_delete(self, emoji, *, reason = None):
        """
        Deletes the given emoji.
        
        This method is a coroutine.
        
        Parameters
        ----------
        emoji : ``Emoji``
            The emoji to delete.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Will show up at the respective guild's audit logs.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If `emoji` was not given as ``Emoji``.
        """
        guild_id, emoji_id = get_emoji_guild_id_and_id(emoji)
        
        # Cannot delete partially loaded emoji.
        if guild_id is None:
            return
        
        await self.http.emoji_delete(guild_id, emoji_id, reason = reason)
    
    
    async def emoji_edit(self, emoji, *, name=..., roles=..., reason = None):
        """
        Edits the given emoji.
        
        This method is a coroutine.
        
        Parameters
        ----------
        emoji : ``Emoji``, `tuple` (`int`, `int`)
            The emoji to edit.
        name : `str`, Optional (Keyword only)
            The emoji's new name. It's length can be in range [2:32].
        roles : `None`, (`list`, `set`, `tuple`) of (``Role``, `int`), Optional (Keyword only)
            The roles to what is the role limited. By passing it as `None`, or as an empty `list` you can remove the
            current ones.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Shows up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            - If `roles` contains a non ``Role``, `int` element.
            - If `emoji` is not ``Emoji``, `tuple` (`int`, `int`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `name` was not given as `str`.
            - If `name` length is out of the expected range [1:32].
            - If `roles` was not given neither as `None`, `list`, `tuple`, `set`.
        """
        guild_id, emoji_id = get_emoji_guild_id_and_id(emoji)
        
        # Cannot edit partially loaded emojis.
        if not guild_id:
            return
        
        data = {}
        
        # name is not a required parameter anymore, we can edit the emoji normally.
        if (name is not ...):
            if __debug__:
                if not isinstance(name, str):
                    raise AssertionError(
                        f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
                    )
            
            name = ''.join(_VALID_NAME_CHARS.findall(name))
            
            if __debug__:
                name_length = len(name)
                if name_length < 2 or name_length > 32:
                    raise AssertionError(
                        f'`name` length can be in range [2:32], got {name_length!r}; {name!r}.'
                    )
            
            data['name'] = name
        
        
        if (roles is not ...):
            role_ids = set()
            if (roles is not None):
                if __debug__:
                    if not isinstance(roles, (list, set, tuple)):
                        raise AssertionError(
                            f'`roles` can be `None`, `list`, `set`, `tuple`, got '
                            f'{roles.__class__.__name__}; {roles!r}.'
                        )
                
                for role in roles:
                    if isinstance(role, Role):
                        role_id = role.id
                    else:
                        role_id = maybe_snowflake(role)
                        if role_id is None:
                            raise TypeError(
                                f'`roles` contains not `{Role.__name__}`, `int` element, got '
                                f'{role.__class__.__name__}; {role!r}; roles={roles!r}.'
                            )
                    
                    role_ids.add(role_id)
            
            data['roles'] = role_ids
        
        
        await self.http.emoji_edit(guild_id, emoji_id, data, reason)
