__all__ = ('PollResult',)

from scarletio import RichAttributeErrorBaseType

from .fields import (
    parse_answer_id, parse_count, put_answer_id, put_count, validate_answer_id, validate_count, validate_users
)


class PollResult(RichAttributeErrorBaseType):
    """
    Represents a poll's result for an answer.
    
    Attributes
    ----------
    answer_id : `int`
        The represented answer's identifier.
    
    count : `int`
        The amount of votes.
    
    users : ``None | set<ClientUserBase>``
        The known voters.
    """
    __slots__ = ('answer_id', 'count', 'users')
    
    def __new__(cls, *, answer_id = ..., count = ..., users = ...,):
        """
        Creates a poll result instance.
        
        Parameters
        ----------
        answer_id : `int`, Optional (Keyword only)
            The represented answer's identifier.
        
        count : `int`, Optional (Keyword only)
            The amount of votes.
        
        users : `None`, `iterable` of ``ClientUserBase``, Optional (Keyword only)
            The known voters.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # answer_id
        if answer_id is ...:
            answer_id = 0
        else:
            answer_id = validate_answer_id(answer_id)
        
        # count
        if count is ...:
            count = 0
        else:
            count = validate_count(count)
        
        # users
        if users is ...:
            users = None
        else:
            users = validate_users(users)
        
        # post-checks
        if (users is not None) and (len(users) > count):
            count = len(users)
        
        # Construct
        self = object.__new__(cls)
        self.answer_id = answer_id
        self.count = count
        self.users = users
        return self
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new poll result with the given data.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Executable data.
        """
        self = object.__new__(cls)
        self.answer_id = parse_answer_id(data)
        self.count = parse_count(data)
        self.users = None
        return self
    
    
    def to_data(self, *, defaults = False):
        """
        Converts the poll result to json serializable object.
        
        Parameters
        ----------
        defaults : `bool` = `False`, Optional (Keyword only)
            Whether fields with their default value should be included as well.
        
        Returns
        -------
        data : `dict<str, object>`
        """
        data = {}
        put_answer_id(self.answer_id, data, defaults)
        put_count(self.count, data, defaults)
        return data
    
    
    def __repr__(self):
        """Returns the count's representation."""
        repr_parts = ['<', type(self).__name__]
        
        # answer_od
        repr_parts.append(' answer_id = ')
        repr_parts.append(repr(self.answer_id))
        
        # count
        repr_parts.append(', count = ')
        repr_parts.append(repr(self.count))
        
        # users
        repr_parts.append(', users = ')
        repr_parts.append(repr(self.users))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two poll results are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        # answer_id
        if self.answer_id != other.answer_id:
            return False
        
        # count
        if self.count != other.count:
            return False
        
        # users
        length = len(self)
        if length != len(other) or (length != 0 and self.users != other.users):
            return False
        
        return True
    
    
    def __hash__(self):
        """Returns the count's hash."""
        hash_value = 0
        
        # answer_id
        hash_value ^= self.answer_id
        
        # count
        hash_value ^= self.count
        
        # users
        users = self.users
        if (users is not None):
            hash_value ^= len(users) << 4
            for user in users:
                hash_value ^= hash(user)
        
        return hash_value
    
    
    def copy(self):
        """
        Copies the poll result.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        new = object.__new__(type(self))
        
        new.answer_id = self.answer_id
        new.count = self.count
        
        users = self.users
        if (users is not None):
            users = users.copy()
        new.users = users
        
        return new
    
    
    def copy_with(self, *, answer_id = ..., count = ..., users = ...):
        """
        Copies the poll result with the given fields.
        
        Parameters
        ----------
        answer_id : `int`, Optional (Keyword only)
            The represented answer's identifier.
        
        count : `int`, Optional (Keyword only)
            The amount of votes.
        
        users : `None`, `iterable` of ``ClientUserBase``, Optional (Keyword only)
            The known voters.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's value is incorrect.
        """
        # answer_id
        if answer_id is ...:
            answer_id = self.answer_id
        else:
            answer_id = validate_answer_id(answer_id)
        
        # count
        if count is ...:
            count = self.count
        else:
            count = validate_count(count)
        
        # users
        if users is ...:
            users = self.users
            if (users is not None):
                users = users.copy()
        else:
            users = validate_users(users)
        
        # post-checks
        if (users is not None) and len(users) > count:
            count = len(users)
        
        # Construct
        new = object.__new__(type(self))
        new.answer_id = answer_id
        new.count = count
        new.users = users
        return new
    
    
    def __len__(self):
        """Returns the amount of known voters."""
        users = self.users
        if users is None:
            return 0
        
        return len(users)
    
    
    def __iter__(self):
        """Iterates over the known voters."""
        users = self.users
        if (users is not None):
            yield from users
    
    
    def __contains__(self, user):
        """Returns whether the given user is in the known votes."""
        users = self.users
        if (users is None):
            return False
        
        return user in users
    
    
    def _merge_with(self, other):
        """
        Merges the poll result with the other one.
        
        Always `other` is right and `other` should be empty.
        
        Parameters
        ----------
        other : `instance<type<self>>`
            Other instance.
        """
        new_count = other.count
        
        self_users = self.users
        other_users = other.users
        if self_users is None:
            if (other_users is not None):
                self_users = other_users.copy()
                self.users = self_users
        
        else:
            if self.count != new_count:
                self_users.clear()
                if (other_users is not None):
                    self_users.update(other_users)
            
            else:
                if (other_users is not None) and (not other_users.issubset(self_users)):
                    self_users.clear()
                    self_users.update(other_users)
            
        self.count = new_count
    
    
    @classmethod
    def _create_empty(cls, answer_id):
        """
        Creates an empty poll result.
        
        Parameters
        ----------
        answer_id : `int`
            The represented answer's identifier.
        
        Returns
        -------
        self : `instance<cls>`
        """
        self = object.__new__(cls)
        self.answer_id = answer_id
        self.count = 0
        self.users = None
        return self
    
    
    def _add_vote(self, user):
        """
        Adds a voter.
        
        Parameters
        ----------
        user : ``ClientUserBase``
            The user who voted.
        
        Returns
        -------
        success : `bool`
        """
        users = self.users
        if users is None:
            self.users = {user}
            self.count += 1
            return True
        
        old_length = len(users)
        users.add(user)
        new_length = len(users)
        if old_length == new_length:
            return False
        
        self.count += 1
        return True
    
    
    def _fill_some_votes(self, some_users):
        """
        Fills out some voters.
        
        Parameters
        ----------
        some_users : ``list<ClientUserBase>``
            The users who voted.
        """
        users = self.users
        if users is None:
            if some_users:
                users = {*some_users}
                self.users = users
        else:
            users.update(some_users)
        
        # This should not happen
        if (users is not None) and (self.count < len(users)):
            self.count = len(users)
    
    
    def _fill_all_votes(self, all_users):
        """
        Fills out all voters.
        
        Parameters
        ----------
        all_users : ``list<ClientUserBase>``
            The users who voted.
        """
        users = self.users
        if users is None:
            if all_users:
                users = {*all_users}
                self.users = users
        else:
            users.clear()
            users.update(all_users)
        
        # This should not happen
        user_count = 0 if users is None else len(users)
        if self.count != user_count:
            self.count = user_count
    
    
    def _remove_vote(self, user):
        """
        Removes a voter.
        
        Parameters
        ----------
        user : ``ClientUserBase``
            The user who removed their vote.
        
        Returns
        -------
        success : `bool`
        """
        users = self.users
        count = self.count
        
        if users is None:
            if count <= 0:
                return False
            
            self.count = count - 1
            return True
        
        old_length = len(users)
        users.discard(user)
        new_length = len(users)
        if old_length == new_length:
            count = self.count
            if count <= new_length:
                return False
            
            self.count = count - 1
            return True
        
        if count <= 0:
            return False
        
        self.count = count - 1
        return True
    
    
    @property
    def unknown(self):
        """
        Returns the amount of unknown voters.
        
        Returns
        -------
        unknown : `int`
        """
        count = self.count
        users = self.users
        if users is None:
            return count
        
        return count - len(users)
    
    
    def filter_after(self, limit, after):
        """
        If we know all the voters, then instead of executing a Discord API request we filter the voters locally
        using this method.
        
        Parameters
        ----------
        limit : `int`
            The maximal limit of the users to return.
        after : `int`
            Gets the users after this specified id.
        
        Returns
        -------
        users : ``list<ClientUserBase>``
        """
        users = self.users
        if users is None:
            return []
        
        filtered_users = [user for user in self if user.id > after]
        filtered_users.sort()
        del filtered_users[limit:]
        return filtered_users
    
    
    def iter_users(self):
        """
        Iterates over the known voters.
        
        This method is an iterable generator.
        
        Yields
        ------
        user : ``ClientUserBase``
        """
        users = self.users
        if (users is not None):
            yield from users
