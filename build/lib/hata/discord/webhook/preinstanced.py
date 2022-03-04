__all__ = ('WebhookType',)

from ..bases import Preinstance as P, PreinstancedBase


class WebhookType(PreinstancedBase):
    """
    Represents a webhook's type.
    
    Attributes
    ----------
    name : `str`
        The name of the webhook type.
    value : `int`
        The discord side identifier value of the webhook type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``WebhookType``) items
        Stores the predefined ``WebhookType``-s. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The webhook types' values' type.
    DEFAULT_NAME : `str` = `'Undefined'`
        The default name of the webhook types.
    
    Every predefined webhook type can be accessed as class attribute as well:
    
    +-----------------------+---------------+-------+
    | Class attribute name  | name          | value |
    +=======================+===============+=======+
    | none                  | none          | 0     |
    +-----------------------+---------------+-------+
    | bot                   | bot           | 1     |
    +-----------------------+---------------+-------+
    | server                | server        | 2     |
    +-----------------------+---------------+-------+
    | application           | application   | 3     |
    +-----------------------+---------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    bot = P(1, 'bot')
    server = P(2, 'server')
    application = P(3, 'application')

