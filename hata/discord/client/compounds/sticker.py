__all__ = ()

import reprlib, warnings

from scarletio import Compound
from scarletio.web_common import Formdata

from ...bases import maybe_snowflake_pair
from ...core import  GUILDS, STICKERS
from ...emoji import Emoji
from ...http import DiscordHTTPClient, VALID_STICKER_IMAGE_MEDIA_TYPES
from ...sticker import Sticker, StickerPack
from ...utils import MEDIA_TYPE_TO_EXTENSION, get_image_media_type

from ..functionality_helpers import ForceUpdateCache
from ..request_helpers import get_guild_and_id, get_guild_id, get_sticker_and_id, get_sticker_pack_and_id


STICKER_PACK_CACHE = ForceUpdateCache()


def _handle_emoji_representation_parameter_deprecation(instance, tags, emoji_representation):
    """
    Handles the deprecation of the `emoji_representation` parameter.
    
    Parameters
    ----------
    instance : ``Client``
        Client instance used for raising correct warning.
    tags : ``Emoji``, `str`, `iterable` of `str`
        The tags of the sticker.
    emoji_representation : ``Emoji``, `str`, `iterable` of `str`
        The tags of the sticker.
    
    Returns
    -------
    tags : ``Emoji``, `str`, `iterable` of `str`
    """
    if emoji_representation is not ...:
        warnings.warn(
            (
                f'`{instance.__class__.__name__}.sticker_guild_create`\'s `emoji_representation` is deprecated '
                f'and will be removed in 2023 Marc. '
                f'Please use `tags` instead.'
            ),
            FutureWarning,
            stacklevel = 3,
        )
        
        tags = emoji_representation
    
    return tags


def _validate_tags(tags):
    """
    Validates the given tags value.
    
    Parameters
    ----------
    tags : ``Emoji``, `str`, `iterable` of `str`
        The tags of the sticker.
    
    Returns
    -------
    tags : `set` of `str`
        The validated tags.
    
    Raises
    ------
    TypeError
        - If `tags`'s type is incorrect.
    """
    validated_tags = set()
    
    if isinstance(tags, str):
        validated_tags.add(tags)
    
    elif isinstance(tags, Emoji):
        validated_tags.add(tags.name)
    
    elif (getattr(tags, '__iter__', None) is not None):
        for tag in tags:
            if not isinstance(tag, str):
                raise TypeError(
                    f'`tags` can have `str` elements, got {tag.__class__.__name__}; {tag!r}; tags = {tags!r}'
                )
            validated_tags.add(tag)
    
    else:
        raise TypeError(
            f'`tags` can be `str`, `{Emoji.__name__}`, `iterable` of `str`, got {tags.__class__.__name__}; {tags!r}.'
        )
    
    return validated_tags


