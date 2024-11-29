__all__ = ('EventHandlerPlugin', )

from .meta import EventHandlerPluginMeta


class EventHandlerPlugin(metaclass = EventHandlerPluginMeta):
    """
    Inherit event handler manager plugins from this class, like:
    
    ```py
    class MyPlugin(EventHandlerPlugin):
        my_event = Event(...)
    ```
    
    Each ``Event`` will be picked up and added as a plugin event.
    
    To register the plugin:
    
    ```
    my_plugin = MyPlugin()
    client.events.register_plugin(my_plugin)
    ```
    
    After it, you are able to add new event handlers to your client.
    
    ```py
    @client.events
    async def my_event(...):
        pass
    ```
    
    To ensure an event, do:
    
    ```py
    Task(KOKORO, my_plugin.my_event(...))
    ```
    """
    __slots__ = ()
