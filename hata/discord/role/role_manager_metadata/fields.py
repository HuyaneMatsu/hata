__all__ = ()

from ...field_parsers import entity_id_parser_factory
from ...field_putters import entity_id_optional_putter_factory
from ...field_validators import bool_validator_factory, entity_id_validator_factory
from ...user import ClientUserBase

from .constants import BOT_ID_KEY, INTEGRATION_ID_KEY, PURCHASABLE_KEY, SUBSCRIPTION_LISTING_ID_KEY

# bot_id

parse_bot_id = entity_id_parser_factory(BOT_ID_KEY)
put_bot_id_into = entity_id_optional_putter_factory(BOT_ID_KEY)
validate_bot_id = entity_id_validator_factory('bot_id', ClientUserBase)

# integration_id

parse_integration_id = entity_id_parser_factory(INTEGRATION_ID_KEY)
put_integration_id_into = entity_id_optional_putter_factory(INTEGRATION_ID_KEY)
validate_integration_id = entity_id_validator_factory('integration_id', NotImplemented, include = 'Integration')

# purchasable

def parse_purchasable(data):
    """
    Parses whether the role is available for purchase.
    
    Parameters
    ----------
    data : `dict` of (`str`, `object`) items
        Role manager data.
    
    Returns
    -------
    purchasable : `bool`
    """
    return PURCHASABLE_KEY in data


def put_purchasable_into(purchasable, data, defaults):
    """
    Puts the given `purchasable` value in the given role manager data.
    
    Parameters
    ----------
    purchasable : `bool`
        Whether the role is available for purchase.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    if purchasable:
        data[PURCHASABLE_KEY] = None
    
    return data

validate_purchasable = bool_validator_factory('purchasable')

# subscription_listing_id

parse_subscription_listing_id = entity_id_parser_factory(SUBSCRIPTION_LISTING_ID_KEY)
put_subscription_listing_id_into = entity_id_optional_putter_factory(SUBSCRIPTION_LISTING_ID_KEY)
validate_subscription_listing_id = entity_id_validator_factory('subscription_listing_id')
