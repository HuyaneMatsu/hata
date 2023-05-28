__all__ = ('SoundboardSoundsEventHandler',)

from scarletio import RichAttributeErrorBaseType, TaskGroup

from ..core import KOKORO

from .soundboard_sounds_event_waiter import SoundboardSoundsEventWaiter


SOUNDBOARD_SOUNDS_TIMEOUT = 1.25


class SoundboardSoundsEventHandler(RichAttributeErrorBaseType):
    """
    Waits for soundboard sound events.
    
    Attributes
    ----------
    waiters : `dict` of (`int`, ``SoundboardSoundsEventWaiter``) items
        User chunk waiters.
    """
    __slots__ = ('waiters',)
    
    __event_name__ = 'soundboard_sounds'
    
    def __new__(cls):
        """
        Creates a new soundboard sounds event handler.
        """
        self = object.__new__(cls)
        self.waiters = {}
        return self
    
    
    async def __call__(self, client, event):
        """
        Called by the event parser. Ensures that the waiter's result for the given guild is set.
        
        This method is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client, who received the respective dispatch event.
        event : ``SoundboardSoundsEvent``
            The received guild user chunk event.
        """
        try:
            waiter = self.waiters.pop(event.guild_id)
        except KeyError:
            pass
        else:
            waiter.future.set_result_if_pending(event)
    
    
    def __repr__(self):
        """Returns the soundboard sounds event handler's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append('waits at: ')
        repr_parts.append(repr(len(self.waiters)))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    async def wait_for_events_in_guilds(self, guild_ids):
        """
        Waits for responses in the given guilds.
        
        This method is a coroutine.
        
        Parameters
        ----------
        guild_ids : `list` of `int`
            The guild identifiers to wait events for.
        
        Returns
        -------
        results : `list` of ``SoundboardSoundsEvent``
        """
        task_group = TaskGroup(KOKORO)
        
        # Start waiters and add them into the task group.
        waiters = self.waiters
        for guild_id in guild_ids:
            try:
                waiter = waiters[guild_id]
            except KeyError:
                waiter = SoundboardSoundsEventWaiter()
                waiters[guild_id] = waiter
            else:
                waiter.counter += 1
            
            task_group.add_future(waiter.future)
        
        # Wait all futures to complete with timeout
        future = task_group.wait_all()
        future.apply_timeout(SOUNDBOARD_SOUNDS_TIMEOUT)
        
        try:
            await future
        except TimeoutError:
            # Timeout all started waiters.
            for guild_id in guild_ids:
                try:
                    waiter = waiters.pop(guild_id)
                except KeyError:
                    pass
                else:
                    waiter.future.set_result_if_pending(None)
        
        except:
            # Other exception -> decrement waiter counters -> remove them if counter is 0
            for guild_id in guild_ids:
                try:
                    waiter = waiters[guild_id]
                except KeyError:
                    pass
                else:
                    counter = waiter.counter - 1
                    if counter == 0:
                        del waiters[guild_id]
                        waiter.future.set_result_if_pending(None)
                    else:
                        waiter.counter = counter
            
            raise
        
        # Collect results
        results = []
        
        for future in task_group.done:
            result = future.get_result()
            if (result is not None):
                results.append(result)
        
        return results
