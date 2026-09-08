__all__ = ()

from ..field_validators import preinstanced_array_validator_factory, nullable_string_array_validator_factory

from .preinstanced import FileTypeFilterGroup


validate_groups = preinstanced_array_validator_factory('groups', FileTypeFilterGroup)

validate_individuals = nullable_string_array_validator_factory('individuals')
