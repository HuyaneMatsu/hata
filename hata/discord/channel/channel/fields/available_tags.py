__all__ = ()

from ....field_parsers import nullable_entity_array_parser_factory
from ....field_putters import nullable_entity_array_optional_putter_factory
from ....field_validators import nullable_entity_array_validator_factory

from ...forum_tag import ForumTag


parse_available_tags = nullable_entity_array_parser_factory('available_tags', ForumTag)
put_available_tags_into = nullable_entity_array_optional_putter_factory('available_tags')
validate_available_tags = nullable_entity_array_validator_factory('available_tags', ForumTag)
