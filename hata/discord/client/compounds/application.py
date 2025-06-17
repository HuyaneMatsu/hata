__all__ = ()

from scarletio import Compound

from ...application import Application, Entitlement, SKU, Subscription
from ...application.entitlement.fields import (
    validate_exclude_deleted as validate_entitlement_exclude_deleted,
    validate_exclude_ended as validate_entitlement_exclude_ended, validate_guild_id as validate_entitlement_guild_id,
    validate_sku_ids as validate_entitlement_sku_ids, validate_user_id as validate_entitlement_user_id
)
from ...application.entitlement.utils import ENTITLEMENT_FIELD_CONVERTERS
from ...application.subscription.fields import (
    validate_sku_id as validate_subscription_sku_id, validate_user_id as validate_subscription_user_id
)
from ...embedded_activity import EmbeddedActivity
from ...http import DiscordApiClient
from ...payload_building import build_create_payload
from ...utils import log_time_converter

from ..request_helpers import (
    get_embedded_activity_and_id, get_entitlement_and_id, get_entitlement_id, get_subscription_and_sku_id_and_id
)

ENTITLEMENT_GET_CHUNK_LIMIT_MIN = 1
ENTITLEMENT_GET_CHUNK_LIMIT_MAX = 100


def _assert__application_id(application_id):
    """
    Asserts the the client's has `.application` synced by asserting whether it's value is not `0`.
    
    Parameters
    ----------
    application_id : `int`
        The client's application id.
    
    Raises
    ------
    AssertionError
        - If the client's application is not yet synced.
    """
    if application_id == 0:
        raise AssertionError(
            'The client\'s application is not yet synced.'
        )
    
    return True


