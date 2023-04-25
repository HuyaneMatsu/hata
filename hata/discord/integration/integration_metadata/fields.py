__all__ = ()

from scarletio import include


from ...field_parsers import (
    bool_parser_factory, default_entity_parser_factory, entity_id_parser_factory, int_parser_factory,
    nullable_date_time_parser_factory, nullable_entity_parser_factory, preinstanced_array_parser_factory,
    preinstanced_parser_factory
)
from ...field_putters import (
    bool_optional_putter_factory, entity_id_optional_putter_factory, entity_putter_factory, int_optional_putter_factory,
    nullable_date_time_optional_putter_factory, nullable_entity_putter_factory, preinstanced_array_putter_factory,
    preinstanced_putter_factory
)
from ...field_validators import (
    bool_validator_factory, default_entity_validator, entity_id_validator_factory, entity_validator_factory,
    int_conditional_validator_factory, int_options_validator_factory, nullable_date_time_validator_factory,
    nullable_entity_validator_factory, preinstanced_array_validator_factory, preinstanced_validator_factory
)
from ...oauth2 import Oauth2Scope
from ...role import Role
from ...user import ClientUserBase, User

from ..integration_account import IntegrationAccount
from ..integration_application import IntegrationApplication

from .constants import EXPIRE_GRACE_PERIOD_DEFAULT, EXPIRE_GRACE_PERIOD_OPTIONS, SUBSCRIBER_COUNT_DEFAULT
from .preinstanced import IntegrationExpireBehavior


IntegrationType = include('IntegrationType')

# account

parse_account = default_entity_parser_factory(
    'account', IntegrationAccount, default_factory = lambda : IntegrationAccount._create_empty()
)
put_account_into = entity_putter_factory('account', IntegrationAccount)
validate_account = default_entity_validator(
    'account', IntegrationAccount, default_factory = lambda : IntegrationAccount._create_empty()
)

# account [discord]

def parse_account__discord(data):
    """
    Parses out an integration account of a Discord integration out from the given data.
    
    Parameters
    ----------
    data : `dict` of (`str`, `Any`) items
        Integration account data.
    
    Returns
    -------
    integration_account : ``ClientUserBase``
    """
    account_data = data.get('account', None)
    if (account_data is None):
        return IntegrationAccount._create_empty()
    
    user_id = int(account_data['id'])
    name = account_data['name']
    
    return User.precreate(user_id, name = name, bot = True)


def put_account_into__discord(account, data, defaults):
    """
    Serialises the given discord integration account into the given `data`.
    
    Parameters
    ----------
    account : ``ClientUserBase``
        Integration account of a discord integration.
    data : `dict` of (`str`, `Any`) items
        Json serializable dictionary.
    defaults : `bool`
        Whether default fields should be included as well.
    
    Returns
    -------
    data : `dict` of (`str`, `Any`) items
    """
    data['account'] = {
        'id': str(account.id),
        'name': account.name,
    }
    
    return data

validate_account__discord = entity_validator_factory('account', ClientUserBase)

# application

parse_application = nullable_entity_parser_factory('application', IntegrationApplication)
put_application_into = nullable_entity_putter_factory('application', IntegrationApplication)
validate_application = nullable_entity_validator_factory('application', IntegrationApplication)

# scopes

parse_scopes = preinstanced_array_parser_factory('scopes', Oauth2Scope)
put_scopes_into = preinstanced_array_putter_factory('scopes')
validate_scopes = preinstanced_array_validator_factory('scopes', Oauth2Scope)

# expire_behavior

parse_expire_behavior = preinstanced_parser_factory(
    'expire_behavior', IntegrationExpireBehavior, IntegrationExpireBehavior.remove_role,
)
put_expire_behavior_into = preinstanced_putter_factory('expire_behavior')
validate_expire_behavior = preinstanced_validator_factory('expire_behavior', IntegrationExpireBehavior)

# expire_grace_period

parse_expire_grace_period = int_parser_factory('expire_grace_period', EXPIRE_GRACE_PERIOD_DEFAULT)
put_expire_grace_period_into = int_optional_putter_factory('expire_grace_period', EXPIRE_GRACE_PERIOD_DEFAULT)
validate_expire_grace_period = int_options_validator_factory('expire_grace_period', EXPIRE_GRACE_PERIOD_OPTIONS)

# revoked

parse_revoked = bool_parser_factory('revoked', False)
put_revoked_into = bool_optional_putter_factory('revoked', False)
validate_revoked = bool_validator_factory('revoked', False)

# role_id

parse_role_id = entity_id_parser_factory('role_id')
put_role_id_into = entity_id_optional_putter_factory('role_id')
validate_role_id = entity_id_validator_factory('role_id', Role)

# subscriber_count

parse_subscriber_count = int_parser_factory('subscriber_count', SUBSCRIBER_COUNT_DEFAULT)
put_subscriber_count_into = int_optional_putter_factory('subscriber_count', SUBSCRIBER_COUNT_DEFAULT)
validate_subscriber_count = int_conditional_validator_factory(
    'subscriber_count', 0, lambda integer: integer >= SUBSCRIBER_COUNT_DEFAULT, 'positive'
)

# synced_at

parse_synced_at = nullable_date_time_parser_factory('synced_at')
put_synced_at_into = nullable_date_time_optional_putter_factory('synced_at')
validate_synced_at = nullable_date_time_validator_factory('synced_at')

# syncing

parse_syncing = bool_parser_factory('syncing', False)
put_syncing_into = bool_optional_putter_factory('syncing', False)
validate_syncing = bool_validator_factory('syncing', False)
