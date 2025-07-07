import vampytest

from ....bases import Icon
from ....color import Color
from ....core import BUILTIN_EMOJIS
from ....permission import Permission
from ....permission.constants import PERMISSION_KEY
from ....role import RoleColorConfiguration, RoleFlag
from ....role.role.fields import (
    validate_color, validate_color_configuration, validate_flags, validate_mentionable, validate_name,
    validate_permissions, validate_position, validate_separated, validate_unicode_emoji
)
from ....role.role.role import ROLE_ICON

from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversion import (
    _assert_fields_set as _assert_conversion_fields_set
)
from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversionGroup import (
    _assert_fields_set as _assert_conversion_group_fields_set
)
from ...conversion_helpers.converters import value_deserializer_name, value_serializer_name

from ..role import (
    COLOR_CONVERSION, COLOR_CONFIGURATION_CONVERSION, FLAGS_CONVERSION, ICON_CONVERSION, MENTIONABLE_CONVERSION,
    NAME_CONVERSION, PERMISSIONS_CONVERSION, POSITION_CONVERSION, ROLE_CONVERSIONS, SEPARATED_CONVERSION,
    UNICODE_EMOJI_CONVERSION
)


def test__ROLE_CONVERSIONS():
    """
    Tests whether `ROLE_CONVERSIONS` contains conversion for every expected key.
    """
    _assert_conversion_group_fields_set(ROLE_CONVERSIONS)
    vampytest.assert_eq(
        {*ROLE_CONVERSIONS.iter_field_keys()},
        {
            'color', 'colors', 'flags', 'icon_hash', 'mentionable', 'name', PERMISSION_KEY, 'position', 'hoist',
            'unicode_emoji'
        },
    )


# ---- color ----

def test__COLOR_CONVERSION__generic():
    """
    Tests whether ``COLOR_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(COLOR_CONVERSION)
    # vampytest.assert_is(COLOR_CONVERSION.value_deserializer, )
    # vampytest.assert_is(COLOR_CONVERSION.value_serializer, )
    vampytest.assert_is(COLOR_CONVERSION.value_validator, validate_color)


def _iter_options__color__value_deserializer():
    yield 60, Color(60)
    yield 0, Color()
    yield None, Color()


@vampytest._(vampytest.call_from(_iter_options__color__value_deserializer()).returning_last())
def test__COLOR_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `COLOR_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``Color``
    """
    output = COLOR_CONVERSION.value_deserializer(input_value)
    vampytest.assert_instance(output, Color)
    return output


def _iter_options__color__value_serializer():
    yield Color(60), 60
    yield Color(), 0


@vampytest._(vampytest.call_from(_iter_options__color__value_serializer()).returning_last())
def test__COLOR_CONVERSION__value_serializer(input_value):
    """
    Tests whether `COLOR_CONVERSION.value_serializer` works as intended.
    
    Parameters
    ----------
    input_value : ``Color``
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    output = COLOR_CONVERSION.value_serializer(input_value)
    vampytest.assert_instance(output, int, accept_subtypes = False)
    return output


# ---- color_configuration ----

def test__COLOR_CONFIGURATION_CONVERSION__generic():
    """
    Tests whether ``COLOR_CONFIGURATION_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(COLOR_CONFIGURATION_CONVERSION)
    # vampytest.assert_is(COLOR_CONFIGURATION_CONVERSION.value_deserializer, )
    # vampytest.assert_is(COLOR_CONFIGURATION_CONVERSION.value_serializer, )
    vampytest.assert_is(COLOR_CONFIGURATION_CONVERSION.value_validator, validate_color_configuration)


def _iter_options__color_configuration__value_deserializer():
    color_configuration = RoleColorConfiguration(
        color_primary = Color(222),
        color_secondary = Color(233),
        color_tertiary = Color(244),
    )
    
    yield color_configuration.to_data(), color_configuration
    yield None, RoleColorConfiguration.create_empty()


