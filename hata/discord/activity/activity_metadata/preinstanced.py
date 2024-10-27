__all__ = ('HangType',)

from ...bases import Preinstance as P, PreinstancedBase


ACTIVITY_NAME_HANGING_DEFAULT = 'Right now, I\'m -'


def _name_getter_custom(activity):
    """
    Name getter for ``HangType`` for its custom instance.
    
    Parameters
    ----------
    activity : ``Activity``
        The activity to get its name of.
    
    Returns
    -------
    name : `str`
    """
    details = activity.details
    emoji = activity.emoji
    if (details is None):
        if (emoji is None):
            name = ACTIVITY_NAME_HANGING_DEFAULT
        else:
            name = emoji.as_emoji
    else:
        if (emoji is None):
            name = details
        else:
            name = f'{emoji} {details}'

    return name


class HangType(PreinstancedBase):
    """
    Represents a hanging activity' type.
    
    Attributes
    ----------
    name : `str`
        The hang type's name.
    
    name_getter : `(Activity) -> str`
        Function used when getting the hanging activity's name.
    
    value : `str`
        The Discord side identifier value of the hang type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`str`, ``HangType``) items
        Stores the predefined ``HangType``-s.
    
    VALUE_TYPE : `type` = `str`
        The hang types' values' type.
    
    DEFAULT_NAME : `str` = `''`
        The default name of the hang types. Guild features have the same value as name, so at their case it is not
        applicable.
    
    Every predefined hang type can be accessed as class attribute as well:
    
    +-----------------------+---------------+---------------+
    | Class attribute names | name          | value         |
    +=======================+===============+===============+
    | none                  | none          |               |
    +-----------------------+---------------+---------------+
    | be_right_back         | be right back | brb           |
    +-----------------------+---------------+---------------+
    | chilling              | chilling      | chilling      |
    +-----------------------+---------------+---------------+
    | custom                | custom        | custom        |
    +-----------------------+---------------+---------------+
    | focusing              | focusing      | focusing      |
    +-----------------------+---------------+---------------+
    | gaming                | gaming        | gaming        |
    +-----------------------+---------------+---------------+
    | eating                | eating        | eating        |
    +-----------------------+---------------+---------------+
    | travelling            | travelling    | in-transit    |
    +-----------------------+---------------+---------------+
    | watching              | watching      | watching      |
    +-----------------------+---------------+---------------+
    """
    INSTANCES = {}
    VALUE_TYPE = str
    DEFAULT_NAME = ''
    DEFAULT_NAME_GETTER = lambda activity: ACTIVITY_NAME_HANGING_DEFAULT
    
    __slots__ = ('name_getter', )
    
    @classmethod
    def _from_value(cls, value):
        """
        Creates a new hang type.
        
        Parameters
        ----------
        value : `str`
            The hang type's identifier value.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.value = value
        self.name = value.casefold().replace('-', ' ')
        self.name_getter = cls.DEFAULT_NAME_GETTER
        self.INSTANCES[value] = self
        return self
    
    
    def __init__(self, value, name, name_getter):
        """
        Creates a hang type and stores it at the class's `.INSTANCES` class attribute as well.
        
        Parameters
        ----------
        value : `str`
            The Discord side identifier value of the hang type.
        
        name : `str`
            The name of the hang type.
        
        metadata_type : `FunctionType`
            The hang type's name getter.
        """
        self.name = name
        self.name_getter = name_getter
        self.value = value
        
        self.INSTANCES[value] = self
    
    
    # predefined
    none = P('', 'none', DEFAULT_NAME_GETTER)
    be_right_back = P('brb', 'be right back', (lambda activity: 'Gonna BRB'))
    chilling = P('chilling', 'chilling', (lambda activity: 'Chilling'))
    custom = P('custom', 'custom', _name_getter_custom)
    eating = P('eating', 'eating', (lambda activity: 'Grubbin'))
    focusing = P('focusing', 'focusing', (lambda activity: 'In the zone'))
    gaming = P('gaming', 'gaming', (lambda activity: 'GAMING'))
    travelling = P('in-transit', 'travelling', (lambda activity: 'Wandering IRL'))
    watching = P('watching', 'watching', (lambda activity: 'Watchin\' stuff'))
