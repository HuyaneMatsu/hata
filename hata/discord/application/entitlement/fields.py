__all__ = ()

from ...field_parsers import (
    bool_parser_factory, entity_id_parser_factory, nullable_date_time_parser_factory, preinstanced_parser_factory
)
from ...field_putters import (
    bool_optional_putter_factory, entity_id_optional_putter_factory, entity_id_putter_factory,
    nullable_date_time_optional_putter_factory, preinstanced_putter_factory
)
from ...field_validators import (
    bool_validator_factory, entity_id_array_validator_factory, entity_id_validator_factory,
    nullable_date_time_validator_factory, preinstanced_validator_factory
)
from ...guild import Guild
from ...user import ClientUserBase

from ..application import Application
from ..sku import SKU
from ..subscription import Subscription

from .preinstanced import EntitlementOwnerType, EntitlementType


# application_id

parse_application_id = entity_id_parser_factory('application_id')
put_application_id_into = entity_id_putter_factory('application_id')
validate_application_id = entity_id_validator_factory('application_id', Application)

# consumed

parse_consumed = bool_parser_factory('consumed', False)
put_consumed_into = bool_optional_putter_factory('consumed', False)
validate_consumed = bool_validator_factory('consumed', False)

# deleted

parse_deleted = bool_parser_factory('deleted', False)
put_deleted_into = bool_optional_putter_factory('deleted', False)
validate_deleted = bool_validator_factory('deleted', False)

# ends_at

parse_ends_at = nullable_date_time_parser_factory('ends_at')
put_ends_at_into = nullable_date_time_optional_putter_factory('ends_at')
validate_ends_at = nullable_date_time_validator_factory('ends_at')

# exclude_ended

validate_exclude_ended = bool_validator_factory('deleted', False)

# guild_id

parse_guild_id = entity_id_parser_factory('guild_id')
put_guild_id_into = entity_id_optional_putter_factory('guild_id')
validate_guild_id = entity_id_validator_factory('guild_id', Guild)

# id

parse_id = entity_id_parser_factory('id')
put_id_into = entity_id_putter_factory('id')
validate_id = entity_id_validator_factory('entitlement_id')

# owner

def put_owner_into(owner, data, defaults):
    """
    Serialises the entitlement's owner's type into the given data.
    
    Parameters
    ----------
    owner : `(EntitlementOwnerType, int)`
        The entitlement's owner represented by an ``EntitlementOwnerType`` and its identifier.
    data : `dict` of (`str`, `object`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `object`) items
    """
    put_owner_type_into(owner[0], data, defaults)
    put_owner_id_into(owner[1], data, defaults)
    return data


def validate_owner(owner):
    """
    Validates an entitlement's owner.
    
    Parameters
    ----------
    owner : `None`, ``ClientUserBase``, ``Guild``, `(int | EntitlementOwnerType, int | str)`
        The owner to validate.
    
    Returns
    -------
    owner : `(EntitlementOwnerType, int)`
    
    Raises
    ------
    TypeError
        - If `owner`'s type is incorrect.
    ValueError
        - If `owner`'s value is incorrect.
    """
    if owner is None:
        return EntitlementOwnerType.none, 0
    
    if isinstance(owner, Guild):
        return EntitlementOwnerType.guild, owner.id
    
    if isinstance(owner, ClientUserBase):
        return EntitlementOwnerType.user, owner.id
    
    if isinstance(owner, tuple):
        if len(owner) == 2:
            return validate_owner_type(owner[0]), validate_owner_id(owner[1])
        
        raise ValueError(
            f'When `owner` is given as a `tuple` its length must be `2`, got {len(owner)!r}; owner = {owner!r}.'
        )
    
    raise TypeError(
        f'`owner` can be `None`, `{ClientUserBase.__name__}`, `{Guild.__name__}` or a `tuple` of'
        f'`{EntitlementOwnerType.__name__}` and `int` representing it. Got {type(owner).__name__}; {owner!r}.'
    )


# owner_id

put_owner_id_into = entity_id_putter_factory('owner_id')
validate_owner_id = entity_id_validator_factory('owner_id')

# owner_type

put_owner_type_into = preinstanced_putter_factory('owner_type')
validate_owner_type = preinstanced_validator_factory('owner_type', EntitlementOwnerType)

# sku_id

parse_sku_id = entity_id_parser_factory('sku_id')
put_sku_id_into = entity_id_putter_factory('sku_id')
validate_sku_id = entity_id_validator_factory('sku_id', SKU)

# sku_ids

validate_sku_ids = entity_id_array_validator_factory('sku_ids', SKU)

# starts_at

parse_starts_at = nullable_date_time_parser_factory('starts_at')
put_starts_at_into = nullable_date_time_optional_putter_factory('starts_at')
validate_starts_at = nullable_date_time_validator_factory('starts_at')

# subscription_id

parse_subscription_id = entity_id_parser_factory('subscription_id')
put_subscription_id_into = entity_id_optional_putter_factory('subscription_id')
validate_subscription_id = entity_id_validator_factory('subscription_id', Subscription)

# type

parse_type = preinstanced_parser_factory('type', EntitlementType, EntitlementType.none)
put_type_into = preinstanced_putter_factory('type')
validate_type = preinstanced_validator_factory('entitlement_type', EntitlementType)

# user_id

parse_user_id = entity_id_parser_factory('user_id')
put_user_id_into = entity_id_optional_putter_factory('user_id')
validate_user_id = entity_id_validator_factory('user_id', ClientUserBase)
