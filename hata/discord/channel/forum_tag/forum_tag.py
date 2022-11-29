__all__ = ('ForumTag', )

from scarletio import copy_docs

from ...bases import DiscordEntity
from ...core import FORUM_TAGS
from ...preconverters import preconvert_snowflake

from .fields import (
    parse_emoji, parse_moderated, parse_name, put_emoji_into, put_moderated_into, put_name_into, validate_emoji,
    validate_moderated, validate_name
)


class ForumTag(DiscordEntity, immortal=True):
    """
    Forum tags can be applied to a thread of a forum channel.
    
    Attributes
    ----------
    id : `int`
        The tag's identifier.
    emoji : `None`, ``Emoji``
        The tag's emoji.
    name : `str`
        The tag's name.
    moderated : `bool`
        Whether this tag can only be added or removed by a user with `manage_threads` permission.
    """
    __slots__ = ('emoji', 'name', 'moderated')
    
    def __new__(cls, name, *, emoji = None, moderated = False):
        """
        Creates a new forum tag instance.
        
        Parameters
        ----------
        name : `str`
            The tag's name.
        emoji : `None`, ``Emoji`` = `None`, Optional (Keyword only)
            The tag's emoji.
        moderated : `bool` = `False`, Optional (Keyword only)
            Whether this tag can only be added or removed by a user with `manage_threads` permission.
        """
        emoji = validate_emoji(emoji)
        moderated = validate_moderated(moderated)
        name = validate_name(name)
        
        self = object.__new__(cls)
        self.id = 0
        self.emoji = emoji
        self.name = name
        self.moderated = moderated
        return self
    
    
    @copy_docs(DiscordEntity.__hash__)
    def __hash__(self):
        forum_tag_id = self.id
        if forum_tag_id:
            return forum_tag_id
        
        return self._get_hash_partial()
    
    
    def _get_hash_partial(self):
        """
        Hashes the fields of the forum tag.
        
        Returns
        -------
        hash_value : `int`
        """
        hash_value = 0
        
        # emoji
        emoji = self.emoji
        if (emoji is not None):
            hash_value ^= emoji.id
        
        # name
        hash_value ^= hash(self.name)
        
        # moderated
        hash_value ^= self.moderated
        
        return hash_value
    
    
    @copy_docs(DiscordEntity.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        # id_
        id_ = self.id
        if id_:
            repr_parts.append(' id=')
            repr_parts.append(repr(id_))
        else:
            repr_parts.append(' partial')
        
        # name
        repr_parts.append(' name=')
        repr_parts.append(repr(self.name))
        
        # emoji:
        emoji = self.emoji
        if (emoji is not None):
            repr_parts.append(' emoji=')
            repr_parts.append(repr(emoji))
        
        # moderated
        if self.moderated:
            repr_parts.append(' moderated=True')
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(DiscordEntity.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        return self._is_equal_same_type(other)
    
    
    @copy_docs(DiscordEntity.__ne__)
    def __ne__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        return not self._is_equal_same_type(other)
    
    
    def _is_equal_same_type(self, other):
        """
        Returns whether the two types are equal.
        
        Helper method for ``.__eq__``
        
        Parameters
        ----------
        other : `instance<type<<self>>`
            The other instance. Must be from the same type.
        
        Returns
        -------
        is_equal : `bool`
        """
        # id
        self_id = self.id
        other_id = other.id
        if self_id and other_id:
            if self_id == other_id:
                return True
            
            return False
        
        # emoji
        if self.emoji != other.emoji:
            return False
        
        # name:
        if self.name != other.name:
            return False
        
        # moderated
        if self.moderated != other.moderated:
            return False
        
        return True
    
    
    @classmethod
    def _create_empty(cls, forum_tag_id):
        """
        Creates an empty forum tag with their default attributes set.
        
        Parameters
        ----------
        forum_tag_id : `int`
            The forum tag's identifier.
        
        Returns
        -------
        self : ``ForumTag``
        """
        self = object.__new__(cls)
        self.id = forum_tag_id
        self.emoji = None
        self.name = ''
        self.moderated = False
        return self
    
    
    def copy(self):
        """
        Copies the forum tag.
        
        Returns
        -------
        new : ``ForumTag``
        """
        new = object.__new__(type(self))
        
        # id
        new.id = 0
        
        # emoji
        new.emoji = self.emoji
        
        # name
        new.name = self.name
        
        # moderated
        new.moderated = self.moderated
        
        return new
    
    
    def copy_with(self, **keyword_parameters):
        # emoji
        try:
            emoji = keyword_parameters.pop('emoji')
        except KeyError:
            emoji = self.emoji
        else:
            emoji = validate_emoji(emoji)
        
        # name
        try:
            name = keyword_parameters.pop('name')
        except KeyError:
            name = self.name
        else:
            name = validate_name(name)
        
        # moderated
        try:
            moderated = keyword_parameters.pop('moderated')
        except KeyError:
            moderated = self.moderated
        else:
            moderated = validate_moderated(moderated)
        
        
        if keyword_parameters:
            raise TypeError(f'Unused or unsettable attributes: {keyword_parameters!r}.')
        
        
        new = object.__new__(type(self))
        new.id = 0
        new.emoji = emoji
        new.name = name
        new.moderated = moderated
        return new
    
    
    @classmethod
    def precreate(cls, forum_tag_id, **keyword_parameters):
        """
        Precreates a new forum tag instance.
        
        Other Parameters
        ----------------
        emoji : `None`, ``Emoji``, Optional (Keyword only)
            The tag's emoji.
        
        name : `str`, Optional (Keyword only)
            The tag's name.
        
        moderated : `bool`, Optional (Keyword only)
            Whether this tag can only be added or removed by a user with `manage_threads` permission.
        
        Returns
        -------
        forum_tag : ``ForumTag``
        
        Raises
        ------
        TypeError
            If any parameter's type is bad or if unexpected parameter is passed.
        ValueError
            If an parameter's type is good, but it's value is unacceptable.
        """
        forum_tag_id = preconvert_snowflake(forum_tag_id, 'forum_tag_id')
        
        if keyword_parameters:
            processable = []
            
            # emoji
            try:
                emoji = keyword_parameters.pop('emoji')
            except KeyError:
                pass
            else:
                emoji = validate_emoji(emoji)
                processable.append(('emoji', emoji))
            
            # name
            try:
                name = keyword_parameters.pop('name')
            except KeyError:
                pass
            else:
                name = validate_name(name)
                processable.append(('name', name))
            
            # moderated
            try:
                moderated = keyword_parameters.pop('moderated')
            except KeyError:
                pass
            else:
                moderated = validate_moderated(moderated)
                processable.append(('moderated', moderated))
            
            if keyword_parameters:
                raise TypeError(f'Unused or unsettable attributes: {keyword_parameters!r}.')
            
        else:
            processable = None
        
        try:
            self = FORUM_TAGS[forum_tag_id]
        except KeyError:
            self = cls._create_empty(forum_tag_id)
            FORUM_TAGS[forum_tag_id] = self
            
            # Cannot detect when we are really-partial in our channel's scope, so lets assign variables only if we
            # were just created.
            if (processable is not None):
                for item in processable:
                    setattr(self, *item)
        
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new forum tag from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Forum tag data.
        
        Returns
        -------
        self : ``ForumTag``
        """
        forum_tag_id = int(data['id'])
        
        try:
            self = FORUM_TAGS[forum_tag_id]
        except KeyError:
            self = object.__new__(cls)
            self.id = forum_tag_id
            FORUM_TAGS[forum_tag_id] = self
        
        self._update_attributes(data)
        return self
    
    
    def _update_attributes(self, data):
        """
        Updates the forum tag with the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Forum tag data.
        """
        # id
        # Internal field
        
        # emoji
        self.emoji = parse_emoji(data)
        
        # name
        self.name = parse_name(data)
        
        # moderated
        self.moderated = parse_moderated(data)
    
    
    def _difference_update_attributes(self, data):
        """
        Updates the forum tag with the given data and returns the changed attributes in an `attribute name - old value`
        relation.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Forum tag data.
        
        Returns
        -------
        old_attributes : `dict` of (`str`, `Any`) items
            The updated attributes.
            
            Every item in the dictionary is optional.
            
            +-----------+-------------------+
            | Keys      | Values            |
            +===========+===================+
            | emoji     | `None`, ``Emoji`` |
            +-----------+-------------------+
            | name      | `str`             |
            +-----------+-------------------+
            | moderated | `bool`            |
            +-----------+-------------------+
        """
        old_attributes = {}
        
        # id
        # Internal field
        
        # emoji
        emoji = parse_emoji(data)
        if (emoji is not self.emoji):
            old_attributes['emoji'] = self.emoji
            self.emoji = emoji
        
        # name
        name = parse_name(data)
        if (name != self.name):
            old_attributes['name'] = self.name
            self.name = name
        
        # moderated
        moderated = parse_moderated(data)
        if (moderated != self.moderated):
            old_attributes['moderated'] = self.moderated
            self.moderated = moderated
        
        return old_attributes
    
    
    def to_data(self, *, defaults = False, include_internals = False):
        """
        Converts the forum tag to a json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether default values should be included as well.
        include_internals : `bool` = `False`, Optional (Keyword only)
            Whether we want to include identifiers as well.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        data = {}
        
        # id
        if include_internals:
            id_ = self.id
            if id_:
                data['id'] = str(id_)
        
        # emoji
        put_emoji_into(self.emoji, data, defaults)
        
        # name
        put_name_into(self.name, data, defaults)
        
        # moderated
        put_moderated_into(self.moderated, data, defaults)
        
        return data
    
    
    @property
    def partial(self):
        """
        Returns whether the forum tag is partial.
        
        Returns
        -------
        partial : `bool`
        """
        if self.id == 0:
            return True
        
        return False
