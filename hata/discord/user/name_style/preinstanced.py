__all__ = ('NameStyleEffect', 'NameStyleFont')


from ...bases import Preinstance as P, PreinstancedBase


class NameStyleEffect(PreinstancedBase, value_type = int):
    """
    Represents a name's style's effect.
    
    Attributes
    ----------
    value : `int`
        The Discord side identifier value of the name style effect.
    
    name : `str`
        The name of the name style effect.
    
    Type Attributes
    ---------------
    Every predefined names style effect can be accessed as type attribute as well:
    
    +-----------------------+-----------+-------+
    | Type attribute name   | name      | value |
    +=======================+===========+=======+
    | none                  | none      | 0     |
    +-----------------------+-----------+-------+
    | gradient              | gradient  | 1     |
    +-----------------------+-----------+-------+
    | neon                  | neon      | 2     |
    +-----------------------+-----------+-------+
    | toon                  | toon      | 3     |
    +-----------------------+-----------+-------+
    | pop                   | pop       | 4     |
    +-----------------------+-----------+-------+
    """
    __slots__ = ()
    
    # predefined
    none = P(0, 'none')
    gradient = P(1, 'gradient')
    neon = P(2, 'neon')
    toon = P(3, 'toon')
    pop = P(4, 'pop')


class NameStyleFont(PreinstancedBase, value_type = int):
    """
    Represents a name's style's font.
    
    Attributes
    ----------
    display_name : `str`
        The display name of the name style font.
    
    font_name : `str`
        The font's name of the name style font.
    
    name : `str`
        The name of the message name style font.
    
    value : `int`
        The Discord side identifier value of the message name style font.
    
    Type Attributes
    ---------------
    Every predefined name style font can be accessed as type attribute as well:
    
    +-----------------------+---------------+-------+---------------+-------------------+
    | Type attribute name   | name          | value | display_name  | font_name         |
    +=======================+===============+=======+===============+===================+
    | default               | default       | 0     |               | Sans              |
    +-----------------------+---------------+-------+---------------+-------------------+
    | sakura                | sakura        | 3     | Sakura        | Cherry Bomb One   |
    +-----------------------+---------------+-------+---------------+-------------------+
    | jelly_bean            | jelly bean    | 4     | Jellybean     | Chicle            |
    +-----------------------+---------------+-------+---------------+-------------------+
    | modern                | modern        | 6     | Modern        | Museo Moderno     |
    +-----------------------+---------------+-------+---------------+-------------------+
    | medieval              | medieval      | 7     | Medieval      | Neo Castel        |
    +-----------------------+---------------+-------+---------------+-------------------+
    | eight_bit             | eight bit     | 8     | 8Bit          | Pixelify Sans     |
    +-----------------------+---------------+-------+---------------+-------------------+
    | vampire               | vampire       | 10    | Vampyre       | Sinistre          |
    +-----------------------+---------------+-------+---------------+-------------------+
    | gg_sans               | gg sans       | 11    | GG Sans       | GG Sans           |
    +-----------------------+---------------+-------+---------------+-------------------+
    | tempo                 | tempo         | 12    | Tempo         | Zilla Slab        |
    +-----------------------+---------------+-------+---------------+-------------------+
    """
    __slots__ = ('display_name', 'font_name')
    
    def __new__(cls, value, name = None, display_name = '', font_name = ''):
        """
        Creates a new name style font.
        
        Parameters
        ----------
        value : `int`
            The Discord side identifier value of the message name style font.
        
        name : `None | str` = `None`, Optional
            The name of the message name style font.
        
        display_name : `str` = `''`, Optional
            The display name of the name style font.
        
        font_name : `str` = `''`, Optional
            The font's name of the name style font.
        """
        self = PreinstancedBase.__new__(cls, value, name)
        self.display_name = display_name
        self.font_name = font_name
        return self
    
    
    # predefined
    default = P(0, 'default', '', 'Sans')
    sakura = P(3, 'sakura', 'Sakura', 'Cherry Bomb One')
    jelly_bean = P(4, 'jelly bean', 'Jellybean', 'Chicle')
    modern = P(6, 'modern', 'Modern', 'Museo Moderno')
    medieval = P(7, 'medieval', 'Medieval', 'Neo Castel')
    eight_bit = P(8, 'eight bit', '8Bit', 'Pixelify Sans')
    vampire = P(10, 'vampire', 'Vampyre', 'Sinistre')
    gg_sans = P(11, 'gg sans', 'GG Sans', 'GG Sans')
    tempo = P(12, 'tempo', 'Tempo', 'Zilla Slab')
