__all__ = ()

from .plugin_tree import PluginTree


def _is_plugin_in_plugin_trees(plugin, plugin_trees):
    """
    Returns whether the plugin is in an of the given plugin trees.
    
    Parameters
    ----------
    plugin : ``Plugin``
        The plugin to check its presence of.
    plugin_trees : `set` of ``PluginTree``
        Already built plugin trees.
    
    Returns
    -------
    is_plugin_in_plugin_trees : `bool`
    """
    for plugin_tree in plugin_trees:
        if plugin_tree.has_plugin(plugin):
            return True
    
    return False


def _remove_subset_plugin_trees(plugin_tree, plugin_trees):
    """
    Removes subset only plugins trees. Their entry point must match too.
    
    Parameters
    ----------
    plugin_tree : ``PluginTree``
        The plugin tree to check against.
    plugin_trees : `set` of ``PluginTree``
        Already built plugin trees.
    """
    plugin_trees_to_remove = None
    
    for plugin_tree_to_check in plugin_trees:
        if plugin_tree.get_entry_plugin() is not plugin_tree_to_check.get_entry_plugin():
            continue
        
        if not plugin_tree_to_check.is_subset_of_plugin_tree(plugin_tree):
            continue
        
        if plugin_trees_to_remove is None:
            plugin_trees_to_remove = []
        
        plugin_trees_to_remove.append(plugin_tree_to_check)
        
    if (plugin_trees_to_remove is not None):
        plugin_trees.discard(plugin_tree)


def _build_plugin_trees(plugins, plugin_trees, deep):
    """
    Builds plugin trees from the given plugins.
    
    Parameters
    ----------
    plugins : `iterable` of ``Plugin``
        Plugins to build trees for.
    plugin_trees : `iterable` of ``PluginTree``
        Already matched plugin trees if any.
    deep : `bool`
        Whether the plugin with all of it's parent and with their child should be returned.
    
    Returns
    -------
    plugin_trees : `set` of ``PluginTree``
    """
    plugin_trees = {*plugin_trees}
    
    for plugin in plugins:
        if _is_plugin_in_plugin_trees(plugin, plugin_trees):
            continue
        
        plugin_tree = PluginTree(plugin, deep)
        _remove_subset_plugin_trees(plugin_tree, plugin_trees)
        plugin_trees.add(plugin_tree)
    
    return plugin_trees


def _sort_plugin_trees(plugin_trees):
    """
    Sorts the given plugin trees.
    
    Parameters
    ----------
    plugin_trees : `set` of ``PluginTree``
        Plugin trees to sort.
    
    Returns
    -------
    plugin_trees : `list` of ``PluginTree``
    """
    return sorted(plugin_trees)


def _build_and_sort_plugin_trees(plugins, plugin_trees, deep):
    """
    Builds plugin tree and sorts them.
    
    Parameters
    ----------
    plugins : `iterable` of ``Plugin``
        A list of plugin to build the tree form.
    plugin_trees : `iterable` of ``PluginTree``
        Already matched plugin trees if any.
    deep : `bool`
        Whether the plugin with all of it's parent and with their child should be returned.
    
    Returns
    -------
    plugin_trees : `list` of ``PluginTree``
    """
    return _sort_plugin_trees(_build_plugin_trees(plugins, plugin_trees, deep))


def _unwrap_plugin_trees_into_plugins(plugin_trees):
    """
    Unwraps the plugin trees.
    
    Parameters
    ----------
    plugin_trees : `list` of ``PluginTree``
        Plugin trees to unwrap.
    
    Returns
    -------
    plugins : `list` of ``PluginTree``
    """
    plugins = []
    
    for plugin_tree in plugin_trees:
        plugins.extend(plugin_tree.get_plugins_sorted())
    
    return plugins
