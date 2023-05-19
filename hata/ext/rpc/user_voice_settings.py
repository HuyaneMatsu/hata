__all__ = ('AudioBalance', 'UserVoiceSettings')

from ...discord.preconverters import preconvert_float


class UserVoiceSettings:
    """
    Attributes
    ----------
    mute : `None`, `bool`
        Whether the user is muted.
    
    audio_balance : `None`, ``AudioBalance``
        Audio balance.
    
    user_id : `None`, `int`
        The user's identifier.
    
    volume : `None`, `float`
        The user's volume.
        
        Can be in range [0.0:2.0].
    """
    __slots__ = ('audio_balance', 'mute', 'user_id', 'volume')
    
    def __repr__(self):
        """Returns the user voice setting's representation."""
        repr_parts = ['<', self.__class__.__name__, ' user_id = ', repr(self.user_id), '>']
        return ''.join(repr_parts)
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new user voice setting from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            User voice settings data.
        
        Returns
        -------
        self : ``UserVoiceSettings``
        """
        mute = data['mute']
        audio_balance = AudioBalance.from_data(data['pan'])
        user_id = int(data['user_id'])
        volume = data['volume']*0.01
        
        self = object.__new__(cls)
        self.mute = mute
        self.audio_balance = audio_balance
        self.user_id = user_id
        self.volume = volume
        
        return self


class AudioBalance:
    """
    Audio balance of a ``UserVoiceSettings``.
    
    Attributes
    ----------
    left : `None`, `float`
        Left balance of the user.
        
        Can be in range [0.0:1.0].
    
    right : `None`, `float`
        Right balance of the user.
        
        Can be in range [0.0:1.0].
    """
    __slots__ = ('left', 'right')
    
    def __new__(cls, *, left = None, right = None):
        """
        Creates a new ``AudioBalance`` from the given parameters.
        
        Parameters
        ----------
        left : `None`, `float` = `None`, Optional (Keyword only)
            Left balance of the user.
            
            Can be in range [0.0:1.0].
        
        right : `None`, `float` = `None`, Optional (Keyword only)
            Right balance of the user.
            
            Can be in range [0.0:1.0].
        
        Raises
        ------
        TypeError
            - If `left` is not `None` nor `float`.
            - If `right` is not `None` nor `float`.
        ValueError
            - If `left` is out of range [0.0:1.0].
            - If `right` is out of range [0.0:1.0].
        """
        if (left is not None):
            left = preconvert_float(left, 'left', 0.0, 1.0)
        
        if (right is not None):
            right = preconvert_float(right, 'right', 0.0, 1.0)
        
        self = object.__new__(cls)
        self.left = left
        self.right = right
        return self
    
    
    def __repr__(self):
        """Returns the audio balance's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        left = self.left
        if (left is not None):
            repr_parts.append(' left=')
            repr_parts.append(left.__format__('.02f'))
            
            field_added = True
        else:
            field_added = False
        
        right = self.right
        if (right is not None):
            if field_added:
                repr_parts.append(',')
                
            repr_parts.append(' right=')
            repr_parts.append(right.__format__('.02f'))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    def to_data(self):
        """
        Converts the audio balance to json serializable object.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        data = {}
        
        left = self.left
        if (left is not None):
            data['left'] = left
        
        right = self.right
        if (right is not None):
            data['right'] = right
        
        return data
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new ``AudioBalance`` from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `object`) items
            Audio balance data.
        
        Returns
        -------
        self : ``AudioBalance``
        """
        left = data['left']
        right = data['right']
        
        self = object.__new__(cls)
        self.left = left
        self.right = right
        return self




