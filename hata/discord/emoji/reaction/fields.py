__all__ = ()

from ...field_validators import preinstanced_validator_factory

from .preinstanced import ReactionType


# type

validate_type = preinstanced_validator_factory('reaction_type', ReactionType)
