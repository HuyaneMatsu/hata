__all__ = ()

from itertools import chain


def _unwrap_plugin(plugin, deep):
    """
    Unwraps the given plugin.
    
    Parameters
    ----------
    plugin : ``Plugin``
        The plugin to unwrap.
    deep : `bool`
        Whether the plugin with all of it's parent and with their child should be returned.
    
    Returns
    -------
    plugins : `set` of ``Plugin``
    """
    plugins_to_unwrap = [plugin]
    unwrapped_plugins = set()
    
    while plugins_to_unwrap:
        plugin = plugins_to_unwrap.pop()
        
        if deep:
            for iterated_plugin in chain(
                plugin.iter_child_plugins(),
                plugin.iter_parent_plugins(),
                plugin.iter_sub_module_plugins()
            ):
                if iterated_plugin not in unwrapped_plugins:
                    plugins_to_unwrap.append(iterated_plugin)
        
        unwrapped_plugins.add(plugin)
    
    return unwrapped_plugins


def _sort_plugins(plugins):
    """
    Sorts the given plugins.
    
    Parameters
    ----------
    plugins : `set` of ``Plugin``
        Plugin to sort.
    
    Returns
    -------
    plugins : `list` of ``Plugin``
        Sorted plugins.
    """
    plugins_to_check_ordered = sorted(plugins, reverse = True)
    
    plugins_satisfied = set()
    plugins_satisfied_ordered = []
    
    while plugins_to_check_ordered:
        for index in reversed(range(len(plugins_to_check_ordered))):
            plugin = plugins_to_check_ordered[index]
            
            if not plugin.are_child_plugins_present_in(plugins_satisfied):
                continue
            
            plugins_satisfied.add(plugin)
            plugins_satisfied_ordered.append(plugin)
            del plugins_to_check_ordered[index]
            break

        else:
            raise RuntimeError(
                f'Plugins with circular satisfaction: {plugins_to_check_ordered!r}'
            )
    
    return plugins_satisfied_ordered
