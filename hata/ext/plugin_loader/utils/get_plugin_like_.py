__all__ = ('get_plugin_like',)

from re import I as re_ignore_case, compile as re_compile, escape as re_escape


from ..constants import PLUGINS


def get_plugin_like(name):
    """
    Returns the plugin witch matches the given name the most.
    
    Parameters
    ----------
    name : `str`
        An plugin's name.
    
    Returns
    -------
    plugin : ``Plugin``, `None`.
        The matched plugin if any.
    """
    name = name.replace('-', '_').replace(' ', '_')
    
    target_name_length = len(name)
    pattern = re_compile(re_escape(name), re_ignore_case)
    
    accurate_plugin = None
    accurate_name_length = -1
    
    for plugin in PLUGINS.values():
        plugin_name = plugin.name
        name_length = len(plugin_name)
        if (accurate_name_length != -1) and (name_length > accurate_name_length):
            continue
        
        if pattern.search(plugin_name) is None:
            continue
        
        if (accurate_name_length == -1) or (name_length < accurate_name_length):
            accurate_plugin = plugin
            accurate_name_length = name_length
        
        if (name_length == target_name_length) and (name == plugin_name):
            return plugin
        
        continue
    
    return accurate_plugin