@vampytest._(vampytest.call_from(_iter_options__color_configuration__value_deserializer()).returning_last())
def test__COLOR_CONFIGURATION_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `COLOR_CONFIGURATION_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``RoleColorConfiguration``
    """
    output = COLOR_CONFIGURATION_CONVERSION.value_deserializer(input_value)
    vampytest.assert_instance(output, RoleColorConfiguration)
    return output


def _iter_options__color_configuration__value_serializer():
    color_configuration = RoleColorConfiguration(
        color_primary = Color(222),
        color_secondary = Color(233),
        color_tertiary = Color(244),
    )
    
    yield color_configuration, color_configuration.to_data(defaults = True)


@vampytest._(vampytest.call_from(_iter_options__color_configuration__value_serializer()).returning_last())
def test__COLOR_CONFIGURATION_CONVERSION__value_serializer(input_value):
    """
    Tests whether `COLOR_CONFIGURATION_CONVERSION.value_serializer` works as intended.
    
    Parameters
    ----------
    input_value : ``RoleColorConfiguration``
        Processed value.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    output = COLOR_CONFIGURATION_CONVERSION.value_serializer(input_value)
    vampytest.assert_instance(output, dict)
    return output

# ---- flags ----

def test__FLAGS_CONVERSION__generic():
    """
    Tests whether ``FLAGS_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(FLAGS_CONVERSION)
    vampytest.assert_is(FLAGS_CONVERSION.value_validator, validate_flags)


def _iter_options__flags__value_deserializer():
    yield 60, RoleFlag(60)
    yield 0, RoleFlag()
    yield None, RoleFlag()


@vampytest._(vampytest.call_from(_iter_options__flags__value_deserializer()).returning_last())
def test__FLAGS_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `FLAGS_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``RoleFlag``
    """
    output = FLAGS_CONVERSION.value_deserializer(input_value)
    vampytest.assert_instance(output, RoleFlag)
    return output


def _iter_options__flags__value_serializer():
    yield RoleFlag(60), 60
    yield RoleFlag(), 0


@vampytest._(vampytest.call_from(_iter_options__flags__value_serializer()).returning_last())
def test__FLAGS_CONVERSION__value_serializer(input_value):
    """
    Tests whether `FLAGS_CONVERSION.value_serializer` works as intended.
    
    Parameters
    ----------
    input_value : ``RoleFlag``
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    output = FLAGS_CONVERSION.value_serializer(input_value)
    vampytest.assert_instance(output, int, accept_subtypes = False)
    return output


# ---- icon ----

def test__ICON_CONVERSION__generic():
    """
    Tests whether ``ICON_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(ICON_CONVERSION)
    vampytest.assert_eq(ICON_CONVERSION.value_deserializer, Icon.from_base_16_hash)
    vampytest.assert_eq(ICON_CONVERSION.value_serializer, Icon.as_base_16_hash.fget)
    vampytest.assert_eq(ICON_CONVERSION.value_validator, ROLE_ICON.validate_icon)


# ---- mentionable ---

def test__MENTIONABLE_CONVERSION__generic():
    """
    Tests whether ``MENTIONABLE_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(MENTIONABLE_CONVERSION)
    vampytest.assert_is(MENTIONABLE_CONVERSION.value_serializer, None)
    vampytest.assert_is(MENTIONABLE_CONVERSION.value_validator, validate_mentionable)


def _iter_options__mentionable__value_deserializer():
    yield True, True
    yield False, False
    yield None, False


