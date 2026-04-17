__all__ = ('get_plugins_like',)

from re import I as re_ignore_case, compile as re_compile, escape as re_escape

from ..constants import PLUGINS


def _plugin_match_sort_key(item):
    """
    Sort key used inside of ``get_plugins_like`` to sort plugins based on their match rate.
    
    Parameters
    ----------
    item : `tuple` (``Plugin``, `tuple` (`int`, `int`))
        The plugin and it's match rate.
    
    Returns
    -------
    match_rate : `tuple` (`int`, `int`)
    """
    return item[1]


def get_plugins_like(name):
    """
    Returns the plugins witch match the given name the most.
    
    Parameters
    ----------
    name : `str`
        An plugin's name.
    
    Returns
    -------
    plugins : `list` of ``Plugin``.
        The matched plugins.
    """
    name = name.replace('-', '_').replace(' ', '_')
    
    pattern = re_compile(re_escape(name), re_ignore_case)
    
    to_sort = []
    
    for plugin in PLUGINS.values():
        plugin_name = plugin.name
        parsed = pattern.search(plugin_name)
        if parsed is None:
            continue
        
        match_start = parsed.start()
        to_sort.append((plugin, (match_start, len(plugin_name))))
    
    if not to_sort:
        return to_sort
    
    to_sort.sort(key = _plugin_match_sort_key)
    return [item[0] for item in to_sort]
