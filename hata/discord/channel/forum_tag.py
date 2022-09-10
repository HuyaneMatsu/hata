__all__ = ('ForumTag',)

from scarletio import copy_docs

from ..bases import DiscordEntity
from ..core import FORUM_TAGS
from ..emoji import Emoji, create_partial_emoji_from_data, put_partial_emoji_data_into
from ..preconverters import preconvert_snowflake

from .constants import FORUM_TAG_NAME_LENGTH_MAX, FORUM_TAG_NAME_LENGTH_MIN


def _assert__forum_tag__name(name):
    """
    Asserts the `name` parameter of ``ForumTag.__new__`` method.
    
    Parameters
    ----------
    name : `name`
        The tag's name.
    
    Raises
    ------
    AssertionError
        - If `name` is not `str`.
        - If `name`'s length is out of the expected range.
    """
    if not isinstance(name, str):
        raise AssertionError(
            f'`name` can be `str`, got {name.__class__.__name__}; {name!r}.'
        )
    
    name_length = len(name)
    if (name_length > FORUM_TAG_NAME_LENGTH_MAX) or (name_length < FORUM_TAG_NAME_LENGTH_MIN):
        raise AssertionError(
            f'`name` can be have length in range [{FORUM_TAG_NAME_LENGTH_MIN}:{FORUM_TAG_NAME_LENGTH_MAX}], got '
            f'{name_length!r}; {name!r}.'
        )
    
    return True


def _assert__forum_tag__emoji(emoji):
    """
    Asserts the `emoji` parameter of ``ForumTag.__new__`` method.
    
    Parameters
    ----------
    emoji : `None`, ``Emoji``
        The tag's emoji.
    
    Raises
    ------
    AssertionError
        - If `emoji` is not `None`, ``Emoji``.
    """
    if (emoji is not None) and (not isinstance(emoji, Emoji)):
        raise AssertionError(
            f'`emoji` can be `None`, `{Emoji.__name__}`, got {emoji.__class__.__name__}; {emoji!r}.'
        )
    
    return True


def _assert__forum_tag__moderated(moderated):
    """
    Asserts the `moderated` parameter of ``ForumTag.__new__`` method.
    
    Parameters
    ----------
    moderated : ``bool``
        Whether this tag can only be added or removed by a user with `manage_threads` permission.
    
    Raises
    ------
    AssertionError
        - If `moderated` is not `bool`.
    """
    if not isinstance(moderated, bool):
        raise AssertionError(
            f'`moderated` can be `bool`, got {moderated.__class__.__name__}; {moderated!r}.'
        )
    
    return True


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
    
    def __new__(cls, name, *, emoji=None, moderated=False):
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
        assert _assert__forum_tag__name(name)
        assert _assert__forum_tag__emoji(emoji)
        assert _assert__forum_tag__moderated(moderated)
        
        self = object.__new__(cls)
        self.id = 0
        self.emoji = emoji
        self.name = name
        self.moderated = moderated
        return self
    
    
    @copy_docs(DiscordEntity.__hash__)
    def __hash__(self):
        id_ = self.id
        if id_:
            return id_
        
        return self._get_hash_partial()
    
    
    def _get_hash_partial(self):
        """
        Hashes the fields of teh forum tag.
        
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
        other : `type<self>`
            The other instance. Must be from the same type.
        
        Returns
        -------
        is_equal : `bool`
        """
        # id_
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
            assert _assert__forum_tag__emoji(emoji)
        
        # name
        try:
            name = keyword_parameters.pop('name')
        except KeyError:
            name = self.name
        else:
            assert _assert__forum_tag__name(name)
        
        # moderated
        try:
            moderated = keyword_parameters.pop('moderated')
        except KeyError:
            moderated = self.moderated
        else:
            assert _assert__forum_tag__moderated(moderated)
        
        
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
                assert _assert__forum_tag__emoji(emoji)
                processable.append(('emoji', emoji))
            
            # name
            try:
                name = keyword_parameters.pop('name')
            except KeyError:
                pass
            else:
                assert _assert__forum_tag__name(name)
                processable.append(('name', name))
            
            # moderated
            try:
                moderated = keyword_parameters.pop('moderated')
            except KeyError:
                pass
            else:
                assert _assert__forum_tag__moderated(moderated)
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
        self.emoji = create_partial_emoji_from_data(data)
        
        # name
        self.name = data['name']
        
        # moderated
        self.moderated = data.get('moderated', False)
    
    
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
        emoji = create_partial_emoji_from_data(data)
        if (emoji is not self.emoji):
            old_attributes['emoji'] = self.emoji
            self.emoji = emoji
        
        # name
        name = data['name']
        if (name != self.name):
            old_attributes['name'] = self.name
            self.name = name
        
        # moderated
        moderated = data.get('moderated', False)
        if (moderated != self.moderated):
            old_attributes['moderated'] = self.moderated
            self.moderated = moderated
        
        return old_attributes
    
    
    def to_data(self):
        """
        Converts the forum tag to a json serializable object.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        data = {}
        
        # emoji
        put_partial_emoji_data_into(data, self.emoji)
        
        # name
        data['name'] = self.name
        
        # moderated
        data['moderated'] = self.moderated
        
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
