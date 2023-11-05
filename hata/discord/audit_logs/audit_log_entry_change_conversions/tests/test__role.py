import vampytest

from ....bases import Icon
from ....color import Color
from ....core import BUILTIN_EMOJIS
from ....permission import Permission
from ....permission.constants import PERMISSION_KEY
from ....role import RoleFlag
from ....role.role.fields import (
    validate_color, validate_flags, validate_mentionable, validate_name, validate_permissions, validate_position,
    validate_separated, validate_unicode_emoji
)
from ....role.role.role import ROLE_ICON

from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversion import (
    _assert_fields_set as _assert_conversion_fields_set
)
from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversionGroup import (
    _assert_fields_set as _assert_conversion_group_fields_set
)
from ...conversion_helpers.converters import get_converter_name, put_converter_name

from ..role import (
    COLOR_CONVERSION, FLAGS_CONVERSION, ICON_CONVERSION, MENTIONABLE_CONVERSION, NAME_CONVERSION,
    PERMISSIONS_CONVERSION, POSITION_CONVERSION, ROLE_CONVERSIONS, SEPARATED_CONVERSION, UNICODE_EMOJI_CONVERSION
)


def test__ROLE_CONVERSIONS():
    """
    Tests whether `ROLE_CONVERSIONS` contains conversion for every expected key.
    """
    _assert_conversion_group_fields_set(ROLE_CONVERSIONS)
    vampytest.assert_eq(
        {*ROLE_CONVERSIONS.get_converters.keys()},
        {'color', 'flags', 'icon_hash', 'mentionable', 'name', PERMISSION_KEY, 'position', 'hoist', 'unicode_emoji'},
    )


# ---- color ----

def test__COLOR_CONVERSION__generic():
    """
    Tests whether ``COLOR_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(COLOR_CONVERSION)
    # vampytest.assert_is(COLOR_CONVERSION.get_converter, )
    # vampytest.assert_is(COLOR_CONVERSION.put_converter, )
    vampytest.assert_is(COLOR_CONVERSION.validator, validate_color)


def _iter_options__color__get_converter():
    yield 60, Color(60)
    yield 0, Color()
    yield None, Color()


@vampytest._(vampytest.call_from(_iter_options__color__get_converter()).returning_last())
def test__COLOR_CONVERSION__get_converter(input_value):
    """
    Tests whether `COLOR_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``Color``
    """
    output = COLOR_CONVERSION.get_converter(input_value)
    vampytest.assert_instance(output, Color)
    return output


def _iter_options__color__put_converter():
    yield Color(60), 60
    yield Color(), 0


@vampytest._(vampytest.call_from(_iter_options__color__put_converter()).returning_last())
def test__COLOR_CONVERSION__put_converter(input_value):
    """
    Tests whether `COLOR_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : ``Color``
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    output = COLOR_CONVERSION.put_converter(input_value)
    vampytest.assert_instance(output, int, accept_subtypes = False)
    return output


# ---- flags ----

def test__FLAGS_CONVERSION__generic():
    """
    Tests whether ``FLAGS_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(FLAGS_CONVERSION)
    # vampytest.assert_is(FLAGS_CONVERSION.get_converter, )
    # vampytest.assert_is(FLAGS_CONVERSION.put_converter, )
    vampytest.assert_is(FLAGS_CONVERSION.validator, validate_flags)


def _iter_options__flags__get_converter():
    yield 60, RoleFlag(60)
    yield 0, RoleFlag()
    yield None, RoleFlag()


@vampytest._(vampytest.call_from(_iter_options__flags__get_converter()).returning_last())
def test__FLAGS_CONVERSION__get_converter(input_value):
    """
    Tests whether `FLAGS_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``RoleFlag``
    """
    output = FLAGS_CONVERSION.get_converter(input_value)
    vampytest.assert_instance(output, RoleFlag)
    return output


def _iter_options__flags__put_converter():
    yield RoleFlag(60), 60
    yield RoleFlag(), 0


@vampytest._(vampytest.call_from(_iter_options__flags__put_converter()).returning_last())
def test__FLAGS_CONVERSION__put_converter(input_value):
    """
    Tests whether `FLAGS_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : ``RoleFlag``
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    output = FLAGS_CONVERSION.put_converter(input_value)
    vampytest.assert_instance(output, int, accept_subtypes = False)
    return output


