__all__ = ()

from scarletio import RichAttributeErrorBaseType

from .constants import PLUGIN_ACTION_FLAG_NAME_LOOKUP
from .exceptions import PluginError
from .helpers import _iter_lookup_plugin_names_and_paths, _try_get_plugin
from .plugin import Plugin
from .plugin_tree import PluginTree


class PluginExtractor(RichAttributeErrorBaseType):
    """
    Extracts different plugin related values from related input(s).
    
    Attributes
    ----------
    input_plugin_trees : `None`, `set` of ``PluginTree``
        Extracted plugin trees from the input.
    input_plugins : `None`, `set` of ``Plugin``
        Extracted plugins from the input.
    input_strings : `None`, `set` of `str`
        Extracted plugins from the input.
    name : `str`
        The extracted value(s) name.
    """
    __slots__ = ('input_plugin_trees', 'input_plugins', 'input_strings', 'name')
    
    def __new__(cls, name, value):
        """
        Creates a new plugin extractor instance from the given value(s).
        
        Parameters
        ----------
        name : `str`
            The extracted value(s) name.
        value : `None`, `str`, ``Plugin``, ``PluginTree`` `iterable` of (`None`, `str`, ``Plugin``, ``PluginTree``)
            The value(s) to extract.
        
        Raises
        ------
        TypeError
            - If `value`'s type is invalid.
        """
        input_strings = None
        input_plugins = None
        input_plugin_trees = None
        
        if value is None:
            pass
        
        elif isinstance(value, str):
            input_strings = {str(value)}
        
        elif isinstance(value, Plugin):
            input_plugins = {value}
        
        elif isinstance(value, PluginTree):
            input_plugin_trees = {value}
        
        else:
            if getattr(value, '__iter__', None) is None:
                raise TypeError(
                    f'`{name}` can be either `None`, `str`, `{Plugin.__name__}`, `{PluginTree.__name__}`, `iterable`, '
                    f'got {value.__class__.__name__}; {value!r}.'
                )
            
            for iterated_value in value:
                if iterated_value is None:
                    pass
                
                elif isinstance(iterated_value, str):
                    if input_strings is None:
                        input_strings = set()
                    
                    input_strings.add(iterated_value)
                
                elif isinstance(iterated_value, Plugin):
                    if input_plugins is None:
                        input_plugins = set()
                    
                    input_plugins.add(iterated_value)
                
                elif isinstance(iterated_value, PluginTree):
                    if input_plugin_trees is None:
                        input_plugin_trees = set()
                    
                    input_plugin_trees.add(iterated_value)
                
                else:
                    raise TypeError(
                        f'`{name}` elements can be `None`, `str`, `{Plugin.__name__}`, `{PluginTree.__name__}`, '
                        f'got {iterated_value.__class__.__name__}; {iterated_value!r}; value = {value!r}.'
                    )
        
        self = object.__new__(cls)
        self.input_plugin_trees = input_plugin_trees
        self.input_plugins = input_plugins
        self.input_strings = input_strings
        self.name = name
        return self
    
    
    @classmethod
    def from_strings(cls, name, value):
        """
        Creates a new plugin extractor instance from the given string(s).
        
        Parameters
        ----------
        name : `str`
            The extracted value(s) name.
        value : `str`, `iterable` of `str`
            The value(s) to extract.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If `value`'s type is invalid.
        """
        input_strings = None
        
        if isinstance(value, str):
            input_strings = {str(value)}
        else:
            if getattr(value, '__iter__', None) is None:
                raise TypeError(
                    f'`{name}` can be either `str`, `iterable`, got {value.__class__.__name__}; {value!r}.'
                )
            
            for iterated_value in value:
                if isinstance(iterated_value, str):
                    if input_strings is None:
                        input_strings = set()
                    
                    input_strings.add(iterated_value)
                else:
                    raise TypeError(
                        f'`{name}` elements can be `None`, `str`, `{Plugin.__name__}`, `{PluginTree.__name__}`, '
                        f'got {iterated_value.__class__.__name__}; {iterated_value!r}; value = {value!r}.'
                    )

        self = object.__new__(cls)
        self.input_plugin_trees = None
        self.input_plugins = None
        self.input_strings = input_strings
        self.name = name
        return self
    
    
    def __repr__(self):
        """Returns the representation of the plugin extractor."""
        repr_parts = ['<', self.__class__.__name__]
        repr_parts.append(' name = ')
        repr_parts.append(repr(self.name))
        
        input_plugin_trees = self.input_plugin_trees
        if (input_plugin_trees is not None):
            repr_parts.append(', input_plugin_trees = ')
            repr_parts.append(repr(input_plugin_trees))
        
        input_plugins = self.input_plugins
        if (input_plugins is not None):
            repr_parts.append(', input_plugins = ')
            repr_parts.append(repr(input_plugins))
        
        input_strings = self.input_strings
        if (input_strings is not None):
            repr_parts.append(', input_strings = ')
            repr_parts.append(repr(input_strings))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def iter_input_strings(self):
        """
        Iterates over the input strings of the plugin extractor.
        
        This method is an iterable generator.
        
        Yields
        ------
        input_string : `str`
        """
        input_strings = self.input_strings
        if (input_strings is not None):
            yield from input_strings
    
    
    def iter_input_plugins(self):
        """
        Iterates over the input plugins of the plugin extractor.
        
        This method is an iterable generator.
        
        Yields
        ------
        input_plugin : ``Plugin``
        """
        input_plugins = self.input_plugins
        if (input_plugins is not None):
            yield from input_plugins
    
    
    def iter_input_plugin_trees(self):
        """
        Iterates over the input plugin trees of the plugin extractor.
        
        This method is an iterable generator.
        
        Yields
        ------
        input_plugin_tree : ``PluginTree``
        """
        input_plugin_trees = self.input_plugin_trees
        if (input_plugin_trees is not None):
            yield from input_plugin_trees
    
    
    def get_plugin_names_and_paths(self, *, register_directories_as_roots = False):
        """
        Gets plugin names and paths from the input.
        
        Parameters
        ----------
        register_directories_as_roots : `bool` = `False`, Optional (Keyword only)
            Whether directory roots should be registered.
        
        Returns
        -------
        plugin_names_and_paths : `set` of `tuple` ((`str`, `None`), `str`)
            Plugin name - plugin path pairs.
        """
        return {
            *self.iter_plugin_names_and_paths_from_strings(register_directories_as_roots),
            *self.iter_plugin_names_and_paths_from_plugins(),
            *self.iter_plugin_names_and_paths_from_plugin_trees(),
        }
    
    
    def get_plugins(self, *, raise_if_cannot_resolve = True):
        """
        Gets the plugins from the input.
        
        Returns
        -------
        plugins : `set`
            Plugin name - plugin path pairs.
        
        Parameters
        ----------
        raise_if_cannot_resolve : `bool` = `True`, Optional (Keyword only)
            Whether exception should be raised if a plugin cannot be resolved.
        
        Raises
        ------
        PluginError
            If a plugin could not be found.
        """
        return {
            *self.iter_plugins_from_strings(raise_if_cannot_resolve),
            *self.iter_input_plugins(),
            *self.iter_plugin_from_plugin_trees(),
        }
    
    
    def iter_plugin_names_and_paths_from_strings(self, register_directories_as_roots):
        """
        gets the plugin names and the paths from the input strings.
        
        This method is an iterable generator.
        
        Parameters
        ----------
        register_directories_as_roots : `bool`
            Whether directory roots should be registered.
        
        Yields
        ------
        plugin_name : `None`, `str`
            Plugin's  name.
        plugin_path : `str`
            Path of the plugin file.
        """
        for input_string in self.iter_input_strings():
            yield from _iter_lookup_plugin_names_and_paths(input_string, register_directories_as_roots, False)
    
    
    def iter_plugin_names_and_paths_from_plugins(self):
        """
        Gets the plugin names and the paths from the input plugins.
        
        This method is an iterable generator.
        
        Yields
        ------
        plugin_name : `str`
            Plugin's  name.
        plugin_path : `str`
            Path of the plugin file.
        """
        for input_plugin in self.iter_input_plugins():
            yield input_plugin.name, input_plugin.path
    
    
    def iter_plugin_names_and_paths_from_plugin_trees(self):
        """
        Gets the plugin names and the paths from the input plugin trees.
        
        This method is an iterable generator.
        
        Yields
        ------
        plugin_name : `str`
            Plugin's  name.
        plugin_path : `str`
            Path of the plugin file.
        """
        for plugin in self.iter_plugin_from_plugin_trees():
            yield plugin.name, plugin.path
    
    
    def iter_plugins_from_strings(self, raise_if_cannot_resolve):
        """
        Gets the plugins from the input strings.
        
        This method is an iterable generator.
        
        Parameters
        ----------
        raise_if_cannot_resolve : `bool`
            Whether exception should be raised if a plugin cannot be resolved.
        
        Yields
        ------
        plugin : ``Plugin``
        
        Raises
        ------
        PluginError
            If a plugin could not be found.
        """
        for plugin_name, plugin_path in self.iter_plugin_names_and_paths_from_strings(False):
            plugin = _try_get_plugin(plugin_name, plugin_path)
            if (plugin is not None):
                yield plugin
                continue
            
            if raise_if_cannot_resolve:
                raise PluginError(
                    f'No plugin was added with name: `{plugin_name}`.',
                    action = PLUGIN_ACTION_FLAG_NAME_LOOKUP,
                    value = (plugin_name, plugin_path),
                )
    
    
    def iter_plugin_from_plugin_trees(self):
        """
        Gets the plugins from the input plugins trees.
        
        This method is an iterable generator.
        
        Yields
        ------
        plugin : ``Plugin``
        """
        for input_plugin_tree in self.iter_input_plugin_trees():
            yield from input_plugin_tree.iter_plugins()