class ClientCompoundStickerEndpoints(Compound):
    
    http : DiscordHTTPClient
    
    
    async def sticker_get(self, sticker, *, force_update=False):
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
        
        data = await self.http.sticker_get(sticker_id)
        if (sticker is None):
            sticker = Sticker(data)
        else:
            sticker._update_from_partial(data)
        
        return sticker
    
    
    async def sticker_pack_get(self, sticker_pack, *, force_update=False):
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
            sticker_pack_data = await self.http.sticker_pack_get(sticker_pack_id)
            sticker_pack = StickerPack._create_and_update(sticker_pack_data)
        
        return sticker_pack
    
    
    async def sticker_pack_get_all(self, *, force_update=False):
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
            data = await self.http.sticker_pack_get_all()
            sticker_pack_datas = data['sticker_packs'] # Discord pls.
            if force_update:
                sticker_packs = [StickerPack._create_and_update(sticker_pack_data) for sticker_pack_data in
                    sticker_pack_datas]
            else:
                sticker_packs = [StickerPack(sticker_pack_data) for sticker_pack_data in sticker_pack_datas]
            
            STICKER_PACK_CACHE.set(sticker_packs)
        
        else:
            sticker_packs = STICKER_PACK_CACHE.value
        
        return sticker_packs
    
    
    async def sticker_guild_get(self, sticker, *deprecated_parameters, force_update=False):
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
        if deprecated_parameters:
            if len(deprecated_parameters) > 1:
                raise TypeError(
                    f'`{self.__class__.__name__}.sticker_guild_get` accepts up to `2` positional parameters, got '
                    f'{len(deprecated_parameters) + 1}.'
                )
            
            warnings.warn(
                (
                    f'2nd parameter of `{self.__class__.__name__}.sticker_guild_get` is deprecated and will be '
                    f'removed in 2022 Jun. Please pass just an `{Sticker.__name__}` or a pair of snowflake.'
                ),
                FutureWarning,
                stacklevel = 2,
            )
            
            guild, sticker, = sticker, *deprecated_parameters
            sticker, sticker_id = get_sticker_and_id(sticker)
            guild_id = get_guild_id(guild)
            
        else:
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
        
        data = await self.http.sticker_guild_get(guild_id, sticker_id)
        if (sticker is None):
            sticker = Sticker(data)
        else:
            sticker._update_from_partial(data)
        
        return sticker
    
    
    async def sticker_guild_create(
        self, guild, name, image, tags = ..., description = None, *, emoji_representation = ..., reason = None
    ):
        """
        Creates a sticker in the guild.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild : ``Guild``, `int`
            The guild to create the sticker in.
        name : `str`
            The sticker's name. It's length can be in range [2:32]
        tags : ``Emoji``, `str`, `iterable` of `str`
            The tags of the sticker.
        image : `bytes-like`
            The sticker's image in bytes.
        description : `None`, `str` = `None`, Optional
            The sticker's representation. It's length can be in range [0:100]
        reason : `None`, `str` = `None`, Optional (Keyword only)
            Will show up at the respective guild's audit logs.
        
        Returns
        -------
        sticker : ``Sticker``
            The created sticker.
        
        Raises
        ------
        TypeError
            - If `str` is neither `str` nor ``Emoji``, `iterable` of `str`.
            - If `guild` is neither ``Guild`` nor `int`.
        ValueError
            If `image`s media type is neither `image/png` nor `application/json`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `name` is not `str`.
            - If `name`'s length is out of range [2:32].
            - If `description` is neither `None`, `str`.
            - If `description`'s length is out of range [0:100].
        """
        # Handle deprecation.
        tags = _handle_emoji_representation_parameter_deprecation(self, tags, emoji_representation)
        if tags is ...:
            raise TypeError('`tags` parameter is required.')
        
        guild_id = get_guild_id(guild)
        
        if __debug__:
            if not isinstance(name, str):
                raise AssertionError(
                    f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
                )
        
            name_length = len(name)
            if (name_length < 2) or (name_length > 32):
                raise AssertionError(
                    f'`name` length can be in range [2:32], got {name_length!r}; {name!r}.'
                )
        
        if __debug__:
            if (description is not None):
                if (not isinstance(description, str)):
                    raise AssertionError(
                        f'`description` can be `str`, got {description.__class__.__name__}; {description!r}.'
                    )
                
                description_length = len(description)
                if (description_length > 100):
                    raise AssertionError(
                        f'`description` length can be in range [0:100], got {description_length!r}; {description!r}.'
                    )
        
        if (description is not None) and (not description):
            description = None
        
        tags = _validate_tags(tags)
        
        if __debug__:
            if not isinstance(image, (bytes, bytearray, memoryview)):
                raise TypeError(
                    f'`image` can be `None`, `bytes-like`, got {image.__class__.__name__}; {reprlib.repr(image)}.'
                )
        
        media_type = get_image_media_type(image)
        if media_type not in VALID_STICKER_IMAGE_MEDIA_TYPES:
            raise ValueError(
                f'Invalid `image` type: {media_type}, got {reprlib.repr(image)}.'
            )
        
        extension = MEDIA_TYPE_TO_EXTENSION[media_type]
        
        form_data = Formdata()
        form_data.add_field('name', name)
        
        if (description is not None):
            form_data.add_field('description', description)
        else:
            # If no description is given Discord drops back an unrelated error
            form_data.add_field('description', '')
        
        form_data.add_field('tags', ', '.join(tags))
        
        form_data.add_field('file', image, filename=f'file.{extension}', content_type=media_type)
        
        
        sticker_data = await self.http.sticker_guild_create(guild_id, form_data, reason)
        
        return Sticker(sticker_data)
    
    
    async def sticker_guild_edit(
        self, sticker, *, name=..., tags = ..., emoji_representation=..., description = ..., reason = None
    ):
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
            - If `sticker` is neither ``Sticker``, nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - Non guild bound sticker cannot be edited.
            - If `name` is not `str`.
            - If `name`'s length is out of range [2:32].
            - If `description` is neither `None`, `str`.
            - If `description`'s length is out of range [0:100].
        """
        # Handle deprecation.
        tags = _handle_emoji_representation_parameter_deprecation(self, tags, emoji_representation)
        
        sticker = await self.sticker_get(sticker)
        
        if __debug__:
            if not sticker.guild_id:
                raise AssertionError(
                    f'Non guild bound sticker cannot be edited, got {sticker!r}.'
                )
        
        if (name is ...):
            name = sticker.name
        else:
            if __debug__:
                if not isinstance(name, str):
                    raise AssertionError(
                        f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
                    )
            
                name_length = len(name)
                if (name_length < 2) or (name_length > 32):
                    raise AssertionError(
                        f'`name` length can be in range [2:32], got {name_length!r}; {name!r}.'
                    )
        
        if (tags is ...):
            tags = sticker.tags
        else:
            tags = _validate_tags(tags)
        
        if (description is ...):
            description = sticker.description
        else:
            if __debug__:
                if (description is not None):
                    if (not isinstance(description, str)):
                        raise AssertionError(
                            f'`description` can be `None`, `str`, got {description.__class__.__name__}; '
                            f'{description!r}.'
                        )
            
                    description_length = len(description)
                    if (description_length > 100):
                        raise AssertionError(
                            f'`description` length can be in range [0:100], got {description_length!r}; '
                            f'{description!r}.'
                        )
            
            if (description is None):
                description = ''
        
        data = {
            'name': name,
            'tags': ', '.join(tags),
            'description': description,
        }
        
        await self.http.sticker_guild_edit(sticker.guild_id, sticker.id, data, reason)
    
    
    async def sticker_guild_delete(self, sticker, *, reason = None):
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
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            Non guild bound sticker cannot be edited.
        """
        sticker = await self.sticker_get(sticker)
        
        if __debug__:
            if not sticker.guild_id:
                raise AssertionError(
                    f'Non guild bound sticker cannot be edited, got {sticker!r}.'
                )
        
        await self.http.sticker_guild_delete(sticker.guild_id, sticker.id, reason)
    
    
    
    async def sticker_guild_get_all(self, guild):
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
        
        sticker_datas = await self.http.sticker_guild_get_all(guild_id)
        
        if guild is None:
            # Do not create a partial guild, because it would have been garbage collected after leaving the function
            # anyways
            guild = GUILDS.get(guild_id, None)
        
        if guild is None:
            stickers = [Sticker(sticker_data) for sticker_data in sticker_datas]
        else:
            guild._sync_stickers(sticker_datas)
            stickers = [*guild.stickers.values()]
        
        return stickers
    
    
    async def guild_sync_stickers(self, guild):
        """
        Deprecated and will be removed in 2022 Jun. Please use ``.sticker_guild_get_all`` instead.
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.guild_sync_stickers` is deprecated and will be '
                f'removed in 2022 Jun. Please use `.sticker_guild_get_all` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        
        return await self.sticker_guild_get_all(guild)