# ---- icon ----

def test__ICON_CONVERSION__generic():
    """
    Tests whether ``ICON_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(ICON_CONVERSION)
    vampytest.assert_eq(ICON_CONVERSION.get_converter, Icon.from_base_16_hash)
    vampytest.assert_eq(ICON_CONVERSION.put_converter, Icon.as_base_16_hash.fget)
    vampytest.assert_eq(ICON_CONVERSION.validator, ROLE_ICON.validate_icon)


# ---- mentionable ---

def test__MENTIONABLE_CONVERSION__generic():
    """
    Tests whether ``MENTIONABLE_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(MENTIONABLE_CONVERSION)
    # vampytest.assert_is(MENTIONABLE_CONVERSION.get_converter, )
    # vampytest.assert_is(MENTIONABLE_CONVERSION.put_converter, )
    vampytest.assert_is(MENTIONABLE_CONVERSION.validator, validate_mentionable)


def _iter_options__mentionable__get_converter():
    yield True, True
    yield False, False
    yield None, False


@vampytest._(vampytest.call_from(_iter_options__mentionable__get_converter()).returning_last())
def test__MENTIONABLE_CONVERSION__get_converter(input_value):
    """
    Tests whether `MENTIONABLE_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `bool`
    """
    return MENTIONABLE_CONVERSION.get_converter(input_value)


def _iter_options__mentionable__put_converter():
    yield True, True
    yield False, False


@vampytest._(vampytest.call_from(_iter_options__mentionable__put_converter()).returning_last())
def test__MENTIONABLE_CONVERSION__put_converter(input_value):
    """
    Tests whether `MENTIONABLE_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `bool`
        Processed value.
    
    Returns
    -------
    output : `bool`
    """
    return MENTIONABLE_CONVERSION.put_converter(input_value)


# ---- name ----

def test__NAME_CONVERSION__generic():
    """
    Tests whether ``NAME_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(NAME_CONVERSION)
    vampytest.assert_is(NAME_CONVERSION.get_converter, get_converter_name)
    vampytest.assert_is(NAME_CONVERSION.put_converter, put_converter_name)
    vampytest.assert_is(NAME_CONVERSION.validator, validate_name)


# ---- permissions ----

def test__PERMISSIONS_CONVERSION__generic():
    """
    Tests whether ``PERMISSIONS_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(PERMISSIONS_CONVERSION)
    # vampytest.assert_is(PERMISSIONS_CONVERSION.get_converter, )
    # vampytest.assert_is(PERMISSIONS_CONVERSION.put_converter, )
    vampytest.assert_is(PERMISSIONS_CONVERSION.validator, validate_permissions)

def _iter_options__permissions__get_converter():
    yield '60', Permission(60)
    yield '0', Permission()
    yield None, Permission()


@vampytest._(vampytest.call_from(_iter_options__permissions__get_converter()).returning_last())
def test__permission_conversions__get_converter(input_value):
    """
    Tests whether `PERMISSIONS_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``Permission``
    """
    output = PERMISSIONS_CONVERSION.get_converter(input_value)
    vampytest.assert_instance(output, Permission)
    return output


def _iter_options__permissions__put_converter():
    yield Permission(60), '60'
    yield Permission(), '0'


@vampytest._(vampytest.call_from(_iter_options__permissions__put_converter()).returning_last())
def test__PERMISSIONS_CONVERSION__put_converter(input_value):
    """
    Tests whether `PERMISSIONS_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : ``Permission``
        Processed value.
    
    Returns
    -------
    output : `str`
    """
    output = PERMISSIONS_CONVERSION.put_converter(input_value)
    vampytest.assert_instance(output, str)
    return output


