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


class HangType(PreinstancedBase, value_type = str):
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
    
    Type Attributes
    ---------------
    Every predefined hang type can be accessed as type attribute as well:
    
    +-----------------------+---------------+---------------+
    | Type attribute name   | name          | value         |
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
    NAME_GETTER_DEFAULT = lambda activity: ACTIVITY_NAME_HANGING_DEFAULT
    
    __slots__ = ('name_getter', )
    
    def __new__(cls, value, name = None, name_getter = None):
        """
        Creates a new hang type.
        
        Parameters
        ----------
        value : `str`
            The Discord side identifier value of the hang type.
        
        name : `None | str` = `None`, Optional
            The name of the hang type.
        
        name_getter : `None | FunctionType` = `None`, Optional
            The hang type's name getter.
        """
        if name is None:
            name = value.casefold().replace('-', ' ')
        
        if name_getter is None:
            name_getter = cls.NAME_GETTER_DEFAULT
        
        self = PreinstancedBase.__new__(cls, value, name)
        self.name_getter = name_getter
        return self
    
    
    # predefined
    none = P('', 'none', NAME_GETTER_DEFAULT)
    be_right_back = P('brb', 'be right back', (lambda activity: 'Gonna BRB'))
    chilling = P('chilling', 'chilling', (lambda activity: 'Chilling'))
    custom = P('custom', 'custom', _name_getter_custom)
    eating = P('eating', 'eating', (lambda activity: 'Grubbin'))
    focusing = P('focusing', 'focusing', (lambda activity: 'In the zone'))
    gaming = P('gaming', 'gaming', (lambda activity: 'GAMING'))
    travelling = P('in-transit', 'travelling', (lambda activity: 'Wandering IRL'))
    watching = P('watching', 'watching', (lambda activity: 'Watchin\' stuff'))
