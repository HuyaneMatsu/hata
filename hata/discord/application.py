# -*- coding: utf-8 -*-
__all__ = ('Application', 'Team', 'TeamMember', 'TeamMembershipState', )

from .bases import DiscordEntity, IconSlot, ICON_TYPE_NONE
from .http import URLS
from .user import ZEROUSER, User
from .guild import PartialGuild
from .client_core import TEAMS

class Application(DiscordEntity):
    """
    Represents a Discord application with all of it's spice.
    
    When a ``Client`` is created, it starts it's life with an empty application by defualt. However when the client
    logs in, it's application is requested, but it can be updated by ``Client.update_application_info`` anytime.
    
    Attributes
    ----------
    bot_public : `bool`.
        Whether not only the application's owner can join the application's bot to guilds. Defaults to `False`
    bot_require_code_grant : `bool`
        Whether the application's bot will only join a guild, when completing the full `oauth2` code grant flow.
        Defaults to `False`.
    cover_hash : `int`
        The application's store cover image's hash in `uint128`. If the application is sold at Discord, this image
        will be used at the store.
    cover_type : `IconType`
        The application's store cover image's type.
    description : `str`
        The description of the application. Defaults to empty string.
    guild : `None` / ``Guild``
        If the application is a game sold on Discord, this field links it's respective guild. Defaults to `None`.
    icon_hash : `int`
        The application's icon's hash as `uint128`.
    icon_type : `IconType`
        The application's icon's type.
    id : `int`
        The application's id. Defaults to `0`. Meanwhile set as `0`, hashing the application will raise `RuntimeError`.
    name : `str`
        The name of the application. Defaults to empty string.
    owner : ``User``, ``Client`` or ``Team``
        The application's owner. Defaults to `ZEROUSER`
    primary_sku_id : `int`
        If the application is a game sold on Discord, this field will be the id of the created `Game SKU`.
        Defaults to `0`.
    rpc_origins : `list` of `str`
        A list of `rpc` origin urls, if `rpc` is enabled.
    slug : `str` or `None`
        If this application is a game sold on Discord, this field will be the url slug that links to the store page.
        Defaults to `None`.
    summary : `str`
        if this application is a game sold on Discord, this field will be the summary field for the store page of its
        primary sku. Defautls to empty string.
    verify_key : `str`
        A base64 encoded key for the GameSDK's `GetTicket`. Defaults to empty string.
    """
    __slots__ = ('bot_public', 'bot_require_code_grant', 'description', 'guild', 'name', 'owner', 'primary_sku_id',
        'rpc_origins', 'slug', 'summary', 'verify_key',)
    
    cover = IconSlot('cover', 'cover_image', URLS.application_cover_url, URLS.application_cover_url_as, add_updater=False)
    icon = IconSlot('icon', 'icon', URLS.application_icon_url, URLS.application_icon_url_as, add_updater=False)
    
    def __init__(self, data=None):
        """
        Creates an application. If no data is given creates a partial one.
        
        Parameters
        ----------
        data : `None` or `dict` of (`str`, `Any`) items, Optional
            Application data received from Discord or `None` to create a partial one.
        """
        if data is None:
            self._fillup()
        else:
            self(data)
    
    def __hash__(self):
        """Returns the application's hash value."""
        id_ = self.id
        if id_:
            return id_
        
        raise TypeError(f'Cannot hash partial {self.__class__.__name__} object.')
    
    @property
    def partial(self):
        """
        Returns whether the application is partial.
        
        An application if partial, if it's id is set as `0`.
        Returns
        -------
        partial : `bool`
        """
        return (self.id == 0)
    
    def __repr__(self):
        """Returns the application's representation"""
        result = [
            '<',
            self.__class__.__name__,
                ]
        
        id_ = self.id
        if id_:
            result.append(' id=')
            result.append(repr(id_))
            result.append(', name=')
            result.append(repr(self.name))
        else:
            result.append(' partial')
        
        result.append('>')
        
        return ''.join(result)
    
    def __str__(self):
        """Returns the application's name."""
        return self.name
    
    def _fillup(self):
        """
        Fills up the application with it's default attributes.
        """
        self.id=0
        self.name=''
        self.description=''
        self.rpc_origins=[]
        self.bot_public=False
        self.bot_require_code_grant=False
        self.owner=ZEROUSER
        self.summary=''
        self.verify_key=''
        self.guild=None
        self.primary_sku_id=0
        self.slug=None
        self.cover_hash = 0
        self.cover_type = ICON_TYPE_NONE
        self.icon_hash = 0
        self.icon_type = ICON_TYPE_NONE
    
    def __call__(self, data):
        """
        Updates the application with the data received from Discord.
        
        Parameters
        ----------
        data : `None` or `dict` of (`str`, `Any`) items
            Application data received from Discord.
        """
        self.id=int(data['id'])
        self.name=data['name']
        
        self.description=data['description']
        
        try:
            self.rpc_origins=data['rpc_origins']
        except KeyError:
            self.rpc_origins=[]
        
        self.bot_public=data['bot_public']
        self.bot_require_code_grant=data['bot_require_code_grant']
        self.summary=data['summary']
        self.verify_key=data['verify_key']
        
        #TODO: do we get owner data if we request other application ?
        team_data=data['team']
        self.owner=User(data['owner']) if team_data is None else Team(team_data)
        
        guild_id=data.get('guild_id',None)
        self.guild=None if guild_id is None else PartialGuild({'id':guild_id})
        
        primary_sku_id=data.get('primary_sku_id')
        self.primary_sku_id=0 if primary_sku_id is None else int(primary_sku_id)
        
        self.slug=data.get('slug',None)
        
        self._set_cover(data)
        self._set_icon(data)

