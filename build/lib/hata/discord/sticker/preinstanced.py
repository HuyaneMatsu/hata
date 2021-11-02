__all__ = ('StickerFormat', 'StickerType', )

from ...backend.export import export

from ..bases import PreinstancedBase, Preinstance as P

@export
class StickerFormat(PreinstancedBase):
    """
    Represents a message sticker's format's type.
    
    Attributes
    ----------
    name : `str`
        The name of the message sticker format type.
    value : `int`
        The Discord side identifier value of the message sticker format type.
    extension : `str`
        The extension of the sticker format type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``StickerFormat``) items
        Stores the predefined ``StickerFormat`` instances. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The message sticker format type' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the sticker format types.
    DEFAULT_EXTENSION : `str` = `'png'`
        The default extension of the sticker format type.
    
    Every predefined sticker format type can be accessed as class attribute as well:
    
    +-----------------------+-----------+-------+---------------+
    | Class attribute name  | name      | value | extension     |
    +=======================+===========+=======+===============+
    | none                  | none      | 0     | png           |
    +-----------------------+-----------+-------+---------------+
    | png                   | png       | 1     | png           |
    +-----------------------+-----------+-------+---------------+
    | apng                  | apng      | 2     | png           |
    +-----------------------+-----------+-------+---------------+
    | lottie                | lottie    | 3     | json          |
    +-----------------------+-----------+-------+---------------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    DEFAULT_EXTENSION = 'png'
    
    __slots__ = ('extension', )
    
    @classmethod
    def _from_value(cls, value):
        """
        Creates a sticker format type from the given id and stores it at class's `.INSTANCES`.
        
        Called by `.get` when no sticker format type was found with the given id.
        
        Parameters
        ----------
        id_ : `int`
            The identifier of the sticker format type.
        
        Returns
        -------
        sticker_format : ``StickerFormat``
        """
        self = object.__new__(cls)
        self.name = cls.DEFAULT_NAME
        self.value = value
        self.extension = cls.DEFAULT_EXTENSION
        self.INSTANCES[value] = self
        return self
    
    def __init__(self, value, name, extension):
        """
        Creates a new sticker format type with the given parameters and stores it at the class's `.INSTANCES`.
        
        Parameters
        ----------
        value : `int`
            The Discord side identifier value of the message sticker format type.
        name : `str`
            The name of the message sticker format type.
        extension : `str`
            The extension of the sticker format type.
        """
        self.name = name
        self.value = value
        self.extension = extension
        self.INSTANCES[value] = self
    
    # predefined
    none = P(0, 'none', 'png')
    png = P(1, 'png', 'png')
    apng = P(2, 'apng', 'png')
    lottie = P(3, 'lottie', 'json')


class StickerType(PreinstancedBase):
    """
    Represents a message sticker's type.
    
    Attributes
    ----------
    name : `str`
        The name of the message sticker type.
    value : `int`
        The Discord side identifier value of the message sticker type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``StickerType``) items
        Stores the predefined ``StickerType`` instances. These can be accessed with their `value` as key.
    VALUE_TYPE : `type` = `int`
        The message sticker types' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the sticker types.
    
    Every predefined sticker type can be accessed as class attribute as well:
    
    +-----------------------+-----------+-------+
    | Class attribute name  | name      | value |
    +=======================+===========+=======+
    | none                  | none      | 0     |
    +-----------------------+-----------+-------+
    | standard              | standard  | 1     |
    +-----------------------+-----------+-------+
    | guild                 | guild     | 2     |
    +-----------------------+-----------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    standard = P(1, 'standard')
    guild = P(2, 'guild')
