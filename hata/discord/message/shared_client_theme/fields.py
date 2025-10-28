__all__ = ()

from ...color import Color
from ...field_parsers import int_parser_factory, nullable_functional_array_parser_factory, preinstanced_parser_factory
from ...field_putters import int_putter_factory, nullable_functional_array_optional_putter_factory, preinstanced_putter_factory
from ...field_validators import int_conditional_validator_factory, nullable_object_array_validator_factory, preinstanced_validator_factory

from .constants import GRADIENT_ANGLE_MAX, GRADIENT_ANGLE_MIN, INTENSITY_MAX, INTENSITY_MIN
from .preinstanced import SharedClientThemeBaseTheme


# base_theme

parse_base_theme = preinstanced_parser_factory(
    'base_theme', SharedClientThemeBaseTheme, SharedClientThemeBaseTheme.none
)
put_base_theme = preinstanced_putter_factory('base_theme')
validate_base_theme = preinstanced_validator_factory('base_theme', SharedClientThemeBaseTheme)


# colors

parse_colors = nullable_functional_array_parser_factory('colors', lambda value : Color(value, 16))
put_colors = nullable_functional_array_optional_putter_factory('colors', lambda color : format(color, 'X'))
validate_colors = nullable_object_array_validator_factory('colors', Color)


# gradient_angle

parse_gradient_angle = int_parser_factory('gradient_angle', GRADIENT_ANGLE_MIN)
put_gradient_angle = int_putter_factory('gradient_angle')
validate_gradient_angle = int_conditional_validator_factory(
    'gradient_angle',
    GRADIENT_ANGLE_MIN,
    (lambda gradient_angle : gradient_angle >= GRADIENT_ANGLE_MIN and gradient_angle <= GRADIENT_ANGLE_MAX),
    f'>= {GRADIENT_ANGLE_MIN} and <= {GRADIENT_ANGLE_MAX}',
)


# intensity

parse_intensity = int_parser_factory('base_mix', INTENSITY_MIN)
put_intensity = int_putter_factory('base_mix')
validate_intensity = int_conditional_validator_factory(
    'intensity',
    INTENSITY_MIN,
    (lambda intensity : intensity >= INTENSITY_MIN and intensity <= INTENSITY_MAX),
    f'>= {INTENSITY_MIN} and <= {INTENSITY_MAX}',
)
