__all__ = ()

from scarletio import Compound

from ...application import Application, EULA
from ...bases import maybe_snowflake
from ...channel import Channel
from ...core import EULAS
from ...embed import EmbedImage
from ...http import DiscordHTTPClient, is_media_url
from ...message import Attachment

from ..request_helpers import get_channel_id
from ..utils import Typer


class ClientCompoundMiscellaneousEndpoints(Compound):
    
    http : DiscordHTTPClient
    

    async def download_attachment(self, attachment):
        """
        Downloads an attachment object's file. This method always prefers the proxy url of the attachment if applicable.
        
        This method is a coroutine.
        
        Parameters
        ----------
        attachment : ``Attachment``, ``EmbedImage``
            The attachment object what's file will be requested.
        
        Returns
        -------
        response_data : `bytes`
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        AssertionError
            If `attachment` was not given as ``Attachment`` nor ``EmbedImage``.
        """
        if __debug__:
            if not isinstance(attachment, (Attachment, EmbedImage)):
                raise AssertionError(
                    f'`attachment` can be `{Attachment.__name__}`, `{EmbedImage.__name__}`, got '
                    f'{attachment.__class__.__name__}; {attachment!r}.'
                )
        
        url = attachment.proxy_url
        if (url is None) or is_media_url(url):
           url = attachment.url
        
        async with self.http.get(url) as response:
            return (await response.read())
    

    async def eula_get(self, eula):
        """
        Requests the eula with the given id.
        
        This method is a coroutine.
        
        Parameters
        ----------
        eula : `int`
            The `id` of the eula to request.

        Returns
        -------
        eula : ``EULA``
        
        Raises
        ------
        TypeError
            If `eula` was not given neither as ``EULA`` not as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        if isinstance(eula, EULA):
            eula_id = eula.id
        
        else:
            eula_id = maybe_snowflake(eula)
            if eula_id is None:
                raise TypeError(
                    f'`eula` can be `{EULA.__name__}`, `int`, got {eula.__class__.__name__}; {eula!r}.'
                )
            
            eula = EULAS.get(eula_id, None)
        
        
        eula_data = await self.http.eula_get(eula_id)
        if eula is None:
            eula = EULA.from_data(eula_data)
        else:
            eula._update_attributes(eula_data)
        
        return eula
    
    
    async def application_get_all_detectable(self):
        """
        Requests the detectable applications
        
        This method is a coroutine.
        
        Returns
        -------
        applications : `list` of ``Application``
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        applications_data = await self.http.application_get_all_detectable()
        return [Application.from_data_detectable(application_data) for application_data in applications_data]
    
    
    async def typing(self, channel):
        """
        Sends a typing event to the given channel.
        
        This method is a coroutine.
        
        Parameters
        ----------
        channel : ``Channel``, `int`
            The channel where typing will be triggered.
        
        Raises
        ------
        TypeError
            If `channel` was not given neither as ``Channel`` nor `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        The client will be shown up as typing for 8 seconds, or till it sends a message at the respective channel.
        """
        channel_id = get_channel_id(channel, Channel.is_in_group_textual)
        
        await self.http.typing(channel_id)
    
    
    def keep_typing(self, channel, timeout=300.0):
        """
        Returns a context manager which will keep sending typing events at the channel. Can be used to indicate that
        the bot is working.
        
        Parameters
        ----------
        channel ``Channel``, `int`
            The channel where typing will be triggered.
        timeout : `float` = `300.0`, Optional
            The maximal duration for the ``Typer`` to keep typing.
        
        Returns
        -------
        typer : ``Typer``
        
        Raises
        ------
        TypeError
            If `channel` was not given neither as ``Channel`` nor `int`.
        
        Examples
        --------
        ```py
        with client.keep_typing(channel):
            # Do some things
            await client.message_create(channel, 'Ayaya')
        ```
        """
        channel_id = get_channel_id(channel, Channel.is_in_group_textual)
        
        return Typer(self, channel_id, timeout)
