__all__ = ()

from ...field_parsers import (
    bool_parser_factory, entity_id_parser_factory, flag_parser_factory, nullable_date_time_parser_factory,
    nullable_entity_parser_factory, preinstanced_parser_factory
)
from ...field_putters import (
    bool_optional_putter_factory, entity_id_optional_putter_factory, entity_id_putter_factory,
    flag_optional_putter_factory, nullable_date_time_optional_putter_factory, nullable_entity_optional_putter_factory,
    preinstanced_putter_factory
)
from ...field_validators import (
    bool_validator_factory, entity_id_array_validator_factory, entity_id_validator_factory,
    flag_validator_factory, nullable_date_time_validator_factory, nullable_entity_validator_factory,
    preinstanced_validator_factory
)
from ...guild import Guild
from ...user import ClientUserBase

from ..application import Application
from ..sku import SKU
from ..subscription import Subscription

from .flags import GiftCodeFlag
from .preinstanced import EntitlementOwnerType, EntitlementSourceType, EntitlementType


# application_id

parse_application_id = entity_id_parser_factory('application_id')
put_application_id = entity_id_putter_factory('application_id')
validate_application_id = entity_id_validator_factory('application_id', Application)

# consumed

parse_consumed = bool_parser_factory('consumed', False)
put_consumed = bool_optional_putter_factory('consumed', False)
validate_consumed = bool_validator_factory('consumed', False)

# deleted

parse_deleted = bool_parser_factory('deleted', False)
put_deleted = bool_optional_putter_factory('deleted', False)
validate_deleted = bool_validator_factory('deleted', False)

# ends_at

parse_ends_at = nullable_date_time_parser_factory('ends_at')
put_ends_at = nullable_date_time_optional_putter_factory('ends_at')
validate_ends_at = nullable_date_time_validator_factory('ends_at')

# exclude_deleted

validate_exclude_deleted = bool_validator_factory('exclude_deleted', False)

# exclude_ended

validate_exclude_ended = bool_validator_factory('exclude_ended', False)


# gift_code_flags

parse_gift_code_flags = flag_parser_factory('gift_code_flags', GiftCodeFlag)
put_gift_code_flags = flag_optional_putter_factory('gift_code_flags', GiftCodeFlag())
validate_gift_code_flags = flag_validator_factory('gift_code_flags', GiftCodeFlag)


# guild_id

parse_guild_id = entity_id_parser_factory('guild_id')
put_guild_id = entity_id_optional_putter_factory('guild_id')
validate_guild_id = entity_id_validator_factory('guild_id', Guild)

# id

parse_id = entity_id_parser_factory('id')
put_id = entity_id_putter_factory('id')
validate_id = entity_id_validator_factory('entitlement_id')

# owner

def put_owner(owner, data, defaults):
    """
    Serialises the entitlement's owner's type into the given data.
    
    Parameters
    ----------
    owner : ``(EntitlementOwnerType, int)``
        The entitlement's owner represented by an ``EntitlementOwnerType`` and its identifier.
    
    data : `dict<str, object>`
        Json serializable dictionary.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    put_owner_type(owner[0], data, defaults)
    put_owner_id(owner[1], data, defaults)
    return data


def validate_owner(owner):
    """
    Validates an entitlement's owner.
    
    Parameters
    ----------
    owner : ``None | ClientUserBase | Guild | (int | EntitlementOwnerType, int | str)``
        The owner to validate.
    
    Returns
    -------
    owner : ``(EntitlementOwnerType, int)``
    
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

put_owner_id = entity_id_putter_factory('owner_id')
validate_owner_id = entity_id_validator_factory('owner_id')


# owner_type

put_owner_type = preinstanced_putter_factory('owner_type')
validate_owner_type = preinstanced_validator_factory('owner_type', EntitlementOwnerType)


# promotion_id

parse_promotion_id = entity_id_parser_factory('promotion_id')
put_promotion_id = entity_id_optional_putter_factory('promotion_id')
validate_promotion_id = entity_id_validator_factory('promotion_id')


# sku

parse_sku = nullable_entity_parser_factory('sku', SKU)
put_sku = nullable_entity_optional_putter_factory('sku', SKU, force_include_internals = True)
validate_sku = nullable_entity_validator_factory('sku', SKU)

# sku_id

parse_sku_id = entity_id_parser_factory('sku_id')
put_sku_id = entity_id_putter_factory('sku_id')
validate_sku_id = entity_id_validator_factory('sku_id', SKU)


# sku_ids

validate_sku_ids = entity_id_array_validator_factory('sku_ids', SKU)


# source_type

parse_source_type = preinstanced_parser_factory('source_type', EntitlementSourceType, EntitlementSourceType.none)
put_source_type = preinstanced_putter_factory('source_type')
validate_source_type = preinstanced_validator_factory('source_type', EntitlementSourceType)


# starts_at

parse_starts_at = nullable_date_time_parser_factory('starts_at')
put_starts_at = nullable_date_time_optional_putter_factory('starts_at')
validate_starts_at = nullable_date_time_validator_factory('starts_at')


# subscription_id

parse_subscription_id = entity_id_parser_factory('subscription_id')
put_subscription_id = entity_id_optional_putter_factory('subscription_id')
validate_subscription_id = entity_id_validator_factory('subscription_id', Subscription)


# type

parse_type = preinstanced_parser_factory('type', EntitlementType, EntitlementType.none)
put_type = preinstanced_putter_factory('type')
validate_type = preinstanced_validator_factory('entitlement_type', EntitlementType)


# user_id

parse_user_id = entity_id_parser_factory('user_id')
put_user_id = entity_id_optional_putter_factory('user_id')
validate_user_id = entity_id_validator_factory('user_id', ClientUserBase)
