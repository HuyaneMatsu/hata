__all__ = ('WebhookType',)

from ...bases import Preinstance as P, PreinstancedBase


class WebhookType(PreinstancedBase, value_type = int):
    """
    Represents a webhook's type.
    
    Attributes
    ----------
    name : `str`
        The name of the webhook type.
    
    value : `int`
        The discord side identifier value of the webhook type.
    
    Type Attributes
    ---------------
    Every predefined webhook type can be accessed as type attribute as well:
    
    +-----------------------+---------------+-------+
    | Type attribute name   | name          | value |
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
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    bot = P(1, 'bot')
    server = P(2, 'server')
    application = P(3, 'application')
