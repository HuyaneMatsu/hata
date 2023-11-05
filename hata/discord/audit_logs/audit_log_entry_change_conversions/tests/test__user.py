from datetime import datetime as DateTime

import vampytest

from ....bases import Icon
from ....user import GuildProfileFlag
from ....user.guild_profile.fields import validate_flags, validate_nick, validate_pending, validate_timed_out_until, \
    validate_bypasses_verification
from ....user.guild_profile.guild_profile import GUILD_PROFILE_AVATAR
from ....user.voice_state.fields import validate_deaf, validate_mute
from ....utils import datetime_to_timestamp

from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversion import (
    _assert_fields_set as _assert_conversion_fields_set
)
from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversionGroup import (
    _assert_fields_set as _assert_conversion_group_fields_set
)
from ...audit_log_role import AuditLogRole
from ...conversion_helpers.converters import get_converter_description, put_converter_description

from ..user import (
    AVATAR_CONVERSION, DEAF_CONVERSION, FLAGS_CONVERSION, MUTE_CONVERSION, NICK_CONVERSION, PENDING_CONVERSION,
    ROLES_CONVERSION__ADDITION, ROLES_CONVERSION__REMOVAL, TIMED_OUT_UNTIL_CONVERSION, USER_CONVERSIONS,
    BYPASSES_VERIFICATION_CONVERSION
)


def test__USER_CONVERSIONS():
    """
    Tests whether `USER_CONVERSIONS` contains conversion for every expected key.
    """
    _assert_conversion_group_fields_set(USER_CONVERSIONS)
    vampytest.assert_eq(
        {*USER_CONVERSIONS.get_converters.keys()},
        {
            '$add', '$remove', 'avatar_hash', 'communication_disabled_until', 'deaf', 'mute', 'nick', 'pending',
            'flags', 'bypasses_verification'
        },
    )


# ---- avatar ----

def test__AVATAR_CONVERSION__generic():
    """
    Tests whether ``AVATAR_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(AVATAR_CONVERSION)
    vampytest.assert_eq(AVATAR_CONVERSION.get_converter, Icon.from_base_16_hash)
    vampytest.assert_eq(AVATAR_CONVERSION.put_converter, Icon.as_base_16_hash.fget)
    vampytest.assert_eq(AVATAR_CONVERSION.validator, GUILD_PROFILE_AVATAR.validate_icon)


# ---- bypasses_verification ----

def test__BYPASSES_VERIFICATION_CONVERSION__generic():
    """
    Tests whether ``BYPASSES_VERIFICATION_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(BYPASSES_VERIFICATION_CONVERSION)
    # vampytest.assert_is(BYPASSES_VERIFICATION_CONVERSION.get_converter, )
    # vampytest.assert_is(BYPASSES_VERIFICATION_CONVERSION.put_converter, )
    vampytest.assert_is(BYPASSES_VERIFICATION_CONVERSION.validator, validate_bypasses_verification)


def _iter_options__bypasses_verification__get_converter():
    yield True, True
    yield False, False
    yield None, False


@vampytest._(vampytest.call_from(_iter_options__bypasses_verification__get_converter()).returning_last())
def test__BYPASSES_VERIFICATION_CONVERSION__get_converter(input_value):
    """
    Tests whether `BYPASSES_VERIFICATION_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `bool`
    """
    return BYPASSES_VERIFICATION_CONVERSION.get_converter(input_value)


def _iter_options__bypasses_verification__put_converter():
    yield True, True
    yield False, False


@vampytest._(vampytest.call_from(_iter_options__bypasses_verification__put_converter()).returning_last())
def test__BYPASSES_VERIFICATION_CONVERSION__put_converter(input_value):
    """
    Tests whether `BYPASSES_VERIFICATION_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `bool`
        Processed value.
    
    Returns
    -------
    output : `bool`
    """
    return BYPASSES_VERIFICATION_CONVERSION.put_converter(input_value)


# ---- deaf ----

def test__DEAF_CONVERSION__generic():
    """
    Tests whether ``DEAF_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(DEAF_CONVERSION)
    # vampytest.assert_is(DEAF_CONVERSION.get_converter, )
    # vampytest.assert_is(DEAF_CONVERSION.put_converter, )
    vampytest.assert_is(DEAF_CONVERSION.validator, validate_deaf)


def _iter_options__deaf__get_converter():
    yield True, True
    yield False, False
    yield None, False


@vampytest._(vampytest.call_from(_iter_options__deaf__get_converter()).returning_last())
def test__DEAF_CONVERSION__get_converter(input_value):
    """
    Tests whether `DEAF_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `bool`
    """
    return DEAF_CONVERSION.get_converter(input_value)


def _iter_options__deaf__put_converter():
    yield True, True
    yield False, False


@vampytest._(vampytest.call_from(_iter_options__deaf__put_converter()).returning_last())
def test__DEAF_CONVERSION__put_converter(input_value):
    """
    Tests whether `DEAF_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `bool`
        Processed value.
    
    Returns
    -------
    output : `bool`
    """
    return DEAF_CONVERSION.put_converter(input_value)


# ---- pending ----

def test__PENDING_CONVERSION__generic():
    """
    Tests whether ``PENDING_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(PENDING_CONVERSION)
    # vampytest.assert_is(PENDING_CONVERSION.get_converter, )
    # vampytest.assert_is(PENDING_CONVERSION.put_converter, )
    vampytest.assert_is(PENDING_CONVERSION.validator, validate_pending)


