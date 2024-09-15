__all__ = ()

from reprlib import repr as short_repr

from scarletio import Compound
from scarletio.web_common import FormData

from ...bases import maybe_snowflake_pair
from ...core import GUILDS, STICKERS
from ...http import DiscordApiClient, VALID_STICKER_IMAGE_MEDIA_TYPES
from ...sticker import Sticker, StickerPack, StickerType
from ...sticker.sticker.fields import (
    put_description_into, put_name_into, put_tags_into, validate_description, validate_name, validate_tags
)
from ...utils import MEDIA_TYPE_TO_EXTENSION, get_image_media_type

from ..functionality_helpers import ForceUpdateCache
from ..request_helpers import get_guild_and_id, get_guild_id, get_sticker_and_id, get_sticker_pack_and_id


STICKER_PACK_CACHE = ForceUpdateCache()


class ClientCompoundStickerEndpoints(Compound):
    
    api : DiscordApiClient
    
    
    async def sticker_get(self, sticker, *, force_update = False):
        """
        Gets an sticker by it's id. If the sticker is already loaded updates it.
        
        This method is a coroutine.
        
        Parameters
        ----------
        sticker : ``Sticker``, `int`
            The sticker, who will be requested.
        force_update : `bool` = `False`, Optional (Keyword only)
            Whether the sticker should be requested even if it supposed to be up to date.
        
        Returns
        -------
        sticker : ``Sticker``
        
        Raises
        ------
        TypeError
            If `sticker` was not given neither as ``Sticker``, neither as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        TypeError
            If `sticker` was not given as ``Sticker``, nor as `int`.
        """
        sticker, sticker_id = get_sticker_and_id(sticker)
        if (sticker is not None) and (not sticker.partial) and (not force_update):
            return sticker
        
        data = await self.api.sticker_get(sticker_id)
        if (sticker is None):
            sticker = Sticker.from_data(data)
        else:
            sticker._set_attributes(data)
        
        return sticker
    
    
    async def sticker_pack_get(self, sticker_pack, *, force_update = False):
        """
        Gets the sticker packs. If the sticker-packs are already loaded, updates them.
        
        This method is a coroutine.
        
        Parameters
        ----------
        sticker_pack : ``StickerPack``, `int`
            The sticker pack' identifier.
        force_update : `bool` = `False`, Optional (Keyword only)
            Whether the sticker-pack should be requested even if it supposed to be up to date.
        
        Returns
        -------
        sticker_packs : `list` of ``StickerPack``
        
        Raises
        ------
        TypeError
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        sticker_pack, sticker_pack_id = get_sticker_pack_and_id(sticker_pack)
        
        if (sticker_pack is None) or force_update:
            sticker_pack_data = await self.api.sticker_pack_get(sticker_pack_id)
            sticker_pack = StickerPack.from_data(sticker_pack_data, force_update = True)
        
        return sticker_pack
    
    
    async def sticker_pack_get_all(self, *, force_update = False):
        """
        Gets the sticker packs. If the sticker-packs are already loaded, updates them.
        
        This method is a coroutine.
        
        Parameters
        ----------
        force_update : `bool` = `False`, Optional (Keyword only)
            Whether the sticker-packs should be requested even if it supposed to be up to date.
        
        Returns
        -------
        sticker_packs : `list` of ``StickerPack``
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        if force_update or (not STICKER_PACK_CACHE.synced):
            data = await self.api.sticker_pack_get_all()
            sticker_pack_datas = data['sticker_packs'] # Discord pls.
            sticker_packs = [
                StickerPack._create_and_update(sticker_pack_data, force_update = force_update)
                for sticker_pack_data in sticker_pack_datas
            ]
            
            STICKER_PACK_CACHE.set(sticker_packs)
        
        else:
            sticker_packs = STICKER_PACK_CACHE.value
        
        return sticker_packs
    
    
    async def sticker_get_guild(self, sticker, *, force_update = False):
        """
        Gets the specified sticker from the respective guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        sticker : ``Sticker``, `tuple`, (`int`, `int`)
            The sticker to get.
        force_update : `bool` = `False`, Optional (Keyword only)
            Whether the sticker should be requested even if it supposed to be up to date.
        
        Raises
        ------
        TypeError
            If `sticker` is not ``Sticker``, `tuple` (`int`, `int`).
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        if isinstance(sticker, Sticker):
            guild_id = sticker.guild_id
            sticker_id = sticker.id
        else:
            snowflake_pair = maybe_snowflake_pair(sticker)
            if snowflake_pair is None:
                raise TypeError(
                    f'`sticker` can be `{Sticker.__name__}`, `tuple` (`int`, `int`), '
                    f'got {sticker.__class__.__name__}; {sticker!r}.'
                )
            
            guild_id, sticker_id = snowflake_pair
            sticker = STICKERS.get(sticker_id, None)
        
        if (sticker is not None) and (not sticker.partial) and (not force_update):
            return sticker
        
        data = await self.api.sticker_get_guild(guild_id, sticker_id)
        if (sticker is None):
            sticker = Sticker.from_data(data)
        else:
            sticker._set_attributes(data)
        
        return sticker
    
    
    async def sticker_create(self, guild, name, image, tags = None, description = None, *, reason = None):
        """
        Creates a sticker in the guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild to create the sticker in.
        name : `str`
            The sticker's name.
        tags : `None`, `str`, `iterable` of `str`
            The tags of the sticker.
        image : `bytes-like`
            The sticker's image in bytes.
        description : `None`, `str` = `None`, Optional
            The sticker's representation.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Will show up at the respective guild's audit logs.
        
        Returns
        -------
        sticker : ``Sticker``
            The created sticker.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        ValueError
            If `image`s media type is neither `image/png` nor `application/json`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        guild_id = get_guild_id(guild)
        
        description = validate_description(description)
        name = validate_name(name)
        tags = validate_tags(tags)
        
        if not isinstance(image, (bytes, bytearray, memoryview)):
            raise TypeError(
                f'`image` can be `None`, `bytes-like`, got {image.__class__.__name__}; {short_repr(image)}.'
            )
        
        media_type = get_image_media_type(image)
        if media_type not in VALID_STICKER_IMAGE_MEDIA_TYPES:
            raise ValueError(
                f'Invalid `image` type: {media_type}, got {short_repr(image)}.'
            )
        
        extension = MEDIA_TYPE_TO_EXTENSION[media_type]
        
        form_data = FormData()
        form_data.add_field('name', name)
        # If no description is given Discord drops back an unrelated error
        form_data.add_field('description', '' if description is None else description)
        form_data.add_field('tags', '' if tags is None else ', '.join(tags))
        form_data.add_field('file', image, file_name = f'file.{extension}', content_type = media_type)
        
        sticker_data = await self.api.sticker_create(guild_id, form_data, reason)
        
        return Sticker.from_data(sticker_data)
    
    
    async def sticker_edit(self, sticker, *, name = ..., tags = ..., description = ..., reason = None):
        """
        Edits the given guild bound sticker,
        
        This method is a coroutine.
        
        Parameters
        ----------
        sticker : ``Sticker``, `int`
            The respective sticker.
        name : `str`, Optional (keyword only)
            New name of the sticker. It's length can be in range [2:32].
        tags : `str`, ``Emoji``, `iterable` of `str`, Optional (keyword Only)
            The new emoji representation of the sticker. Used as a tag for the sticker.
        description : `None`, `str`, Optional (Keyword only)
            New description for the sticker. It's length can be in range [0:100].
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Will show up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
            - Standard stickers cannot be edited.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        sticker = await self.sticker_get(sticker)
        
        
        if sticker.type is StickerType.standard:
            raise ValueError(
                f'Standard sticker cannot be edited, got {sticker!r}.'
            )
        
        if (name is ...):
            name = sticker.name
        else:
            name = validate_name(name)
        
        if (tags is ...):
            tags = sticker.tags
        else:
            tags = validate_tags(tags)
        
        if (description is ...):
            description = sticker.description
        else:
            description = validate_description(description)
        
        data = {}
        put_description_into(description, data, True)
        put_name_into(name, data, True)
        put_tags_into(tags, data, True)
        
        await self.api.sticker_edit(sticker.guild_id, sticker.id, data, reason)
    
    
    async def sticker_delete(self, sticker, *, reason = None):
        """
        Deletes the sticker.
        
        This method is a coroutine.
        
        Parameters
        ----------
        sticker : ``Sticker``, `int`
            The sticker to delete.
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Will show up at the respective guild's audit logs.
        
        Raises
        ------
        TypeError
            If `sticker` is neither ``Sticker``, nor `int`.
        ValueError
            - Standard stickers cannot be deleted.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        sticker = await self.sticker_get(sticker)
        
        if sticker.type is StickerType.standard:
            raise ValueError(
                f'Standard sticker cannot be deleted, got {sticker!r}.'
            )
        
        await self.api.sticker_delete(sticker.guild_id, sticker.id, reason)
    
    
    async def sticker_get_all_guild(self, guild):
        """
        Syncs the given guild's stickers with the wrapper.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild, what's stickers will be synced.
        
        Returns
        -------
        stickers : `list` of ``Sticker``
            The guild's stickers.
        
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
        
        sticker_datas = await self.api.sticker_get_all_guild(guild_id)
        
        if guild is None:
            # Do not create a partial guild, because it would have been garbage collected after leaving the function
            # anyways
            guild = GUILDS.get(guild_id, None)
        
        if guild is None:
            stickers = [Sticker.from_data(sticker_data) for sticker_data in sticker_datas]
        else:
            guild._update_stickers(sticker_datas)
            stickers = [*guild.stickers.values()]
        
        return stickers
