__all__ = ()

from scarletio import RichAttributeErrorBaseType

from ..constants import PLUGIN_ACTION_FLAG_LOAD


class PluginTreeIterator(RichAttributeErrorBaseType):
    """
    Plugin tree iterator iterating over their plugins.
    
    Attributes
    ----------        
    action : `int`
        Plugin loader action flag that will be executed on the plugins.
    current_plugin_tree : `None`, ``PluginTree``
        The plugin tree that's plugins are currently iterated over.
    current_plugins : `None`, `list` of ``Plugin``
        The plugins we are currently iterating over. They belong to ``.current_plugin_tree``.
    done_cancelled : `None`, `set` of ``PluginTree``
        Cancelled plugin trees.
    done_fail : `None`, `set` of ``PluginTree``
        Failed plugin trees.
    done_success : `None`, `set` of ``PluginTree``
        Plugin trees passed successfully.
    iterated : `None`, `set` of ``Plugin``
        Already iterated plugins.
    to_do : `None`, `list` of ``PluginTree``
       Plugin trees sorted in reversed order to the action executed. (Always the last one is popped.)
    """
    __slots__ = (
        'action', 'current_plugin_tree', 'current_plugins', 'done_cancelled', 'done_fail', 'done_success',
        'iterated', 'to_do'
    )
    
    def __new__(cls, plugin_trees, action):
        """
        Creates a new plugin tree iterator.
        
        Parameters
        ----------
        plugin_trees : `list` of ``PluginTree``
            Already sorted plugin trees.
        
        action : `int`
            Plugin loader action flag that will be executed on the plugins.
        """
        to_do = plugin_trees.copy()
        
        if action == PLUGIN_ACTION_FLAG_LOAD:
            to_do.reverse()
        
        if not to_do:
            to_do = None
        
        self = object.__new__(cls)
        self.action = action
        self.current_plugin_tree = None
        self.current_plugins = None
        self.done_success = None
        self.done_fail = None
        self.done_cancelled = None
        self.iterated = None
        self.to_do = to_do
        return self
    
    
    def __iter__(self):
        """
        Returns an iterator over self.
        
        Returns
        -------
        self : `instance<type<self>>`
        """
        return self
    
    
    def __next__(self):
        """
        Gets the next element of self.
        
        Returns
        -------
        plugin : ``Plugin``
        
        Raises
        ------
        StopIteration
            - If there are no more plugins to iterate trough.
        """
        while True:
            next_plugin = self._try_set_next_plugin_tree_and_pull()
            if (next_plugin is None):
                break
            
            if self._register_as_iterated(next_plugin):
                return next_plugin
        
        raise StopIteration()
    
    
    def _try_set_next_plugin_tree_and_pull(self):
        """
        Tries to set the next plugin tree if required and pulls a new plugin.
        
        Returns
        -------
        plugin : `None`, ``Plugin``
        """
        current_plugins = self.current_plugins
        current_plugin_tree = self.current_plugin_tree
        # Iteration over perhaps?
        if (current_plugins is None):
            if (current_plugin_tree is not None):
                self.add_done_success(current_plugin_tree)
            
            return self._set_next_plugin_tree_and_pull()
        
        if current_plugin_tree is not None:
            return self._pull_next_plugin()
        
        return self._set_next_plugin_tree_and_pull()
    
    
    def _set_next_plugin_tree_and_pull(self):
        """
        Sets the next plugin plugin tree and pulls a new plugin.
        
        Returns
        -------
        plugin : `None`, ``Plugin``
        """
        while True:
            to_do = self.to_do
            if (to_do is None):
                return None
            
            current_plugin_tree = to_do.pop()
            if not to_do:
                self.to_do = None
            
            current_plugins = current_plugin_tree.get_plugins_sorted()
            if not current_plugins:
                self.add_done_success(current_plugin_tree)
                continue
            
            current_plugins = current_plugins.copy()
            
            if self.action == PLUGIN_ACTION_FLAG_LOAD:
                current_plugins.reverse()
            
            self.current_plugin_tree = current_plugin_tree
            self.current_plugins = current_plugins
            return self._pull_next_plugin()
    
    
    def _pull_next_plugin(self):
        """
        Pulls the next plugin from the currently set plugin.
        
        Returns
        -------
        plugin : `None`, ``Plugin``
        """
        current_plugins = self.current_plugins
        if (current_plugins is None):
            return None
        
        next_plugin = current_plugins.pop()
        if not current_plugins:
            self.current_plugins = None
        
        return next_plugin
    
    
    def add_done_success(self, plugin_tree):
        """
        Adds a done plugin tree as successfully iterated. The plugin must be not
        
        Parameters
        ----------
        plugin_tree : ``PluginTree``
        """
        if self.has_done(plugin_tree):
            return
        
        done_success = self.done_success
        if (done_success is None):
            done_success = set()
            self.done_success = done_success
        
        done_success.add(plugin_tree)
    
    
    def add_done_fail(self, plugin_tree):
        """
        Adds a done plugin tree as failed.
        
        Parameters
        ----------
        plugin_tree : ``PluginTree``
        """
        done_fail = self.done_fail
        if (done_fail is None):
            done_fail = set()
            self.done_fail = done_fail
        
        done_fail.add(plugin_tree)
    
    
    def add_done_cancelled(self, plugin_tree):
        """
        Adds a done plugin tree as cancelled.
        
        Parameters
        ----------
        plugin_tree : ``PluginTree``
        """
        done_cancelled = self.done_cancelled
        if (done_cancelled is None):
            done_cancelled = set()
            self.done_cancelled = done_cancelled
        
        done_cancelled.add(plugin_tree)
    
    
    def has_done(self, plugin_tree):
        """
        Returns whether the given plugin tree is already in any done groups of the iterator.
        
        Parameters
        ----------
        plugin_tree : ``PluginTree``
            The plugin tree to check for.
        
        Returns
        -------
        has_done : `bool`
        """
        done_success = self.done_success
        if (done_success is not None) and (plugin_tree in done_success):
            return True
        
        done_fail = self.done_fail
        if (done_fail is not None) and (plugin_tree in done_fail):
            return True
    
        done_cancelled = self.done_cancelled
        if (done_cancelled is not None) and (plugin_tree in done_cancelled):
            return True
        
        return False
    
    
    def _register_as_iterated(self, plugin):
        """
        Registers the given plugin as iterated.
        
        Parameters
        ----------
        plugin : ``Plugin``
            the plugin to register.
        
        Returns
        -------
        freshly_registered : `bool`
            Whether the plugin was not registered before.
        """
        iterated = self.iterated
        if (iterated is None):
            iterated = set()
            self.iterated = iterated
        
        length_old = len(iterated)
        iterated.add(plugin)
        length_new = len(iterated)
        
        return length_old != length_new
    
    
    def fail_current_hard(self):
        """
        Fails the currently iterated plugin tree and removes its plugins from the iteration.
        """
        current_plugin_tree = self.current_plugin_tree
        if (current_plugin_tree is not None):
            self.add_done_fail(current_plugin_tree)
            self.current_plugin_tree = None
            self.current_plugins = None
    
    
    def fail_current_soft(self):
        """
        Fails the currently iterated plugin tree.
        """
        current_plugin_tree = self.current_plugin_tree
        if (current_plugin_tree is not None):
            self.add_done_fail(current_plugin_tree)
        
    
    def cancel_dependents_in_to_do(self, plugins):
        """
        Cancels all plugin trees that contain any of the given plugins.
        
        Parameters
        ----------
        plugins : `set` of ``Plugins``
            The plugins to look for the dependent trees.
        """
        new_to_do = None
        old_to_do = self.to_do
        
        while (old_to_do is not None):
            plugin_tree = old_to_do.pop()
            if not old_to_do:
                old_to_do = None
            
            if plugin_tree.has_intersection_with_plugins(plugins):
                if new_to_do is None:
                    new_to_do = []
                
                new_to_do.append(plugin_tree)
            
            else:
                self.add_done_cancelled(plugin_tree)
        
        if (new_to_do is not None):
            new_to_do.reverse()
        self.to_do = new_to_do
    
    
    def iter_done_success(self):
        """
        Iterates over the done (successfully) plugin trees of the plugin tree iterator.
        
        This method is an iterable generator.
        
        Yields
        ------
        plugin_tree : ``PluginTree``
        """
        done_success = self.done_success
        if (done_success is not None):
            yield from done_success


    def iter_done_cancelled(self):
        """
        Iterates over the done (cancelled) plugin trees of the plugin tree iterator.
        
        This method is an iterable generator.
        
        Yields
        ------
        plugin_tree : ``PluginTree``
        """
        done_cancelled = self.done_cancelled
        if (done_cancelled is not None):
            yield from done_cancelled
    
    
    def iter_done_fail(self):
        """
        Iterates over the done (failed) plugin trees of the plugin tree iterator.
        
        This method is an iterable generator.
        
        Yields
        ------
        plugin_tree : ``PluginTree``
        """
        done_fail = self.done_fail
        if (done_fail is not None):
            yield from done_fail