class Team(DiscordEntity, immortal=True):
    """
    Represents a Team on the Discord developer protal.
    
    Attributes
    ----------
    id : `int`
        The unique identificator number of the team.
    icon_hash : `int`
        The team's icon's hash as `uint128`. Defaults to `0`.
    icon_type : `IconType`
        The team's icon's type.
    members : `list` of `TeamMember`
        The members of the team. Includes invited members as well.
    name : `str`
        The teams name.
    owner : ``User`` or ``Client``
        The team's owner.
    
    Notes
    -----
    Team objects support weakreferencig.
    """
    __slots__ = ('members', 'name', 'owner',)
    
    icon = IconSlot('icon', 'icon', URLS.team_icon_url, URLS.team_icon_url_as, add_updater = False)
    
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
        team_id=int(data['id'])
        try:
            team=TEAMS[team_id]
        except KeyError:
            team=object.__new__(cls)
            team.id=team_id
        
        #update every attribute
        team.name=data['name']
        
        team._set_icon(data)
        
        team.members = members = [TeamMember(team_member_data) for team_member_data in data['members']]
        owner_id=int(data['owner_user_id'])
        
        for member in members:
            user = member.user
            if user.id==owner_id:
                break
        else:
            user = ZEROUSER
        
        team.owner = user
        return team
    
    @property
    def invited(self):
        """
        A list of the invited users to the team.
        
        Returns
        -------
        users : `list` of (``User`` or ``Client``) objects
        """
        target_state=TeamMembershipState.INVITED
        return [team_member.user for team_member in self.members if team_member.state is target_state]
    
    @property
    def accepted(self):
        """
        A list of the users, who accepted their invite to the team.
        
        Returns
        -------
        users : `list` of (``User`` or ``Client``) objects
        """
        target_state=TeamMembershipState.ACCEPTED
        return [team_member.user for team_member in self.members if team_member.state is target_state]
    
    def __str__(self):
        """Returns the team's name."""
        return self.name
    
    def __repr__(self):
        """Returns the team's representation."""
        return f'<{self.__class__.__name__} owner={self.owner.full_name}, total count={len(self.members)}>'

class TeamMember(object):
    """
    Represents a team member of a ``Team``.
    
    Attributes
    ----------
    permissions : `list` of `str`
        The permissions of the team member. Right now specific permissions are not supported, so the list has only
        one element : `'*'`, what represents all the permissions.
    state : ``TeamMembershipState``
        The state of the team member. A member can be invited or can have the invite already accepted.
    user : ``User`` or ``Client``
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
        permissions=data['permissions']
        permissions.sort()
        self.permissions=permissions
        self.user=User(data['user'])
        self.state=TeamMembershipState.INSTANCES[data['membership_state']]
    
    def __repr__(self):
        """Returns the team member's representation."""
        return f'<{self.__class__.__name__} user={self.user.full_name} state={self.state.name} permissions={self.permissions}>'
    
    def __hash__(self):
        """Returns the team member's hash value, what is equal to it's user's id."""
        return self.user.id
    
    def __eq__(self, other):
        """Returns whether the two team member is equal"""
        if type(self) is not type(other):
            return False
        
        if (self.user != other.user):
            return False
        
        if (self.state is not other.state):
            return False
        
        if (self.permissions != other.permissions):
            return False
        
        return True

class TeamMembershipState(object):
    """
    Represents a ``TeamMemember``'s state at a ``Team``.
    
    Attributes
    ----------
    name : `str`
        The name of state.
    value : `int`
        The Discord side identificator value of the team membership state.
        
    Class Attributes
    ----------------
    INSTANCES : `list` of ``TeamMembershipState``
        Stores the created team membership state instances. This container is accessed when translating a Discord
        team membership state's value to it's representation.
    
    Every predefined team membership state can be accessed as class attribute as well:
    +-----------------------+-----------+-------+
    | Class attribute name  | name      | value |
    +=======================+===========+=======+
    | NONE                  | NONE      | 0     |
    +-----------------------+-----------+-------+
    | INVITED               | INVITED   | 1     |
    +-----------------------+-----------+-------+
    | ACCEPTED              | ACCEPTED  | 2     |
    +-----------------------+-----------+-------+
    """
    # class related
    INSTANCES = [NotImplemented] * 3
    
    # object related
    __slots__ = ('name', 'value',)
    
    def __init__(self,value,name):
        self.value=value
        self.name=name
        
        self.INSTANCES[value]=self
    
    def __int__(self):
        """Retruns the team membership state's value."""
        return self.value
    
    def __hash__(self):
        """Returns the hash value of the team mebership state, what equals to it's value."""
        return self.value
    
    def __str__(self):
        """Returns the team membership state's name."""
        return self.name
    
    def __repr__(self):
        """Returns the team membership state's representation."""
        return f'{self.__class__.__name__}(value={self.value}, name={self.name!r})'
    
    # predefined
    NONE    = None
    INVITED = None
    ACCEPTED= None

TeamMembershipState.NONE        = TeamMembershipState(0,'NONE')
TeamMembershipState.INVITED     = TeamMembershipState(1,'INVITED')
TeamMembershipState.ACCEPTED    = TeamMembershipState(2,'ACCEPTED')

del URLS
del DiscordEntity
del IconSlot