class ClientCompoundApplicationEndpoints(Compound):
    
    api : DiscordApiClient
    application: Application
    
    
    async def entitlement_create(self, entitlement_template = None, **keyword_parameters):
        """
        Creates a new (test) entitlement.
        
        This method is a coroutine.
        
        Parameters
        ----------
        entitlement_template : `None`, ``Entitlement`` = `None`, Optional
            Entitlement to use as a template
        
        **keyword_parameters : Keyword parameters
            Additional keyword parameters either to define the template, or to overwrite specific fields' values.
        
        Other Parameters
        ----------------
        owner : ``None | ClientUserBase | Guild | (int | EntitlementOwnerType, int | str)``, Optional (Keyword only)
            The entitlement's owner. `owner_id` and `owner_type` combined.
        
        owner_id : `int`, Optional (Keyword only)
            The entitlement's owner's identifier.
        
        owner_type : ``EntitlementOwnerType``, `int`, Optional (Keyword only)
            The entitlement's owner's type.
        
        sku : ``int | SKU``, Optional (Keyword only)
            Alternative for `sku_id`.
        
        sku_id : ``int | SKU``, Optional (Keyword only)
            Stock keeping unit to create the entitlement for.
        
        Returns
        -------
        entitlement : ``Entitlement``
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        application_id = self.application.id
        assert _assert__application_id(application_id)
        
        data = build_create_payload(entitlement_template, ENTITLEMENT_FIELD_CONVERTERS, keyword_parameters)
        entitlement_data = await self.api.entitlement_create(application_id, data)
        return Entitlement.from_data(entitlement_data)
    
    
    async def entitlement_delete(self, entitlement):
        """
        Deletes the given (test) entitlement.
        
        This method is a coroutine.
        
        Parameters
        ----------
        entitlement : ``Entitlement``, `int`
            The entitlement to delete.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        application_id = self.application.id
        assert _assert__application_id(application_id)
        
        entitlement_id = get_entitlement_id(entitlement)
        await self.api.entitlement_delete(application_id, entitlement_id)
    
    
    async def entitlement_get_all(
        self, *, exclude_deleted = ..., exclude_ended = ..., guild_id = ..., sku_ids = ..., user_id = ...
    ):
        """
        Requests all the entitlements of the client's application's entitlements that satisfies the criteria.
        
        This method is a coroutine.
        
        Parameters
        ----------
        exclude_deleted : `bool`, Optional (Keyword only)
            Whether deleted entitlements should be excluded. Defaults to `False`.
        
        exclude_ended : `bool`, Optional (Keyword only)
            Whether ended entitlements should be excluded. Defaults to `False`.
        
        guild_id : `int`, `None`, ``Guild``, Optional (Keyword only)
            Guild identifier to filter for.
        
        sku_ids : ``None | int | SKU | iterable<int> | iterable<SKU>``, Optional (Keyword only)
            Stock keeping units to filter for.
        
        user_id : ``None | int | ClientUserBase``, Optional (Keyword only)
            User identifier to filter for.
        
        Returns
        -------
        entitlements : `list<Entitlement>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        application_id = self.application.id
        assert _assert__application_id(application_id)
        
        query_string_parameters = {
            'limit': ENTITLEMENT_GET_CHUNK_LIMIT_MAX,
            'after': 0,
        }
        
        if user_id is not ...:
            user_id = validate_entitlement_user_id(user_id)
            if user_id:
                query_string_parameters['user_id'] = user_id
        
        if guild_id is not ...:
            guild_id = validate_entitlement_guild_id(guild_id)
            if guild_id:
                query_string_parameters['guild_id'] = guild_id
        
        if exclude_deleted is not ...:
            exclude_deleted = validate_entitlement_exclude_deleted(exclude_deleted)
            if exclude_deleted:
                query_string_parameters['exclude_deleted'] = exclude_deleted
        
        if exclude_ended is not ...:
            exclude_ended = validate_entitlement_exclude_ended(exclude_ended)
            if exclude_ended:
                query_string_parameters['exclude_ended'] = exclude_ended
        
        if sku_ids is not ...:
            sku_ids = validate_entitlement_sku_ids(sku_ids)
            if sku_ids is not None:
                query_string_parameters['sku_ids'] = ','.join(str(sku_id) for sku_id in sku_ids)
        
        entitlements = []
        
        while True:
            entitlement_datas = await self.api.entitlement_get_chunk(application_id, query_string_parameters)
            for entitlement_data in entitlement_datas:
                entitlement = Entitlement.from_data(entitlement_data)
                entitlements.append(entitlement)
                
            if len(entitlement_datas) < ENTITLEMENT_GET_CHUNK_LIMIT_MAX:
                break
            
            query_string_parameters['after'] = entitlements[-1].id
            continue
        
        return entitlements
    
    
    async def entitlement_get_chunk(
        self,
        *,
        after = ...,
        before = ...,
        exclude_deleted = ...,
        exclude_ended = ...,
        guild_id = ...,
        limit = ...,
        sku_ids = ...,
        user_id = ...,
    ):
        """
        Requests a chunk of the client's application's entitlements that satisfies the criteria.
        
        This method is a coroutine.
        
        Parameters
        ----------
        after : `int`, ``DiscordEntity``, `datetime`, Optional (Keyword only)
            The timestamp after the entitlements were created.
        
        before : `int`, ``DiscordEntity``, `datetime`, Optional (Keyword only)
            The timestamp before the entitlements were created.
        
        exclude_deleted : `bool`, Optional (Keyword only)
            Whether deleted entitlements should be excluded. Defaults to `False`.
        
        exclude_ended : `bool`, Optional (Keyword only)
            Whether ended entitlements should be excluded. Defaults to `False`.
        
        guild_id : `int`, `None`, ``Guild``, Optional (Keyword only)
            Guild identifier to filter for.
        
        limit : `int`, Optional (Keyword only)
            Up to how much entitlements should be requested. Can be in range `[1, 100]`. Defaults to `100`.
        
        sku_ids : ``None | int | SKU | iterable<int> | iterable<SKU>``, Optional (Keyword only)
            Stock keeping units to filter for.
        
        user_id : ``None | int | ClientUserBase``, Optional (Keyword only)
            User identifier to filter for.
        
        Returns
        -------
        entitlements : `list<Entitlement>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        application_id = self.application.id
        assert _assert__application_id(application_id)
        
        if limit is ...:
            limit = ENTITLEMENT_GET_CHUNK_LIMIT_MAX
        
        elif isinstance(limit, int):
            if limit < ENTITLEMENT_GET_CHUNK_LIMIT_MIN:
                limit = ENTITLEMENT_GET_CHUNK_LIMIT_MIN
            elif limit > ENTITLEMENT_GET_CHUNK_LIMIT_MAX:
                limit = ENTITLEMENT_GET_CHUNK_LIMIT_MAX
        
        else:
            raise TypeError(
                f'`limit` can be `None | int`, got {type(limit).__name__}; {limit!r}.'
            )
        
        query_string_parameters = {
            'limit': limit,
        }
        
        if (after is not ...):
            query_string_parameters['after'] = log_time_converter(after)
        
        if (before is not ...):
            query_string_parameters['before'] = log_time_converter(before)
        
        if exclude_deleted is not ...:
            exclude_deleted = validate_entitlement_exclude_deleted(exclude_deleted)
            if exclude_deleted:
                query_string_parameters['exclude_deleted'] = exclude_deleted
        
        if exclude_ended is not ...:
            exclude_ended = validate_entitlement_exclude_ended(exclude_ended)
            if exclude_ended:
                query_string_parameters['exclude_ended'] = exclude_ended
        
        if guild_id is not ...:
            guild_id = validate_entitlement_guild_id(guild_id)
            if guild_id:
                query_string_parameters['guild_id'] = guild_id
        
        if sku_ids is not ...:
            sku_ids = validate_entitlement_sku_ids(sku_ids)
            if sku_ids is not None:
                query_string_parameters['sku_ids'] = ','.join(str(sku_id) for sku_id in sku_ids)
        
        if user_id is not ...:
            user_id = validate_entitlement_user_id(user_id)
            if user_id:
                query_string_parameters['user_id'] = user_id
        
        entitlement_datas = await self.api.entitlement_get_chunk(application_id, query_string_parameters)
        return [Entitlement.from_data(entitlement_data) for entitlement_data in entitlement_datas]
    
    
    async def entitlement_get(self, entitlement, *, force_update = False):
        """
        Requests the entitlement of the application.
        
        This method is a coroutine.
        
        Parameters
        ----------
        entitlement : ``Entitlement``, `int`
            The entitlement, or its identifier representing it.
        
        force_update : `bool` = `False`, Optional (Keyword only)
            Whether the entitlement should be requested even if it supposed to be up to date.
        
        Returns
        -------
        entitlement : ``Entitlement``
        
        Raises
        ------
        TypeError
            - If `entitlement` is given as incorrect type.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        application_id = self.application.id
        assert _assert__application_id(application_id)
        
        entitlement, entitlement_id = get_entitlement_and_id(entitlement)
        
        if (not force_update) and (entitlement is not None) and (not entitlement.partial):
            return entitlement
        
        entitlement_data = await self.api.entitlement_get(application_id, entitlement_id)
        
        if (entitlement is None):
            entitlement = Entitlement.from_data(entitlement_data)
        else:
            entitlement._set_attributes(entitlement_data)
        
        return entitlement
    
    
    async def entitlement_consume(self, entitlement):
        """
        Marks the one-time usage entitlement as consumed.
        
        This method is a coroutine.
        
        Parameters
        ----------
        entitlement : ``Entitlement``, `int`
            The entitlement to consume.
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        application_id = self.application.id
        assert _assert__application_id(application_id)
        
        entitlement_id = get_entitlement_id(entitlement)
        await self.api.entitlement_consume(application_id, entitlement_id)
    
    
    async def subscription_get_sku(self, subscription, *, force_update = False):
        """
        Requests an sku bound subscription.
        
        This method is a coroutine.
        
        Parameters
        ----------
        subscription : ``Subscription``, `(int, int)`
            The subscription to request or a tuple of 2 snowflakes (sku_id & subscription_id) representing it.
        
        force_update : `bool` = `False`, Optional (Keyword only)
            Whether the emoji should be requested even if it supposed to be up to date.
        
        Returns
        -------
        subscription : ``Subscription``
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        subscription, sku_id, subscription_id = get_subscription_and_sku_id_and_id(subscription)
                
        if (not force_update) and (subscription is not None) and (not subscription.partial):
            return subscription
        
        subscription_data = await self.api.subscription_get_sku(sku_id, subscription_id)
        
        if (subscription is None):
            subscription = Subscription.from_data(subscription_data)
        else:
            subscription._set_attributes(subscription_data)
        
        return subscription
    
    
    async def subscription_get_all_sku_user(self, sku, user):
        """
        Requests all the sku bound subscriptions of the client's application's for the given user.
        
        This method is a coroutine.
        
        Parameters
        ----------
        sku : ``int | SKU``
            Stock keeping unit to get subscriptions for.
        
        user : `int`, ``ClientUserBase``
            User to get the subscriptions for.
        
        Returns
        -------
        subscriptions : `list<Subscription>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        sku_id = validate_subscription_sku_id(sku)
        user_id = validate_subscription_user_id(user)
        
        query_string_parameters = {
            'limit': 100,
            'after': 0,
            'user_id': user_id,
        }
        
        subscriptions = []
        
        while True:
            subscription_datas = await self.api.subscription_get_chunk_sku_user(sku_id, query_string_parameters)
            for subscription_data in subscription_datas:
                subscription = Subscription.from_data(subscription_data)
                subscriptions.append(subscription)
                
            if len(subscription_datas) < 100:
                break
            
            query_string_parameters['after'] = subscriptions[-1].id
            continue
        
        return subscriptions
    
    
    async def subscription_get_chunk_sku_user(
        self,
        sku,
        user,
        *,
        after = ...,
        before = ...,
        limit = ...,
    ):
        """
        Requests a chunk of the sku bound subscriptions of the client's application's for the given user.
        
        This method is a coroutine.
        
        Parameters
        ----------
        sku : ``int | SKU``
            Stock keeping unit to get subscriptions for.
        
        user : `int`, ``ClientUserBase``
            User to get the subscriptions for.
        
        after : `int`, ``DiscordEntity``, `datetime`, Optional (Keyword only)
            The timestamp after the subscriptions were created.
        
        before : `int`, ``DiscordEntity``, `datetime`, Optional (Keyword only)
            The timestamp before the subscriptions were created.
        
        limit : `int`, Optional (Keyword only)
            Up to how much subscriptions should be requested. Can be in range `[1, 100]`. Defaults to `100`.
        
        Returns
        -------
        subscriptions : `list<Subscription>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is incorrect.
        ValueError
            - If a parameter's type is incorrect.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        sku_id = validate_subscription_sku_id(sku)
        user_id = validate_subscription_user_id(user)
        
        if limit is ...:
            limit = 100
        
        elif isinstance(limit, int):
            if limit < 1:
                limit = 1
            elif limit > 100:
                limit = 100
        
        else:
            raise TypeError(
                f'`limit` can be `None | int`, got {type(limit).__name__}; {limit!r}.'
            )
        
        query_string_parameters = {
            'limit': limit,
            'user_id': user_id,
        }
        
        if (after is not ...):
            query_string_parameters['after'] = log_time_converter(after)
        
        if (before is not ...):
            query_string_parameters['before'] = log_time_converter(before)
        
        subscription_datas = await self.api.subscription_get_chunk_sku_user(sku_id, query_string_parameters)
        return [Subscription.from_data(subscription_data) for subscription_data in subscription_datas]
    
    
    async def sku_get_all(self):
        """
        Requests the client's application's stock keeping unit.
        
        This method is a coroutine.
        
        Returns
        -------
        skus : `list` of ``SKU`
            The received stock keeping units.
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        application_id = self.application.id
        assert _assert__application_id(application_id)
        
        sku_datas = await self.api.sku_get_all(application_id)
        return [SKU.from_data(sku_data) for sku_data in sku_datas]
    
    
    async def embedded_activity_get(self, embedded_activity, *, force_update = False):
        """
        Requests the embedded activity of the application.
        
        This method is a coroutine.
        
        Parameters
        ----------
        embedded_activity : ``EmbeddedActivity``, `(int, int)`
            The embedded activity, or its identifier representing it.
        
        force_update : `bool` = `False`, Optional (Keyword only)
            Whether the embedded_activity should be requested even if it supposed to be up to date.
        
        Returns
        -------
        embedded_activity : ``EmbeddedActivity``
        
        Raises
        ------
        TypeError
            - If `embedded_activity` is given as incorrect type.
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        application_id = self.application.id
        assert _assert__application_id(application_id)
        
        embedded_activity, embedded_activity_id = get_embedded_activity_and_id(embedded_activity)
        
        if (not force_update) and (embedded_activity is not None) and (not embedded_activity.partial):
            return embedded_activity
        
        embedded_activity_data = await self.api.embedded_activity_get(application_id, embedded_activity_id)
        
        if (embedded_activity is None):
            embedded_activity = EmbeddedActivity.from_data(embedded_activity_data)
        else:
            embedded_activity._set_attributes(embedded_activity_data, False, 0)
        
        return embedded_activity
