__all__ = ()

from ...field_validators import entity_validator_factory

from ..oauth2_access import Oauth2Access

validate_access = entity_validator_factory('access', Oauth2Access)
