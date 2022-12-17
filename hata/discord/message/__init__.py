from .attachment import *
from .message_activity import *

from .cross_mention import *
from .flags import *
from .message import *
from .message_application import *
from .message_interaction import *
from .preinstanced import *
from .utils import *


__all__ = (
    *attachment.__all__,
    *message_activity.__all__,
    
    *cross_mention.__all__,
    *flags.__all__,
    *message.__all__,
    *message_application.__all__,
    *message_interaction.__all__,
    *preinstanced.__all__,
    *utils.__all__,
)


from ...utils.module_deprecation import deprecated_import


@deprecated_import
class MessageReference:
    """
    A cross guild reference used as a ``Message``'s `.cross_reference` at crosspost messages.
    
    This type is Deprecated and will be removed in 2023 January.
    """
    __slots__ = ()


@deprecated_import
class MessageRepr:
    """
    Represents an uncached message.
    
    This type is Deprecated and will be removed in 2023 January.
    """
    __slots__ = ()
