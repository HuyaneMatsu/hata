__all__ = ()

from .fields import (
    put_owner_id_into, put_owner_into, put_owner_type_into, put_sku_id_into, validate_owner, validate_owner_id,
    validate_owner_type, validate_sku_id
)


ENTITLEMENT_FIELD_CONVERTERS = {
    'owner': (validate_owner, put_owner_into),
    'owner_id': (validate_owner_id, put_owner_id_into),
    'owner_type': (validate_owner_type, put_owner_type_into),
    'sku': (validate_sku_id, put_sku_id_into),
    'sku_id': (validate_sku_id, put_sku_id_into),
}

