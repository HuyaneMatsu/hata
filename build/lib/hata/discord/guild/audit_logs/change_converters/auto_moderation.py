__all__ = ()

from .shared import convert_nothing


def convert_str__triggered_rule_name(name, data):
    return convert_nothing('trigger_rule_name', data)


AUTO_MODERATION_CONVERTERS = {
    'triggered_rule_name': convert_str__triggered_rule_name,
}