def _iter_options__pending__get_converter():
    yield True, True
    yield False, False
    yield None, False


@vampytest._(vampytest.call_from(_iter_options__pending__get_converter()).returning_last())
def test__PENDING_CONVERSION__get_converter(input_value):
    """
    Tests whether `PENDING_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `bool`
    """
    return PENDING_CONVERSION.get_converter(input_value)


def _iter_options__pending__put_converter():
    yield True, True
    yield False, False


@vampytest._(vampytest.call_from(_iter_options__pending__put_converter()).returning_last())
def test__PENDING_CONVERSION__put_converter(input_value):
    """
    Tests whether `PENDING_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `bool`
        Processed value.
    
    Returns
    -------
    output : `bool`
    """
    return PENDING_CONVERSION.put_converter(input_value)


# ---- mute ----

def test__MUTE_CONVERSION__generic():
    """
    Tests whether ``MUTE_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(MUTE_CONVERSION)
    # vampytest.assert_is(MUTE_CONVERSION.get_converter, )
    # vampytest.assert_is(MUTE_CONVERSION.put_converter, )
    vampytest.assert_is(MUTE_CONVERSION.validator, validate_mute)


def _iter_options__mute__get_converter():
    yield True, True
    yield False, False
    yield None, False


@vampytest._(vampytest.call_from(_iter_options__mute__get_converter()).returning_last())
def test__MUTE_CONVERSION__get_converter(input_value):
    """
    Tests whether `MUTE_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `bool`
    """
    return MUTE_CONVERSION.get_converter(input_value)


def _iter_options__mute__put_converter():
    yield True, True
    yield False, False


@vampytest._(vampytest.call_from(_iter_options__mute__put_converter()).returning_last())
def test__MUTE_CONVERSION__put_converter(input_value):
    """
    Tests whether `MUTE_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `bool`
        Processed value.
    
    Returns
    -------
    output : `bool`
    """
    return MUTE_CONVERSION.put_converter(input_value)


# ---- nick ----

def test__NICK_CONVERSION__generic():
    """
    Tests whether ``NICK_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(NICK_CONVERSION)
    vampytest.assert_is(NICK_CONVERSION.get_converter, get_converter_description)
    vampytest.assert_is(NICK_CONVERSION.put_converter, put_converter_description)
    vampytest.assert_is(NICK_CONVERSION.validator, validate_nick)


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
    yield 60, GuildProfileFlag(60)
    yield 0, GuildProfileFlag()
    yield None, GuildProfileFlag()


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
    output : ``GuildProfileFlag``
    """
    output = FLAGS_CONVERSION.get_converter(input_value)
    vampytest.assert_instance(output, GuildProfileFlag)
    return output


def _iter_options__flags__put_converter():
    yield GuildProfileFlag(60), 60
    yield GuildProfileFlag(), 0


@vampytest._(vampytest.call_from(_iter_options__flags__put_converter()).returning_last())
def test__FLAGS_CONVERSION__put_converter(input_value):
    """
    Tests whether `FLAGS_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : ``GuildProfileFlag``
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    output = FLAGS_CONVERSION.put_converter(input_value)
    vampytest.assert_instance(output, int, accept_subtypes = False)
    return output


# ---- roles ----

def test__ROLES_CONVERSION_ADDITION__generic():
    """
    Tests whether ``ROLES_CONVERSION__ADDITION`` works as intended.
    """
    _assert_conversion_fields_set(ROLES_CONVERSION__ADDITION)
    # vampytest.assert_is(ROLES_CONVERSION__ADDITION.get_converter, )
    # vampytest.assert_is(ROLES_CONVERSION__ADDITION.put_converter, )
    # vampytest.assert_is(ROLES_CONVERSION__ADDITION.validator, validate_flags)


def test__ROLES_CONVERSION_REMOVAL__generic():
    """
    Tests whether ``ROLES_CONVERSION__REMOVAL`` works as intended.
    """
    _assert_conversion_fields_set(ROLES_CONVERSION__REMOVAL)
    # vampytest.assert_is(ROLES_CONVERSION__REMOVAL.get_converter, )
    # vampytest.assert_is(ROLES_CONVERSION__REMOVAL.put_converter, )
    # vampytest.assert_is(ROLES_CONVERSION__REMOVAL.validator, validate_flags)


def _iter_options__roles__get_converter():
    audit_log_role_0 = AuditLogRole(role_id = 202310280000)
    audit_log_role_1 = AuditLogRole(role_id = 202310280001)
    
    yield ROLES_CONVERSION__ADDITION, None, None
    yield ROLES_CONVERSION__ADDITION, [], None
    yield (
        ROLES_CONVERSION__ADDITION,
        [audit_log_role_0.to_data(defaults = True), audit_log_role_1.to_data(defaults = True)],
        (audit_log_role_0, audit_log_role_1),
    )

    yield ROLES_CONVERSION__REMOVAL, None, None
    yield ROLES_CONVERSION__REMOVAL, [], None
    yield (
        ROLES_CONVERSION__REMOVAL,
        [audit_log_role_0.to_data(defaults = True), audit_log_role_1.to_data(defaults = True)],
        (audit_log_role_0, audit_log_role_1),
    )


@vampytest._(vampytest.call_from(_iter_options__roles__get_converter()).returning_last())
def test__ROLES_CONVERSION__get_converter(conversion, value):
    """
    Parameters
    ----------
    conversion : ``AuditLogEntryChangeConversion``
        Conversion to check.
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `None | tuple<AuditLogRole>`
    """
    return conversion.get_converter(value)


def _iter_options__roles__set_converter():
    audit_log_role_0 = AuditLogRole(role_id = 202310280002)
    audit_log_role_1 = AuditLogRole(role_id = 202310280003)
    
    yield ROLES_CONVERSION__ADDITION, None, []
    yield (
        ROLES_CONVERSION__ADDITION,
        (audit_log_role_0, audit_log_role_1),
        [audit_log_role_0.to_data(defaults = True), audit_log_role_1.to_data(defaults = True)],
    )

    yield ROLES_CONVERSION__REMOVAL, None, []
    yield (
        ROLES_CONVERSION__REMOVAL,
        (audit_log_role_0, audit_log_role_1),
        [audit_log_role_0.to_data(defaults = True), audit_log_role_1.to_data(defaults = True)],
    )


@vampytest._(vampytest.call_from(_iter_options__roles__set_converter()).returning_last())
def test__ROLES_CONVERSION__set_converter(conversion, value):
    """
    Parameters
    ----------
    conversion : ``AuditLogEntryChangeConversion``
        Conversion to check.
    input_value : `None | tuple<AuditLogRole>`
        Processed value.
    
    Returns
    -------
    output : `list<dict<str, object>>`
    """
    return conversion.put_converter(value)


def _iter_options__roles__validator__passing():
    audit_log_role_0 = AuditLogRole(role_id = 202310280004)
    audit_log_role_1 = AuditLogRole(role_id = 202310280005)
    
    yield ROLES_CONVERSION__ADDITION, None, None
    yield ROLES_CONVERSION__ADDITION, [], None
    yield ROLES_CONVERSION__ADDITION, [audit_log_role_0, audit_log_role_1], (audit_log_role_0, audit_log_role_1)

    yield ROLES_CONVERSION__REMOVAL, None, None
    yield ROLES_CONVERSION__REMOVAL, [], None
    yield ROLES_CONVERSION__REMOVAL, [audit_log_role_0, audit_log_role_1], (audit_log_role_0, audit_log_role_1)


def _iter_options__roles__validator__type_error():
    yield ROLES_CONVERSION__ADDITION, 12.5
    yield ROLES_CONVERSION__ADDITION, [12.5]


@vampytest._(vampytest.call_from(_iter_options__roles__validator__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__roles__validator__type_error()).raising(TypeError))
def test__ROLES_CONVERSION__validator(conversion, value):
    """
    Parameters
    ----------
    conversion : ``AuditLogEntryChangeConversion``
        Conversion to check.
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | tuple<AuditLogRole>`
    
    Raising
    -------
    TypeError
    """
    return conversion.validator(value)


# ---- timed_out_until ----

def test__TIMED_OUT_UNTIL_CONVERSION__generic():
    """
    Tests whether ``TIMED_OUT_UNTIL_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(TIMED_OUT_UNTIL_CONVERSION)
    # vampytest.assert_is(TIMED_OUT_UNTIL_CONVERSION.get_converter, )
    # vampytest.assert_is(TIMED_OUT_UNTIL_CONVERSION.put_converter, )
    vampytest.assert_is(TIMED_OUT_UNTIL_CONVERSION.validator, validate_timed_out_until)


def _iter_options__timed_out_until__get_converter():
    date_time = DateTime(2016, 5, 14)
    
    yield datetime_to_timestamp(date_time), date_time
    yield None, None


@vampytest._(vampytest.call_from(_iter_options__timed_out_until__get_converter()).returning_last())
def test__TIMED_OUT_UNTIL_CONVERSION__get_converter(input_value):
    """
    Tests whether `TIMED_OUT_UNTIL_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `None | DateTime`
    """
    return TIMED_OUT_UNTIL_CONVERSION.get_converter(input_value)


def _iter_options__timed_out_until__put_converter():
    date_time = DateTime(2016, 5, 14)
    
    yield date_time, datetime_to_timestamp(date_time)
    yield None, None


@vampytest._(vampytest.call_from(_iter_options__timed_out_until__put_converter()).returning_last())
def test__TIMED_OUT_UNTIL_CONVERSION__put_converter(input_value):
    """
    Tests whether `TIMED_OUT_UNTIL_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `None | DateTime`
        Processed value.
    
    Returns
    -------
    output : `None | str`
    """
    return TIMED_OUT_UNTIL_CONVERSION.put_converter(input_value)
