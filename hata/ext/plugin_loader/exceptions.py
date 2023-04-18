__all__ = ('PluginError', )

from scarletio import CauseGroup

from .constants import (
    PLUGIN_ACTION_FLAG_LOAD, PLUGIN_ACTION_FLAG_NONE, PLUGIN_ACTION_FLAG_SYNTAX_CHECK, PLUGIN_ACTION_FLAG_UNLOAD
)


class PluginError(Exception):
    """
    An exception raised by the ``PluginLoader``, if loading, reloading or unloading an plugin fails with any
    reason.
    
    Attributes
    ----------
    _message : `None`, `str`
        The error's message.
    action : `int`
        Bitwise flags of the actions that were executed.
    plugin : `None`, `list`
        The plugin being actioned when the exception occurred.
    plugin_tree_iterators : `None`, `list` of ``PluginTreeIterator``
        Plugin tree iterators used in the executed actions.
    value : `None`, `object`
        If finding a plugin failed, this value may be set with additional information.
    """
    def __init__(
        self,
        message = None,
        *,
        action = PLUGIN_ACTION_FLAG_NONE,
        cause = None,
        plugin = None,
        plugin_tree_iterators = None,
        value = None,
    ):
        """
        Creates a new plugin error.
        
        Parameters
        ----------
        message : `None`, `str` = `None`, Optional
            The error's message.
        
        action : `int`
            Bitwise flags of the actions that were executed.
        
        cause : `None`, `BaseException` = `None`, Optional (Keyword only)
            Exception cause to apply manually.
        
        plugin : `None`, ``Plugin`` = `None`, Optional (Keyword only)
            The plugin being actioned when the exception occurred.
        
        plugin_tree_iterators : `None`, `list` of ``PluginTreeIterator`` = `None`, Optional (Keyword only)
            Plugin tree iterators used in the executed actions.
        
        value : `None`, `object` = `None`, Optional (Keyword only)
            If finding a plugin failed this value might be set with additional information.
        """
        self._message = message
        self.action = action
        self.plugin = plugin
        self.plugin_tree_iterators = plugin_tree_iterators
        self.value = value
        
        if message is None:
            Exception.__init__(self)
        else:
            Exception.__init__(self, message)
        
        if (cause is not None):
            self.__cause__ = cause
    
    
    def get_plugins(self):
        """
        Returns the plugins that were causing the exception.
        
        Returns
        -------
        plugins : `set` of ``Plugin``
        """
        exceptions_to_scan = [self]
        plugins = set()
        
        while exceptions_to_scan:
            exception = exceptions_to_scan.pop()
            
            if isinstance(exception, PluginError):
                plugin = exception.plugin
                if (plugin is not None):
                    plugins.add(plugin)
            
            cause = exception.__cause__
            if cause is None:
                continue
            
            if isinstance(cause, CauseGroup):
                exceptions_to_scan.extend(cause)
                continue
            
            exceptions_to_scan.append(cause)
            continue
            
        return plugins
    
    
    def get_plugin_tree_iterator_for_syntax_check(self):
        """
        Returns the used plugin tree iterator for syntax check action.
        
        Returns
        -------
        plugin_tree_iterator : `None`, ``PluginTreeIterator``
        """
        return self.get_plugin_tree_iterator_for_action(PLUGIN_ACTION_FLAG_SYNTAX_CHECK)
    
    
    def get_plugin_tree_iterator_for_load(self):
        """
        Returns the used plugin tree iterator for load action.
        
        Returns
        -------
        plugin_tree_iterator : `None`, ``PluginTreeIterator``
        """
        return self.get_plugin_tree_iterator_for_action(PLUGIN_ACTION_FLAG_LOAD)
    
    
    def get_plugin_tree_iterator_for_unload(self):
        """
        Returns the used plugin tree iterator for unload action.
        
        Parameters
        ----------
        action : `int`
            Action flag.
        
        Returns
        -------
        plugin_tree_iterator : `None`, ``PluginTreeIterator``
        """
        return self.get_plugin_tree_iterator_for_action(PLUGIN_ACTION_FLAG_UNLOAD)
    
    
    def get_plugin_tree_iterator_for_action(self, action):
        """
        Returns the used plugin tree iterator for the given action.
        
        Parameters
        ----------
        action : `int`
            Action flag.
        
        Returns
        -------
        plugin_tree_iterator : `None`, ``PluginTreeIterator``
        """
        plugin_tree_iterators = self.plugin_tree_iterators
        if (plugin_tree_iterators is not None):
            for plugin_tree_iterator in plugin_tree_iterators:
                if plugin_tree_iterator.action == action:
                    return plugin_tree_iterator
    
    
    def iter_plugin_tree_iterators(self):
        """
        Iterates over the plugin trees
        """
        plugin_tree_iterators = self.plugin_tree_iterators
        if (plugin_tree_iterators is not None):
            yield from plugin_tree_iterators
    
    
    @property
    def message(self):
        """
        Returns the plugin error's message.
        
        If the plugin error contains more messages connects them.
        
        Returns
        -------
        message : ``Message``
        """
        return '\n\n'.join(self.messages)
    
    
    @property
    def messages(self):
        """
        Returns a list containing the exception error's messages.
        
        Returns
        -------
        messages : `list` of `str`
        """
        messages = []
        
        message = self._message
        if (message is not None):
            messages.append(message)
        
        cause = self.__cause__
        if (cause is not None):
            if isinstance(cause, CauseGroup):
                for cause in cause:
                    messages.append(repr(cause))
            
            else:
                messages.append(repr(cause))
        
        return messages
    
    
    def __len__(self):
        """Returns the amount of messages, what the plugin error contains."""
        length = 0
        
        if (self._message is not None):
            length += 1

        cause = self.__cause__
        if (cause is not None):
            if isinstance(cause, CauseGroup):
                length += len(cause)
            
            else:
                length += 1
        
        return length
    
    
    def __repr__(self):
        """Returns the exception error's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        message = self._message
        if (message is not None):
            repr_parts.append(' message = ')
            repr_parts.append(repr(message))
        
        cause = self.__cause__
        if (cause is not None):
            if isinstance(cause, CauseGroup):
                cause_count = len(cause)
            
            else:
                cause_count = 1
            
            repr_parts.append(' with ')
            repr_parts.append(repr(cause_count))
            repr_parts.append(' cause')
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    __str__ = __repr__


class DoNotLoadPlugin(BaseException):
    """
    Raised to stop an plugin loaded without error.
    """
