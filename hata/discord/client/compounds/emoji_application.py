__all__ = ()

from scarletio import Compound

from ...application import Application
from ...http import DiscordApiClient

from ...emoji import Emoji
from ...emoji.emoji.utils import EMOJI_APPLICATION_FIELD_CONVERTERS
from ...http import DiscordApiClient
from ...payload_building import build_create_payload, build_edit_payload
from ...utils import image_to_base64

from ..request_helpers import get_emoji_and_id, get_emoji_id

from .interaction import _assert__application_id


class ClientCompoundEmojiApplicationEndpoints(Compound):
    
    api : DiscordApiClient
    application: Application
    
    async def emoji_get_application(self, emoji, *, force_update = False):
        """
        Requests the emoji by it's id at the given application.
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
        application_id = self.application.id
        assert _assert__application_id(application_id)
        
        emoji, emoji_id = get_emoji_and_id(emoji)
        
        if (not force_update) and (emoji is not None) and (self.application._has_cache_emoji_by_id(emoji_id)):
            return emoji
        
        emoji_data = await self.api.emoji_get_application(application_id, emoji_id)
        
        if (emoji is None):
            emoji = Emoji.from_data(emoji_data, 0)
        else:
            emoji._set_attributes(emoji_data, 0)
        
        self.application._add_cache_emoji(emoji)
        return emoji
    
    
    async def emoji_get_all_application(self):
        """
        Requests the given application's emojis.
        
        This method is a coroutine.
        
        Returns
        -------
        emojis : `list` of ``Emoji``
            The application's emojis.
        
        Raises
        ------
        TypeError
            - If `application`'s type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        application_id = self.application.id
        assert _assert__application_id(application_id)
        
        data = await self.api.emoji_get_all_application(application_id)
        emoji_datas = data.get('items', None)
        
        emojis = []
        if (emoji_datas is not None):
            for emoji_data in emoji_datas:
                emoji = Emoji.from_data(emoji_data, 0)
                self.application._add_cache_emoji(emoji)
                emojis.append(emoji)
        
        return emojis
    
    
    async def emoji_create_application(self, image, emoji_template = None, **keyword_parameters):
        """
        Creates an emoji at the client's application.
        
        This method is a coroutine.
        
        Parameters
        ----------
        image : `bytes-like`
            The emoji's icon. Up to 256 kB.
        
        emoji_template : `None`, ``Emoji`` = `None`, Optional
            Channel entity to use as a template.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters to create the emoji with.
        
        Other attributes
        ----------------
        name : `str`, Optional (Keyword only)
            The emoji's name. It's length can be between `2` and `32`.
        
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
        application_id = self.application.id
        assert _assert__application_id(application_id)
        
        data = build_create_payload(emoji_template, EMOJI_APPLICATION_FIELD_CONVERTERS, keyword_parameters)
        data['image'] = image_to_base64(image)
        emoji_data = await self.api.emoji_create_application(application_id, data)
        
        emoji = Emoji.from_data(emoji_data, 0)
        self.application._add_cache_emoji(emoji)
        return emoji
    
    
    async def emoji_edit_application(self, emoji, emoji_template = None, **keyword_parameters):
        """
        Edits the given (application) emoji.
        
        This method is a coroutine.
        
        Parameters
        ----------
        emoji : ``Emoji``, `(int, int)`
            The emoji to edit.
        
        emoji_template : `None`, ``Emoji`` = `None`, Optional
            A emoji to use as a template.
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters either to define the template, or to overwrite specific fields' values.
        
        Other attributes
        ----------------
        name : `str`, Optional (Keyword only)
            The emoji's name. It's length can be between `2` and `32`.
        
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
        """
        application_id = self.application.id
        assert _assert__application_id(application_id)
        
        emoji, emoji_id = get_emoji_and_id(emoji)
        
        data = build_edit_payload(emoji, emoji_template, EMOJI_APPLICATION_FIELD_CONVERTERS, keyword_parameters)
        
        if not data:
            return
        
        emoji_data = await self.api.emoji_edit_application(application_id, emoji_id, data)
        
        if emoji is None:
            emoji = Emoji.from_data(emoji_data, 0)
        else:
            emoji._set_attributes(emoji_data, 0)
        
        self.application._add_cache_emoji(emoji)
    
    
    async def emoji_delete_application(self, emoji):
        """
        Creates an emoji at the client's application.
        
        This method is a coroutine.
        
        Parameters
        ----------
        emoji : ``Emoji``, `int`
            The emoji to delete.
        
        Raises
        ------
        TypeError
            - If emoji is given as incorrect type.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        application_id = self.application.id
        assert _assert__application_id(application_id)
        
        emoji_id = get_emoji_id(emoji)
        await self.api.emoji_delete_application(application_id, emoji_id)
        
        self.application._delete_cache_emoji_by_id(emoji_id)
