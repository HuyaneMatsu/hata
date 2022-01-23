__all__ = ()

import sys
import warnings
from types import ModuleType

import scarletio
from scarletio import http_client as scarletio_http_client
from scarletio import web_common as scarletio_web_common
from scarletio import websocket as scarletio_websocket


class deprecate(ModuleType):
    def __new__(cls):
        frame = sys._getframe().f_back
        globals_ = frame.f_globals
        
        module_name = globals_['__spec__'].name
        
        module = ModuleType.__new__(cls, module_name)
        
        
        for key, value in globals_.items():
            setattr(module, key, value)
        
        sys.modules[module_name] = module
        
    
    def __getattr__(self, attribute_name):
        for module_name, module_value in (
            ('scarletio', scarletio),
            ('scarletio.web_common', scarletio_web_common),
            ('scarletio.http_client', scarletio_http_client),
            ('scarletio.websocket', scarletio_websocket),
        ):
            try:
                value = getattr(module_value, attribute_name)
            except AttributeError:
                continue
            
            warnings.warn(
                (
                    f'Hata\'s backend has been moved out to a separate library.\n'
                    f'Please do `from {module_name} import {attribute_name}` instead.'
                ),
                FutureWarning,
            )
            
            return value
        
        raise AttributeError(attribute_name)
