__all__ = ()

from ...env import API_VERSION


if API_VERSION in (6, 7):
    PERMISSION_KEY = 'permissions_new'
    PERMISSION_ALLOW_KEY = 'allow_new'
    PERMISSION_DENY_KEY = 'deny_new'
    
else:
    PERMISSION_KEY = 'permissions'
    PERMISSION_ALLOW_KEY = 'allow'
    PERMISSION_DENY_KEY = 'deny'
