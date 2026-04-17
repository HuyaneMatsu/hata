__all__ = ('StickerFormat', 'StickerType', )

from scarletio import export

from ...bases import Preinstance as P, PreinstancedBase


@export
class StickerFormat(PreinstancedBase, value_type = int):
    """
    Represents a message sticker's format's type.
    
    Attributes
    ----------
    extension : `str`
        The extension of the sticker format type.
    
    name : `str`
        The name of the message sticker format type.
    
    value : `int`
        The Discord side identifier value of the message sticker format type.
    
    Type Attributes
    ---------------
    Every predefined sticker format type can be accessed as type attribute as well:
    
    +-----------------------+-----------+-------+---------------+
    | Type attribute name   | name      | value | extension     |
    +=======================+===========+=======+===============+
    | none                  | none      | 0     | png           |
    +-----------------------+-----------+-------+---------------+
    | png                   | png       | 1     | png           |
    +-----------------------+-----------+-------+---------------+
    | apng                  | apng      | 2     | png           |
    +-----------------------+-----------+-------+---------------+
    | lottie                | lottie    | 3     | json          |
    +-----------------------+-----------+-------+---------------+
    | gif                   | gif       | 4     | gif           |
    +-----------------------+-----------+-------+---------------+
    """
    __slots__ = ('extension', )
    
    def __new__(cls, value, name = None, extension = 'png'):
        """
        Creates a new sticker format type.
        
        Parameters
        ----------
        value : `int`
            The Discord side identifier value of the message sticker format type.
        
        name : `None | str` = `None`, Optional
            The name of the message sticker format type.
        
        extension : `str` = `'png'`, Optional
            The extension of the sticker format type.
        """
        self = PreinstancedBase.__new__(cls, value, name)
        self.extension = extension
        return self
    
    
    # predefined
    none = P(0, 'none', 'png')
    png = P(1, 'png', 'png')
    apng = P(2, 'apng', 'png')
    lottie = P(3, 'lottie', 'json')
    gif = P(4, 'gif', 'gif')


class StickerType(PreinstancedBase, value_type = int):
    """
    Represents a message sticker's type.
    
    Attributes
    ----------
    value : `int`
        The Discord side identifier value of the message sticker type.
    
    name : `str`
        The name of the message sticker type.
    
    Type Attributes
    ---------------
    Every predefined sticker type can be accessed as type attribute as well:
    
    +-----------------------+-----------+-------+
    | Type attribute name   | name      | value |
    +=======================+===========+=======+
    | none                  | none      | 0     |
    +-----------------------+-----------+-------+
    | standard              | standard  | 1     |
    +-----------------------+-----------+-------+
    | guild                 | guild     | 2     |
    +-----------------------+-----------+-------+
    """
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    standard = P(1, 'standard')
    guild = P(2, 'guild')