@vampytest._(vampytest.call_from(_iter_options__mentionable__value_deserializer()).returning_last())
def test__MENTIONABLE_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `MENTIONABLE_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `bool`
    """
    return MENTIONABLE_CONVERSION.value_deserializer(input_value)


# ---- name ----

def test__NAME_CONVERSION__generic():
    """
    Tests whether ``NAME_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(NAME_CONVERSION)
    vampytest.assert_is(NAME_CONVERSION.value_deserializer, value_deserializer_name)
    vampytest.assert_is(NAME_CONVERSION.value_serializer, value_serializer_name)
    vampytest.assert_is(NAME_CONVERSION.value_validator, validate_name)


# ---- permissions ----

def test__PERMISSIONS_CONVERSION__generic():
    """
    Tests whether ``PERMISSIONS_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(PERMISSIONS_CONVERSION)
    vampytest.assert_is(PERMISSIONS_CONVERSION.value_validator, validate_permissions)

def _iter_options__permissions__value_deserializer():
    yield '60', Permission(60)
    yield '0', Permission()
    yield None, Permission()


@vampytest._(vampytest.call_from(_iter_options__permissions__value_deserializer()).returning_last())
def test__permission_conversions__value_deserializer(input_value):
    """
    Tests whether `PERMISSIONS_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``Permission``
    """
    output = PERMISSIONS_CONVERSION.value_deserializer(input_value)
    vampytest.assert_instance(output, Permission)
    return output


def _iter_options__permissions__value_serializer():
    yield Permission(60), '60'
    yield Permission(), '0'


@vampytest._(vampytest.call_from(_iter_options__permissions__value_serializer()).returning_last())
def test__PERMISSIONS_CONVERSION__value_serializer(input_value):
    """
    Tests whether `PERMISSIONS_CONVERSION.value_serializer` works as intended.
    
    Parameters
    ----------
    input_value : ``Permission``
        Processed value.
    
    Returns
    -------
    output : `str`
    """
    output = PERMISSIONS_CONVERSION.value_serializer(input_value)
    vampytest.assert_instance(output, str)
    return output


# ---- position ----

def test__POSITION_CONVERSION__generic():
    """
    Tests whether ``POSITION_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(POSITION_CONVERSION)
    vampytest.assert_is(POSITION_CONVERSION.value_serializer, None)
    vampytest.assert_is(POSITION_CONVERSION.value_validator, validate_position)


def _iter_options__position__value_deserializer():
    yield 60, 60
    yield 0, 0
    yield None, 0


@vampytest._(vampytest.call_from(_iter_options__position__value_deserializer()).returning_last())
def test__POSITION_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `POSITION_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `int`
    """
    return POSITION_CONVERSION.value_deserializer(input_value)


# ---- separated ---

def test__SEPARATED_CONVERSION__generic():
    """
    Tests whether ``SEPARATED_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(SEPARATED_CONVERSION)
    vampytest.assert_is(SEPARATED_CONVERSION.value_serializer, None)
    vampytest.assert_is(SEPARATED_CONVERSION.value_validator, validate_separated)


def _iter_options__separated__value_deserializer():
    yield True, True
    yield False, False
    yield None, False


@vampytest._(vampytest.call_from(_iter_options__separated__value_deserializer()).returning_last())
def test__SEPARATED_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `SEPARATED_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `bool`
    """
    return SEPARATED_CONVERSION.value_deserializer(input_value)


# ---- unicode_emoji ---

def test__UNICODE_EMOJI_CONVERSION__generic():
    """
    Tests whether ``UNICODE_EMOJI_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(UNICODE_EMOJI_CONVERSION)
    vampytest.assert_is(UNICODE_EMOJI_CONVERSION.value_validator, validate_unicode_emoji)


def _iter_options__unicode_emoji__value_deserializer():
    emoji = BUILTIN_EMOJIS['x']
    yield None, None
    yield emoji.unicode, emoji


@vampytest._(vampytest.call_from(_iter_options__unicode_emoji__value_deserializer()).returning_last())
def test__UNICODE_EMOJI_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `UNICODE_EMOJI_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``None | Emoji``
    """
    return UNICODE_EMOJI_CONVERSION.value_deserializer(input_value)


def _iter_options__unicode_emoji__value_serializer():
    emoji = BUILTIN_EMOJIS['x']
    yield None, None
    yield emoji, emoji.unicode


@vampytest._(vampytest.call_from(_iter_options__unicode_emoji__value_serializer()).returning_last())
def test__UNICODE_EMOJI_CONVERSION__value_serializer(input_value):
    """
    Tests whether `UNICODE_EMOJI_CONVERSION.value_serializer` works as intended.
    
    Parameters
    ----------
    input_value : ``None | Emoji``
        Processed value.
    
    Returns
    -------
    output : `None | str`
    """
    return UNICODE_EMOJI_CONVERSION.value_serializer(input_value)
