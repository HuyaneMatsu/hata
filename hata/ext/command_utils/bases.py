__all__ = (
    'GUI_STATE_CANCELLED', 'GUI_STATE_CANCELLING', 'GUI_STATE_READY', 'GUI_STATE_SWITCHING_CTX',
    'GUI_STATE_SWITCHING_PAGE', 'PaginationBase'
)

from scarletio import CancelledError, Task

from ...discord.core import KOKORO
from ...discord.exceptions import DiscordException, ERROR_CODES


GUI_STATE_READY = 0
GUI_STATE_SWITCHING_PAGE = 1
GUI_STATE_CANCELLING = 2
GUI_STATE_CANCELLED = 3
GUI_STATE_SWITCHING_CTX = 4

GUI_STATE_VALUE_TO_NAME = {
    GUI_STATE_READY : 'ready',
    GUI_STATE_SWITCHING_PAGE : 'switching_page',
    GUI_STATE_CANCELLING : 'cancelling',
    GUI_STATE_CANCELLED : 'cancelled',
    GUI_STATE_SWITCHING_CTX : 'switching_context',
}

class PaginationBase:
    """
    Base class for pagination like objects.
    
    Attributes
    ----------
    _canceller : `None`, `Function`
        The function called when the ``Pagination`` is cancelled or when it expires. This is a onetime use and after
        it was used, is set as `None`.
    
    _task_flag : `int`
        A flag to store the state of the ``Pagination``.
        
        Possible values:
        +---------------------------+-------+-----------------------------------------------------------------------+
        | Respective name           | Value | Description                                                           |
        +===========================+=======+=======================================================================+
        | GUI_STATE_READY           | 0     | The Pagination does nothing, is ready to be used.                     |
        +---------------------------+-------+-----------------------------------------------------------------------+
        | GUI_STATE_SWITCHING_PAGE  | 1     | The Pagination is currently changing it's page.                       |
        +---------------------------+-------+-----------------------------------------------------------------------+
        | GUI_STATE_CANCELLING      | 2     | The pagination is currently changing it's page, but it was cancelled  |
        |                           |       | meanwhile.                                                            |
        +---------------------------+-------+-----------------------------------------------------------------------+
        | GUI_STATE_CANCELLED       | 3     | The pagination is, or is being cancelled right now.                   |
        +---------------------------+-------+-----------------------------------------------------------------------+
        | GUI_STATE_SWITCHING_CTX   | 4     | The Pagination is switching context. Not used by the default class,   |
        |                           |       | but expected.                                                         |
        +---------------------------+-------+-----------------------------------------------------------------------+
    
    _timeouter : `None`, ``Timeouter``
        Executes the timing out feature on the ``Pagination``.
    
    channel : ``Channel``
        The channel where the ``Pagination`` is executed.
    
    client : ``Client`` of ``Embed`` (or any compatible)
        The client who executes the ``Pagination``.
    
    message : `None`, ``Message``
        The message on what the ``Pagination`` is executed.
    """
    __slots__ = ('_canceller', '_task_flag', '_timeouter', 'channel', 'client', 'message')
    
    async def __new__(cls, client, channel):
        """
        Pagination instances should have asynchronous constructor.
        
        Parameters
        ----------
        
        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError
    
    
    async def __call__(self, client, event):
        """
        Called when a reaction is added or removed from the respective message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who executes the ``Pagination``.
        event : ``ReactionAddEvent``, ``ReactionDeleteEvent``
            The received event.
        """
        pass
    
    
    async def _canceller_function(self, exception):
        """
        Used when the ``Pagination`` is cancelled.
        
        First of all removes the pagination from waitfors, so it will not wait for reaction events, then sets the
        ``._task_flag`` of the it to `GUI_STATE_CANCELLED`.
        
        If `exception` is given as `TimeoutError`, then removes the ``Pagination``'s reactions from the respective
        message.
        
        This method is a coroutine.
        
        Parameters
        ----------
        exception : `None`, ``BaseException``
            Exception to cancel the ``Pagination`` with.
        """
        client = self.client
        message = self.message
        
        client.events.reaction_add.remove(message, self)
        client.events.reaction_delete.remove(message, self)
        
        if self._task_flag == GUI_STATE_SWITCHING_CTX:
            # the message is not our, we should not do anything with it.
            return
        
        self._task_flag = GUI_STATE_CANCELLED
        
        if not await self._handle_close_exception(exception):
            await client.events.error(client, f'{self!r}._canceller_function', exception)
    
    
    async def _handle_close_exception(self, exception):
        """
        Handles close exception if any.
        
        This method is a coroutine.
        
        Parameters
        ----------
        exception : `None`, `BaseException`
            The close exception to handle.
        
        Returns
        -------
        exception_handled : `bool`
            Whether the exception was handled.
        """
        if exception is None:
            return True
        
        client = self.client
        message = self.message
        
        if isinstance(exception, CancelledError):
            try:
                await client.message_delete(message)
            except GeneratorExit:
                raise
            
            except BaseException as err:
                
                if isinstance(err, ConnectionError):
                    # no internet
                    return True
                
                if isinstance(err, DiscordException):
                    if err.code in (
                        ERROR_CODES.unknown_channel, # channel deleted
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.missing_access, # client removed
                    ):
                        return True
                
                await client.events.error(client, f'{self!r}._handle_close_exception', err)
            
            return True
        
        if isinstance(exception, TimeoutError):
            if self.channel.cached_permissions_for(client).can_manage_messages:
                try:
                    await client.reaction_clear(message)
                except GeneratorExit:
                    raise
                
                except BaseException as err:
                    
                    if isinstance(err, ConnectionError):
                        # no internet
                        return True
                    
                    if isinstance(err, DiscordException):
                        if err.code in (
                            ERROR_CODES.unknown_message, # message deleted
                            ERROR_CODES.unknown_channel, # channel deleted
                            ERROR_CODES.missing_access, # client removed
                            ERROR_CODES.missing_permissions, # permissions changed meanwhile
                        ):
                            return True
                    
                    await client.events.error(client, f'{self!r}._handle_close_exception', err)
            
            return True
        
        if isinstance(exception, PermissionError):
            return True
        
        return False
    
    
    def cancel(self, exception=None):
        """
        Cancels the pagination, if it is not cancelled yet.
        
        Parameters
        ----------
        exception : `None`, ``BaseException`` = `None`, Optional
            Exception to cancel the pagination with. Defaults to `None`
        
        Returns
        -------
        canceller_task : `None`, ``Task``
        """
        if self._task_flag in (GUI_STATE_READY, GUI_STATE_SWITCHING_PAGE, GUI_STATE_CANCELLING):
            self._task_flag = GUI_STATE_CANCELLED
        
        canceller = self._canceller
        if canceller is None:
            return
        
        self._canceller = None
        
        timeouter = self._timeouter
        if (timeouter is not None):
            timeouter.cancel()
        
        return Task(canceller(self, exception), KOKORO)
    
    
    def __repr__(self):
        """Returns the pagination instance's representation."""
        repr_parts = [
            '<', self.__class__.__name__,
            ' client = ', repr(self.client),
            ', channel = ', repr(self.channel),
            ', state = '
        ]
        
        task_flag = self._task_flag
        repr_parts.append(repr(task_flag))
        repr_parts.append(' (')
        
        task_flag_name = GUI_STATE_VALUE_TO_NAME[task_flag]
        
        repr_parts.append(task_flag_name)
        repr_parts.append(')')
        
        # Third party things go here
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def is_active(self):
        """
        Returns whether the menu is still active.
        
        Returns
        -------
        is_active : `bool`
        """
        return (self._task_flag in (GUI_STATE_READY, GUI_STATE_SWITCHING_PAGE))
