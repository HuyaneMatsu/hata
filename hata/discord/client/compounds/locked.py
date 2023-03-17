__all__ = ()

from scarletio import Compound, Theory

from ...application import Application
from ...bases import maybe_snowflake
from ...core import APPLICATIONS
from ...http import DiscordHTTPClient
from ...user import ClientUserBase, HypesquadHouse, RelationshipType
from ...utils import Relationship
from ..request_helpers import get_user_and_id, get_user_id


class ClientCompoundLockedEndpoints(Compound):
    
    http : DiscordHTTPClient
    
    @Theory
    async def user_get(self, user, *, force_update = False): ...
    
    
    async def relationship_delete(self, relationship):
        """
        Deletes the given relationship.
        
        This method is a coroutine.
        
        Parameters
        ----------
        relationship : ``Relationship``, ``ClientUserBase``, `int`
            The relationship to delete. Also can be given the respective user with who the client has the relationship
            with.

        Raises
        ------
        TypeError
            If `relationship` was not given neither as ``Relationship``, ``ClientUserBase`` not as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        This endpoint is available only for user accounts.
        """
        if isinstance(relationship, Relationship):
            user_id = relationship.user.id
        elif isinstance(relationship, ClientUserBase):
            user_id = relationship.id
        else:
            user_id = maybe_snowflake(relationship)
            if user_id is None:
                raise TypeError(
                    f'`relationship` can be `{Relationship.__name__}`, `{ClientUserBase.__name__}`, `int`, got '
                    f'{relationship.__class__.__name__}; {relationship!r}.'
                )
        
        await self.http.relationship_delete(user_id)
    
    
    async def relationship_create(self, user, relationship_type = None):
        """
        Creates a relationship with the given user.
        
        This method is a coroutine.
        
        Parameters
        ----------
        user : ```ClientUserBase``, `int`
            The user with who the relationship will be created.
        relationship_type : `None`, ``RelationshipType``, `int` = `None`, Optional
            The type of the relationship. Defaults to `None`.
        
        Raises
        ------
        TypeError
            - If `user` is not given neither as ``ClientUserBase``, `int`.
            - If `relationship_type` was not given neither as `None`, ``RelationshipType`` neither as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        This endpoint is available only for user accounts.
        """
        user_id = get_user_id(user)
        
        if relationship_type is None:
            relationship_type_value = None
        elif isinstance(relationship_type, RelationshipType):
            relationship_type_value = relationship_type.value
        elif isinstance(relationship_type, int):
            relationship_type_value = relationship_type
        else:
            raise TypeError(
                f'`relationship_type` can be `None`, `{RelationshipType.__name__}`, `int`'
                f', got {relationship_type.__class__.__name__}; {relationship_type!r}.'
            )
        
        data = {}
        if (relationship_type_value is not None):
            data['type'] = relationship_type_value
        
        await self.http.relationship_create(user_id, data)
    
    
    async def relationship_friend_request(self, user):
        """
        Sends a friend request to the given user.
        
        This method is a coroutine.
        
        Parameters
        ----------
        user : ```ClientUserBase``, `int`
            The user, who will receive the friend request.
        
        Raises
        ------
        TypeError
            If `user` was not given neither as ```ClientUserBase``, `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        This endpoint is available only for user accounts.
        """
        user, user_id = get_user_and_id(user)
        if (user is None):
            user = await self.user_get(user_id)
        
        data = {
            'username': user.name,
            'discriminator': str(user.discriminator)
        }
        
        await self.http.relationship_friend_request(data)


    async def hypesquad_house_change(self, house):
        """
        Changes the client's hypesquad house.
        
        This method is a coroutine.
        
        Parameters
        ----------
        house : `int`, ``HypesquadHouse``
            The hypesquad house to join.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Raises
        ------
        TypeError
            `house` was not given as `int`  neither as ``HypesquadHouse``.
        
        Notes
        -----
        User account only.
        """
        if isinstance(house, HypesquadHouse):
            house_id = house.value
        elif isinstance(house, int):
            house_id = house
        else:
            raise TypeError(
                f'`house` can be `int`, `{HypesquadHouse.__name__}`, got {house.__class__.__name__}; {house!r}.'
            )
        
        await self.http.hypesquad_house_change({'house_id': house_id})
    
    
    async def hypesquad_house_leave(self):
        """
        Leaves the client from it's current hypesquad house.
        
        This method is a coroutine.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        User account only.
        """
        await self.http.hypesquad_house_leave()


    async def application_get(self, application):
        """
        Requests a specific application by it's id.
        
        This method is a coroutine.
        
        Parameters
        ----------
        application : ``Application``, `int`
            The application or it's identifier to request.
        
        Returns
        -------
        application : ``Application``
        
        Raises
        ------
        TypeError
            If `application` was not given neither as ``Application`` nor as `int`.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        
        Notes
        -----
        This endpoint does not support bot accounts.
        """
        if isinstance(application, Application):
            application_id = application.id
        else:
            application_id = maybe_snowflake(application)
            if application_id is None:
                raise TypeError(
                    f'`application` can be `{Application.__name__}`, `int`, got '
                    f'{application.__class__.__name__}; {application!r}.'
                )
        
        application_data = await self.http.application_get(application_id)
        return Application.from_data_own(application_data)
