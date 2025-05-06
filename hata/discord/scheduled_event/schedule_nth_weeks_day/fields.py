__all__ = ()

from ...field_parsers import int_parser_factory, preinstanced_parser_factory
from ...field_putters import int_putter_factory, preinstanced_putter_factory
from ...field_validators import int_conditional_validator_factory, preinstanced_validator_factory

from .preinstanced import ScheduleWeeksDay


# nth_week

parse_nth_week = int_parser_factory('n', 1)
put_nth_week = int_putter_factory('n')
validate_nth_week = int_conditional_validator_factory(
    'nth_week',
    1,
    (lambda nth_week : nth_week >= 1 and nth_week <= 5),
    '>= 1 and <= 5',
)


# day

parse_weeks_day = preinstanced_parser_factory('day', ScheduleWeeksDay, ScheduleWeeksDay.monday)
put_weeks_day = preinstanced_putter_factory('day')
validate_weeks_day = preinstanced_validator_factory('weeks_day', ScheduleWeeksDay)
