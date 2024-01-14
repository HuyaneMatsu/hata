__all__ = ()

from scarletio import Compound

from ...application import Application, Entitlement, SKU
from ...application.entitlement.fields import (
    validate_exclude_ended as validate_entitlement_exclude_ended, validate_guild_id as validate_entitlement_guild_id,
    validate_sku_ids as validate_entitlement_sku_ids, validate_user_id as validate_entitlement_user_id
)
from ...application.entitlement.utils import ENTITLEMENT_FIELD_CONVERTERS
from ...http import DiscordApiClient
from ...payload_building import build_create_payload
from ...utils import log_time_converter

from ..request_helpers import get_entitlement_id


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
        owner : `None`, ``ClientUserBase``, ``Guild``, `(int | EntitlementOwnerType, int | str)`, Optional (Keyword only)
            The entitlement's owner. `owner_id` and `owner_type` combined.
        
        owner_id : `int`, Optional (Keyword only)
            The entitlement's owner's identifier.
        
        owner_type : ``EntitlementOwnerType``, `int`, Optional (Keyword only)
            The entitlement's owner's type.
        
        sku : `int`, ``SKU``, Optional (Keyword only)
            Alternative for `sku_id`.
        
        sku_id : `int`, ``SKU``, Optional (Keyword only)
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
    
    
    async def entitlement_get_all(self, *, exclude_ended = ..., guild_id = ..., sku_ids = ..., user_id = ...):
        """
        Requests all the entitlements of the client's application's entitlements that satisfies the criteria.
        
        This method is a coroutine.
        
        Parameters
        ----------
        exclude_ended : `bool`, Optional (Keyword only)
            Whether ended entitlements should be excluded. Defaults to `False`.
        
        guild_id : `int`, `None`, ``Guild``, Optional (Keyword only)
            Guild identifier to filter for.
        
        sku_ids : `int`, `None`, ``SKU``, `iterable` of `int`, `iterable` of ``SKU`, Optional (Keyword only)
            Stock keeping units to filter for.
        
        user_id : `int`, `None`, ``ClientUserBase``, Optional (Keyword only)
            User identifier to filter for.
        
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
        
        query_parameters = {
            'limit': 100,
            'after': 0,
        }
        
        if user_id is not ...:
            user_id = validate_entitlement_user_id(user_id)
            if user_id:
                query_parameters['user_id'] = user_id
        
        if guild_id is not ...:
            guild_id = validate_entitlement_guild_id(guild_id)
            if guild_id:
                query_parameters['guild_id'] = guild_id
        
        if exclude_ended is not ...:
            exclude_ended = validate_entitlement_exclude_ended(guild_id)
            if exclude_ended:
                query_parameters['exclude_ended'] = exclude_ended
        
        if sku_ids is not None:
            sku_ids = validate_entitlement_sku_ids(sku_ids)
            if sku_ids is not None:
                query_parameters['sku_ids'] = ','.join(str(sku_id) for sku_id in sku_ids)
        
        entitlements = []
        
        while True:
            entitlement_datas = await self.api.entitlement_get_chunk(application_id, query_parameters)
            for entitlement_data in entitlement_datas:
                entitlement = Entitlement.from_data(entitlement_data)
                entitlements.append(entitlement)
                
            if len(entitlement_datas) < 100:
                break
            
            query_parameters['after'] = entitlements[-1].id
            continue
        
        return entitlements
    
    
    async def entitlement_get_chunk(
        self,
        *,
        after = ...,
        before = ...,
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
        
        exclude_ended : `bool`, Optional (Keyword only)
            Whether ended entitlements should be excluded. Defaults to `False`.
        
        guild_id : `int`, `None`, ``Guild``, Optional (Keyword only)
            Guild identifier to filter for.
        
        limit : `int`, Optional (Keyword only)
            Up to how much entitlements should be requested. Can be in range `[1, 100]`. Defaults to `100`.
        
        sku_ids : `int`, `None`, ``SKU``, `iterable` of `int`, `iterable` of ``SKU`, Optional (Keyword only)
            Stock keeping units to filter for.
        
        user_id : `int`, `None`, ``ClientUserBase``, Optional (Keyword only)
            User identifier to filter for.
        
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
            limit = 100
        
        elif isinstance(limit, int):
            if limit < 1:
                limit = 1
            elif limit > 100:
                limit = 100
        
        else:
            raise TypeError(
                f'`limit` can be `None`, `int`, got {limit.__class__.__name__}; {limit!r}.'
            )
        
        query_parameters = {
            'limit': limit,
        }
        
        if (after is not ...):
            query_parameters['after'] = log_time_converter(after)
        
        if (before is not ...):
            query_parameters['before'] = log_time_converter(before)
        
        if exclude_ended is not ...:
            exclude_ended = validate_entitlement_exclude_ended(guild_id)
            if exclude_ended:
                query_parameters['exclude_ended'] = exclude_ended
        
        if guild_id is not ...:
            guild_id = validate_entitlement_guild_id(guild_id)
            if guild_id:
                query_parameters['guild_id'] = guild_id
        
        
        if sku_ids is not None:
            sku_ids = validate_entitlement_sku_ids(sku_ids)
            if sku_ids is not None:
                query_parameters['sku_ids'] = ','.join(str(sku_id) for sku_id in sku_ids)
            
        if user_id is not ...:
            user_id = validate_entitlement_user_id(user_id)
            if user_id:
                query_parameters['user_id'] = user_id
        
        entitlement_datas = await self.api.entitlement_get_chunk(application_id, query_parameters)
        return [Entitlement.from_data(entitlement_data) for entitlement_data in entitlement_datas]
    
    
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
