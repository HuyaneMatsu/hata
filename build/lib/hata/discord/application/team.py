__all__ = ('Team', 'TeamMember', )

from ..bases import DiscordEntity, IconSlot
from ..user import ZEROUSER, User, ClientUserBase
from ..core import TEAMS, USERS
from .preinstanced import TeamMembershipState

from ..http import urls as module_urls


class Team(DiscordEntity, immortal=True):
    """
    Represents a Team on the Discord developer portal.
    
    Attributes
    ----------
    id : `int`
        The unique identifier number of the team.
    icon_hash : `int`
        The team's icon's hash as `uint128`. Defaults to `0`.
    icon_type : `IconType`
        The team's icon's type.
    members : `list` of `TeamMember`
        The members of the team. Includes invited members as well.
    name : `str`
        The teams name.
    owner_id : `int`
        The team's owner's id.
    
    Notes
    -----
    Team objects support weakreferencing.
    """
    __slots__ = ('members', 'name', 'owner_id',)
    
    icon = IconSlot(
        'icon',
        'icon',
        module_urls.team_icon_url,
        module_urls.team_icon_url_as,
        add_updater = False,
    )
    
    def __new__(cls, data):
        """
        Creates a new ``Team`` instance from the data received from Discord.
        
        Parameters
        ----------
        data : `None` or `dict` of (`str`, `Any`) items
            Team data received from Discord.
        
        Returns
        -------
        team : ``Team``
        """
        team_id = int(data['id'])
        try:
            team = TEAMS[team_id]
        except KeyError:
            team = object.__new__(cls)
            team.id = team_id
        
        #update every attribute
        team.name = data['name']
        
        team._set_icon(data)
        
        team.members = [TeamMember(team_member_data) for team_member_data in data['members']]
        team.owner_id = int(data['owner_user_id'])
        return team
    
    @property
    def owner(self):
        """
        Returns the team's owner.
        
        Returns
        -------
        owner : ``ClientUserBase``
            Defaults to `ZEROUSER`.
        """
        owner_id = self.owner_id
        try:
            owner = USERS[owner_id]
        except KeyError:
            owner = ZEROUSER
        
        return owner
    
    @property
    def invited(self):
        """
        A list of the invited users to the team.
        
        Returns
        -------
        users : `list` of ``ClientUserBase``
        """
        target_state = TeamMembershipState.invited
        return [team_member.user for team_member in self.members if team_member.state is target_state]
    
    @property
    def accepted(self):
        """
        A list of the users, who accepted their invite to the team.
        
        Returns
        -------
        users : `list` of ``ClientUserBase``
        """
        target_state = TeamMembershipState.accepted
        return [team_member.user for team_member in self.members if team_member.state is target_state]
    
    
    def __repr__(self):
        """Returns the team's representation."""
        return f'<{self.__class__.__name__} owner={self.owner.full_name}, total members={len(self.members)}>'

class TeamMember:
    """
    Represents a team member of a ``Team``.
    
    Attributes
    ----------
    permissions : `list` of `str`
        The permissions of the team member. Right now specific permissions are not supported, so the list has only
        one element : `'*'`, what represents all the permissions.
    state : ``TeamMembershipState``
        The state of the team member. A member can be invited or can have the invite already accepted.
    user : ``ClientUserBase``
        The corresponding user account of the team member object.
    """
    __slots__ = ('permissions', 'state', 'user',)
    
    def __init__(self, data):
        """
        Creates a `TeamMember` object from the data sent by Discord.
        
        Parameters
        ----------
        data : `None` or `dict` of (`str`, `Any`) items
            Team member data received from Discord.
        """
        permissions = data['permissions']
        permissions.sort()
        self.permissions = permissions
        self.user = User(data['user'])
        self.state = TeamMembershipState.get(data['membership_state'])
    
    def __repr__(self):
        """Returns the team member's representation."""
        return (f'<{self.__class__.__name__} user={self.user.full_name} state={self.state.name} permissions='
            f'{self.permissions}>')
    
    def __hash__(self):
        """Returns the team member's hash value, what is equal to it's user's id."""
        return self.user.id
    
    def __eq__(self, other):
        """Returns whether the two team members are equal."""
        if type(self) is not type(other):
            return False
        
        if (self.user != other.user):
            return False
        
        if (self.state is not other.state):
            return False
        
        if (self.permissions != other.permissions):
            return False
        
        return True
