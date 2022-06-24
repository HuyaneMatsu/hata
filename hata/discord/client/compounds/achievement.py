__all__ = ()

import reprlib

from scarletio import Compound, IgnoreCaseMultiValueDictionary
from scarletio.web_common.headers import AUTHORIZATION

from ....env import API_VERSION

from ...application import Application
from ...http import DiscordHTTPClient, VALID_ICON_MEDIA_TYPES_EXTENDED
from ...localizations.helpers import serializable_localized_dictionary_builder
from ...oauth2 import Achievement, OA2Access, UserOA2
from ...utils import get_image_media_type, image_to_base64
from ..request_helpers import get_achievement_and_id, get_achievement_id, get_user_id


class ClientCompoundAchievementEndpoints(Compound):
    
    application : Application
    http : DiscordHTTPClient
    
    
    async def achievement_get_all(self):
        """
        Requests all the achievements of the client's application and returns them.
        
        This method is a coroutine.
        
        Returns
        -------
        achievements : `list` of ``Achievement`` objects
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        data = await self.http.achievement_get_all(self.application.id)
        return [Achievement(achievement_data) for achievement_data in data]
    
    
    async def achievement_get(self, achievement):
        """
        Requests one of the client's achievements by it's id.
        
        This method is a coroutine.
        
        Parameters
        ----------
        achievement : ``Achievement``, `int`
            The achievement or it's identifier.
        
        Returns
        -------
        achievement : ``Achievement``
        
        Raises
        ------
        TypeError
            If `achievement` is not given as ``Achievement``, `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        achievement, achievement_id = get_achievement_and_id(achievement)
        data = await self.http.achievement_get(self.application.id, achievement_id)
        
        if achievement is None:
            achievement = Achievement(data)
        else:
            achievement._update_attributes(data)
        
        return achievement
    
    
    async def achievement_create(
        self, name, description, icon, *, description_localizations=None, name_localizations=None, secret=False,
        secure=False
    ):
        """
        Creates an achievement for the client's application and returns it.
        
        This method is a coroutine.
        
        Parameters
        ----------
        name : `str`
            The achievement's name.
        description : `str`
            The achievement's description.
        icon : `bytes-like`
            The achievement's icon. Can have `'jpg'`, `'png'`, `'webp'`, `'gif'` format.
        description_localizations : `None`, `dict` of (`str`, `str`) items = `None`, Optional (Keyword only)
            Localized descriptions of the achievement.
        name_localizations : `None`, `dict` of (`str`, `Any`) items = `None`, Optional (Keyword only)
            Localized names of the achievement.
        secret : `bool` = `False`, Optional (Keyword only)
            Secret achievements will *not* be shown to the user until they've unlocked them.
        secure : `bool` = `False`, Optional (Keyword only)
            Secure achievements can only be set via HTTP calls from your server, not by a game client using the SDK.
        
        Returns
        -------
        achievement : ``Achievement``
            The created achievement entity.
        
        Raises
        ------
        TypeError
            If `icon` was not passed as `bytes-like`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If the `icon`'s format is not any of the expected ones.
            - If `name` was not given as `str`.
            - If `description` was not given as `str`.
            - If `secret` was not given as `bool`.
            - If `secure` was not given as `bool`.
        """
        if __debug__:
            if not isinstance(name, str):
                raise AssertionError(
                    f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
                )
            
            if not isinstance(description, str):
                raise AssertionError(
                    f'`description` can be `str`, got {description.__class__.__name__}; {description!r}.'
                )
        
        if not isinstance(icon, (bytes, bytearray, memoryview)):
            raise TypeError(
                f'`icon` can be `bytes-like`, got {icon.__class__.__name__}; {reprlib.repr(icon)}.'
            )
        
        if __debug__:
            media_type = get_image_media_type(icon)
            if media_type not in VALID_ICON_MEDIA_TYPES_EXTENDED:
                raise AssertionError(
                    f'Invalid `icon` type for achievement: {media_type}; got {reprlib.repr(icon)}.'
                )
        
        icon_data = image_to_base64(icon)
        
        if __debug__:
            if not isinstance(secret, bool):
                raise AssertionError(
                    f'`secret` can be `bool`, got {secret.__class__.__name__}; {secret!r}.'
                )
            
            if not isinstance(secure, bool):
                raise AssertionError(
                    f'`secure` can be `bool`, got {secure.__class__.__name__}; {secure!r}.'
                )
        
        description_localizations = serializable_localized_dictionary_builder(
            description_localizations, 'description_localizations'
        )
        if description_localizations is None:
            description_localizations = {}
        
        name_localizations = serializable_localized_dictionary_builder(name_localizations, 'name_localizations')
        if name_localizations is None:
            name_localizations = {}
        
        data = {
            'secret': secret,
            'secure': secure,
            'icon': icon_data,
        }
        
        
        if API_VERSION >= 10:
            data['name'] = name
            data['description'] = description
            data['name_localizations'] = name_localizations
            data['description_localizations'] = description_localizations
        
        else:
            name_localizations['default'] = name
            data['name'] = name_localizations
            
            description_localizations['default'] = description
            data['description'] = description_localizations
        
        data = await self.http.achievement_create(self.application.id, data)
        
        return Achievement(data)
    
    
    async def achievement_edit(
        self, achievement, *, description=..., description_localizations=..., icon=..., name=...,
        name_localizations=...,  secret=..., secure=...
    ):
        """
        Edits the passed achievement with the specified parameters. All parameter is optional.
        
        This method is a coroutine.
        
        Parameters
        ----------
        achievement : ``Achievement``, `int`
            The achievement, what will be edited.
        description : `str`, Optional (Keyword only)
            The achievement's new description.
        description_localizations : `dict` of (`str`, `str`) items
            Localized descriptions of the achievement.
        icon : `bytes-like`, Optional (Keyword only)
            The achievement's new icon.
        name : `str`, Optional (Keyword only)
            The new name of the achievement.
        name_localizations : `dict` of (`str`, `str`) items
            Localized names of the achievement.
        secret : `bool`, Optional (Keyword only)
            The achievement's new secret value.
        secure : `bool`, Optional (Keyword only)
            The achievement's new secure value.
        
        Returns
        -------
        achievement : ``Achievement``
            After a successful edit, the passed achievement is updated and returned.
        
        Raises
        ------
        TypeError
            - If ``icon`` was not passed as `bytes-like`.
            - If `achievement` was not given neither as ``Achievement``, neither as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `name` was not given as `str`.
            - If `description` was not given as `str`.
            - If `secret` was not given as `bool`.
            - If `secure` was not given as `str`.
            - If `icon`'s format is not any of the expected ones.
        """
        achievement, achievement_id = get_achievement_and_id(achievement)
        
        data = {}
        

        if (icon is not ...):
            icon_type = icon.__class__
            if not isinstance(icon, (bytes, bytearray, memoryview)):
                raise TypeError(
                    f'`icon` can be `bytes-like`, got {icon_type.__name__}; {reprlib.repr(icon_type)}.'
                )
            
            if __debug__:
                media_type = get_image_media_type(icon)
                if media_type not in VALID_ICON_MEDIA_TYPES_EXTENDED:
                    raise ValueError(
                        f'Invalid `icon` type for achievement: {media_type}; got {reprlib.repr(icon_type)!r}.'
                    )
            
            data['icon'] = image_to_base64(icon)
        
        if (secret is not ...):
            if __debug__:
                if not isinstance(secret, bool):
                    raise AssertionError(
                        f'`secret` can be `bool`, got {secret.__class__.__name__}; {secret!r}.'
                    )
            
            data['secret'] = secret
        
        if (secure is not ...):
            if __debug__:
                if not isinstance(secret, bool):
                    raise AssertionError(
                        f'`secure` can be `bool`, got {secure.__class__.__name__}; {secure!r}.'
                    )
            
            data['secure'] = secure
        
        
        if __debug__:
            if (name is not ...):
                if not isinstance(name, str):
                    raise AssertionError(
                        f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
                    )
        
        if __debug__:
            if (description is not ...):
                if not isinstance(description, str):
                    raise AssertionError(
                        f'`description` can be `str`, got {description.__class__.__name__}; {description!r}.'
                    )
        
        if API_VERSION >= 10:
            if (description is not ...):
                data['description'] = description
            
            
                description_localizations = serializable_localized_dictionary_builder(
                    description_localizations,
                    'description_localizations',
                )
                if description_localizations is None:
                    description_localizations = {}
                
                data['description_localizations'] = description_localizations
            
            
            if (name is not ...):
                data['name'] = name
            
        
            if (name_localizations is not ...):
                name_localizations = serializable_localized_dictionary_builder(name_localizations, 'name_localizations')
                if name_localizations is None:
                    name_localizations = {}
            
                data['name_localizations'] = name_localizations
        
        else:
            if (
                (description is not ...) or
                (description_localizations is not ...) or
                (name is not ...) or
                (name_localizations is not ...)
            ):
                if (achievement is None):
                    achievement = await self.achievement_get(achievement_id)
                
                if (name is not ...) or (name_localizations is not ...):
                    if (name is ...):
                        name = achievement.name
                    
                    if (name_localizations is ...):
                        name_localizations = achievement.name_localizations
                        if name_localizations is None:
                            name_localizations = {}
                        else:
                            name_localizations = name_localizations.copy()
                    else:
                        name_localizations = serializable_localized_dictionary_builder(
                            name_localizations, 'name_localizations'
                        )
                        if name_localizations is None:
                            name_localizations = {}
                    
                    name_localizations['default'] = name
                    data['name'] = name_localizations
                
                if (description is not ...) or (description_localizations is not ...):
                    if (description is ...):
                        description = achievement.description
                    
                    if (description_localizations is ...):
                        description_localizations = achievement.description_localizations
                        if description_localizations is None:
                            description_localizations = {}
                        else:
                            description_localizations = description_localizations.copy()
                    
                    else:
                        description_localizations = serializable_localized_dictionary_builder(
                            description_localizations,
                            'description_localizations',
                        )
                        if description_localizations is None:
                            description_localizations = {}
                    
                    description_localizations['default'] = description
                    data['description'] = description_localizations
        
        
        data = await self.http.achievement_edit(self.application.id, achievement_id, data)
        if achievement is None:
            achievement = Achievement(data)
        else:
            achievement._update_attributes(data)
        
        return achievement
    
    
    async def achievement_delete(self, achievement):
        """
        Deletes the passed achievement.
        
        This method is a coroutine.
        
        Parameters
        ----------
        achievement : ``Achievement``, `int`
            The achievement to delete.
        
        Raises
        ------
        TypeError
            If `achievement` was not given neither as ``Achievement``, neither as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        achievement_id = get_achievement_id(achievement)
        
        await self.http.achievement_delete(self.application.id, achievement_id)
    
    
    async def user_achievement_get_all(self, access):
        """
        Requests the achievements of a user with it's oauth2 access.
        
        This method is a coroutine.
        
        Parameters
        ----------
        access : ``OA2Access``, ``UserOA2``, `str`.
            The access of the user, who's achievements will be requested.
        
        Returns
        -------
        achievements : `list` of ``Achievement`` objects
        
        Raises
        ------
        TypeError
            If `access` was not given neither as ``OA2Access``, ``UserOA2``  or `str`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        This endpoint is unintentionally documented and will never work. For reference:
        ``https://github.com/discordapp/discord-api-docs/issues/1230``.
        
        Always drops `DiscordException UNAUTHORIZED (401): 401: Unauthorized`.
        """
        if isinstance(access, (OA2Access, UserOA2)):
            access_token = access.access_token
        elif isinstance(access, str):
            access_token = access
        else:
            raise TypeError(
                f'`access` can be `{OA2Access.__name__}`, `{UserOA2.__name__}`, `str`, got '
                f'{access.__class__.__name__}; {access!r}.'
            )
        
        
        headers = IgnoreCaseMultiValueDictionary()
        headers[AUTHORIZATION] = f'Bearer {access_token}'
        
        data = await self.http.user_achievement_get_all(self.application.id, headers)
        return [Achievement(achievement_data) for achievement_data in data]
    
    
    async def user_achievement_update(self, user, achievement, percent_complete):
        """
        Updates the `user`'s achievement with the given percentage. The  achievement should be `secure`. This
        method only updates the achievement's percentage.
        
        This method is a coroutine.
        
        Parameters
        ----------
        user : ``ClientUserBase``, `int`
            The user, who's achievement will be updated.
        achievement : ``Achievement``, `int`
            The achievement, what's state will be updated
        percent_complete : `int`
            The completion percentage of the achievement.
        
        Raises
        ------
        TypeError
            - If `user` was not given neither as ``ClientUserBase`` nor `int`.
            - If `achievement` was not given neither as ``Achievement``, neither as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            - If `percent_complete` was not given as `int`.
            - If `percent_complete` is out of range [0:100].
        
        Notes
        -----
        This endpoint cannot grant achievement, but can it even update them?. For reference:
        ``https://github.com/discordapp/discord-api-docs/issues/1230``.
        
        Only secure updates are supported, if they are even.
        - When updating secure achievement: `DiscordException NOT FOUND (404), code=10029: Unknown Entitlement`
        - When updating non secure: `DiscordException FORBIDDEN (403), code=40001: Unauthorized`
        """
        user_id = get_user_id(user)
        
        achievement_id = get_achievement_id(achievement)
        
        if __debug__:
            if not isinstance(percent_complete, int):
                raise AssertionError(
                    f'`percent_complete` can be `int`, got {percent_complete.__class__.__name__}; {percent_complete!r}.'
                )
            
            if percent_complete < 0 or percent_complete > 100:
                raise AssertionError(
                    f'`percent_complete` is out of range [0:100], got {percent_complete!r}.'
                )
        
        data = {'percent_complete': percent_complete}
        await self.http.user_achievement_update(user_id, self.application.id, achievement_id, data)
