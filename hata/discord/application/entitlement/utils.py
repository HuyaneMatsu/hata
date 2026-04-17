__all__ = ()

from .fields import (
    put_owner_id, put_owner, put_owner_type, put_sku_id, validate_owner, validate_owner_id,
    validate_owner_type, validate_sku_id
)


ENTITLEMENT_FIELD_CONVERTERS = {
    'owner': (validate_owner, put_owner),
    'owner_id': (validate_owner_id, put_owner_id),
    'owner_type': (validate_owner_type, put_owner_type),
    'sku': (validate_sku_id, put_sku_id),
    'sku_id': (validate_sku_id, put_sku_id),
}

