from .achievement import *
from .connection import *
from .helpers import *
from .oauth2_access import *
from .oauth2_user import *
from .preinstanced import *

__all__ = (
    *achievement.__all__,
    *connection.__all__,
    *helpers.__all__,
    *oauth2_access.__all__,
    *oauth2_user.__all__,
    *preinstanced.__all__,
)

from ...utils.module_deprecation import deprecated_import
deprecated_import(Oauth2User, 'UserOA2')
deprecated_import(Oauth2Access, 'OA2Access')
