__all__ = ()

import warnings

from .. import plugin_loader


def __getattr__(attribute_name):
    new_attribute_name = attribute_name.replace(
        'extension', 'plugin'
    ).replace(
        'EXTENSION', 'PLUGIN'
    ).replace(
        'Extension', 'Plugin'
    )
    
    warnings.warn(
        (
            f'`extension_loader.{attribute_name}` extension is deprecated and will be removed in 2022 December, '
            f'please use `plugin_loader.{new_attribute_name}` instead.'
        ),
        FutureWarning,
        stacklevel = 2,
    )
    
    return getattr(plugin_loader, new_attribute_name)