# ---- position ----

def test__POSITION_CONVERSION__generic():
    """
    Tests whether ``POSITION_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(POSITION_CONVERSION)
    # vampytest.assert_is(POSITION_CONVERSION.get_converter, )
    # vampytest.assert_is(POSITION_CONVERSION.put_converter, )
    vampytest.assert_is(POSITION_CONVERSION.validator, validate_position)


def _iter_options__position__get_converter():
    yield 60, 60
    yield 0, 0
    yield None, 0


@vampytest._(vampytest.call_from(_iter_options__position__get_converter()).returning_last())
def test__POSITION_CONVERSION__get_converter(input_value):
    """
    Tests whether `POSITION_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `int`
    """
    return POSITION_CONVERSION.get_converter(input_value)


def _iter_options__position__put_converter():
    yield 60, 60
    yield 0, 0


@vampytest._(vampytest.call_from(_iter_options__position__put_converter()).returning_last())
def test__POSITION_CONVERSION__put_converter(input_value):
    """
    Tests whether `POSITION_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return POSITION_CONVERSION.put_converter(input_value)


# ---- separated ---

def test__SEPARATED_CONVERSION__generic():
    """
    Tests whether ``SEPARATED_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(SEPARATED_CONVERSION)
    # vampytest.assert_is(SEPARATED_CONVERSION.get_converter, )
    # vampytest.assert_is(SEPARATED_CONVERSION.put_converter, )
    vampytest.assert_is(SEPARATED_CONVERSION.validator, validate_separated)


def _iter_options__separated__get_converter():
    yield True, True
    yield False, False
    yield None, False


@vampytest._(vampytest.call_from(_iter_options__separated__get_converter()).returning_last())
def test__SEPARATED_CONVERSION__get_converter(input_value):
    """
    Tests whether `SEPARATED_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `bool`
    """
    return SEPARATED_CONVERSION.get_converter(input_value)


def _iter_options__separated__put_converter():
    yield True, True
    yield False, False


@vampytest._(vampytest.call_from(_iter_options__separated__put_converter()).returning_last())
def test__SEPARATED_CONVERSION__put_converter(input_value):
    """
    Tests whether `SEPARATED_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `bool`
        Processed value.
    
    Returns
    -------
    output : `bool`
    """
    return SEPARATED_CONVERSION.put_converter(input_value)


# ---- unicode_emoji ---

def test__UNICODE_EMOJI_CONVERSION__generic():
    """
    Tests whether ``UNICODE_EMOJI_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(UNICODE_EMOJI_CONVERSION)
    # vampytest.assert_is(UNICODE_EMOJI_CONVERSION.get_converter, )
    # vampytest.assert_is(UNICODE_EMOJI_CONVERSION.put_converter, )
    vampytest.assert_is(UNICODE_EMOJI_CONVERSION.validator, validate_unicode_emoji)


def _iter_options__unicode_emoji__get_converter():
    emoji = BUILTIN_EMOJIS['x']
    yield None, None
    yield emoji.unicode, emoji


@vampytest._(vampytest.call_from(_iter_options__unicode_emoji__get_converter()).returning_last())
def test__UNICODE_EMOJI_CONVERSION__get_converter(input_value):
    """
    Tests whether `UNICODE_EMOJI_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `None | Emoji`
    """
    return UNICODE_EMOJI_CONVERSION.get_converter(input_value)


def _iter_options__unicode_emoji__put_converter():
    emoji = BUILTIN_EMOJIS['x']
    yield None, None
    yield emoji, emoji.unicode


@vampytest._(vampytest.call_from(_iter_options__unicode_emoji__put_converter()).returning_last())
def test__UNICODE_EMOJI_CONVERSION__put_converter(input_value):
    """
    Tests whether `UNICODE_EMOJI_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `None | Emoji`
        Processed value.
    
    Returns
    -------
    output : `None | str`
    """
    return UNICODE_EMOJI_CONVERSION.put_converter(input_value)
