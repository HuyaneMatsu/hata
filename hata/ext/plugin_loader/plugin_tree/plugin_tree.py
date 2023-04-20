__all__ = ('PluginTree',)

from itertools import chain

from scarletio import RichAttributeErrorBaseType

from ..plugin import Plugin

from .plugin_helpers import _sort_plugins, _unwrap_plugin


class PluginTree(RichAttributeErrorBaseType):
    """
    Represents a standalone plugin tree.
    
    Attributes
    ----------
    _plugins : `frozenset` of ``Plugin``
        Unordered plugins of the plugin tree.
    _plugins_sorted : `None`, `list` of ``Plugin``
        Cache fields for ``.get_plugins_sorted``.
    """
    __slots__ = ('_plugins', '_plugins_sorted')
    
    def __new__(cls, plugin, deep):
        """
        Creates a new plugin tree instance.
        
        Parameters
        ----------
        plugin : ``Plugin``
            Plugin to create tree from.
        deep : `bool`
            Whether the plugin with all of it's parent and with their child should be returned.
        """
        plugins = frozenset(_unwrap_plugin(plugin, deep))
        
        self = object.__new__(cls)
        self._plugins = plugins
        self._plugins_sorted = None
        return self
    
    
    def __repr__(self):
        """Returns the plugin tree's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        try:
            entry_plugin = self.get_entry_plugin()
        except RuntimeError:
            pass
        else:
            repr_parts.append(' entry_plugin = ')
            repr_parts.append(repr(entry_plugin.name))
            repr_parts.append(',')
        
        repr_parts.append(' plugin_count = ')
        repr_parts.append(repr(self.get_plugin_count()))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the hash value of the plugin tree."""
        return hash(self._plugins)
    
    
    def __eq__(self, other):
        """Returns whether the two plugin trees are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self._plugins == other._plugins
    
    
    def __gt__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        return self.get_entry_plugin() > other.get_entry_plugin()
    
    
    
    def get_plugins_sorted(self):
        """
        Returns the sorted plugins.
        
        Returns
        -------
        plugins : `list` of ``Plugin``
        """
        plugins_sorted = self._plugins_sorted
        if plugins_sorted is None:
            plugins_sorted = _sort_plugins(self._plugins)
            self._plugins_sorted = plugins_sorted
        
        return plugins_sorted
    
    
    def get_entry_plugin(self):
        """
        Gets the entry plugin.
        
        Returns
        -------
        plugin : ``Plugin``
        """
        return self.get_plugins_sorted()[-1]
    
    
    def get_plugin_count(self):
        """
        Returns how much plugins are in the plugin tree.
        
        Returns
        -------
        plugin_count : `int`
        """
        return len(self._plugins)
    
    
    def has_plugin(self, plugin):
        """
        Returns whether the plugin tree has the given plugin.
        
        Parameters
        ----------
        plugin : ``Plugin``
            The plugin to check.
        
        Returns
        -------
        has_plugin : `bool`
        """
        return plugin in self._plugins
    
    
    def has_plugin_tree(self, plugin_tree):
        """
        Returns whether the plugin tree is a superset of the given plugin tree.
        
        Parameters
        ----------
        plugin_tree : `instance<type<self>>`
            The plugin tree to check.
        
        Returns
        -------
        is_superset : `bool`
        """
        return plugin_tree._plugins.issuperset(self._plugins)
    
    
    def is_equal_to_plugin(self, plugin):
        """
        Returns whether the plugin tree equals to the given plugin.
        
        Parameters
        ----------
        plugin : ``Plugin``
            The plugin to check.
        
        Returns
        -------
        is_equal : `bool`
        """
        plugins = self._plugins
        return len(plugins) == 1 and next(iter(plugins)) is plugin
    
    
    def is_equal_to_plugin_tree(self, plugin_tree):
        """
        Returns whether the plugin tree equals to the given plugin tree.
        
        Parameters
        ----------
        plugin_tree : `instance<type<self>>`
            The plugin tree to check.
        
        Returns
        -------
        is_equal : `bool`
        """
        return (self._plugins == plugin_tree._plugins)
    
    
    def is_subset_of_plugin(self, plugin):
        """
        Returns whether the plugin tree is a subset of the given plugin.
        
        Parameters
        ----------
        plugin : ``Plugin``
            The plugin to check.
        
        Returns
        -------
        is_subset : `bool`
        """
        return (not self._plugins)
    
    
    def is_subset_of_plugin_tree(self, plugin_tree):
        """
        Returns whether the plugin tree is a sub set the given plugin tree.
        
        Parameters
        ----------
        plugin_tree : `instance<type<self>>`
            The plugin tree to check.
        
        Returns
        -------
        is_subset : `bool`
        """
        return plugin_tree._plugins.issubset(self._plugins)
    
    
    def has_intersection_with_plugin(self, plugin):
        """
        Returns whether the plugin tree has intersection with the given plugin.
        
        Parameters
        ----------
        plugin : ``Plugin``
            The plugin to check.
        
        Returns
        -------
        has_intersection : `bool`
        """
        return plugin in self._plugins
    
    
    def has_intersection_with_plugins(self, plugins):
        """
        Returns whether the plugin tree has intersection with the given plugins.
        
        Parameters
        ----------
        plugins : `iterable` of ``Plugin``
            The plugins to check.
        
        Returns
        -------
        has_intersection : `bool`
        """
        return (True if self._plugins.intersection(plugins) else False)
    
    
    def get_intersection_with_plugins(self, plugins):
        """
        Returns the plugin tree and given plugins intersection.
        
        Parameters
        ----------
        plugins : `iterable` of ``Plugin``
            The plugins to check.
        
        Returns
        -------
        intersection : `set` of ``Plugin``
        """
        return self._plugins.intersection(plugins)
    
    
    def has_intersection_with_plugin_tree(self, plugin_tree):
        """
        Returns whether the plugin tree has intersection with the given plugin tree.
        
        Parameters
        ----------
        plugin_tree : `instance<type<self>>`
            The plugin tree to check.
        
        Returns
        -------
        has_intersection : `bool`
        """
        return (True if self._plugins.intersection(plugin_tree._plugins) else False)
    
    
    def merge_with_plugin_tree(self, plugin_tree):
        """
        Merges the two plugin trees.
        
        Parameters
        ----------
        plugin_tree : `instance<type<self>>`
            The plugin tree to check.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        new._plugins = frozenset(chain(self._plugins, plugin_tree._plugins))
        new._plugins_sorted = None
        return new
    
    
    def iter_plugins(self):
        """
        Iterates over the plugins contained by the plugin tree.
        
        This method is an iterable generator.
        
        Yields
        ------
        plugin : ``Plugin``
        """
        yield from self._plugins
    
    
    def copy_without(self, plugins):
        """
        Copies the plugin tree without the given plugins.
        
        Parameters
        ----------
        plugins : `set` of ``Plugin``
        
        Returns
        -------
        new : `instance<type<self>>`, `None`
            Returns `None` if the new copy would be empty.
        """
        old_plugins = self._plugins
        new_plugins = old_plugins - plugins
        
        new_length = len(new_plugins)
        if new_length == 0:
            return None
        
        if new_length == len(old_plugins):
            return self
        
        new = object.__new__(type(self))
        new._plugins = new_plugins
        new._plugins_sorted = None
        return new
