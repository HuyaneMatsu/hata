import vampytest

from ....sticker import StickerFormat, StickerType
from ....sticker.sticker.constants import SORT_VALUE_MIN
from ....sticker.sticker.fields import (
    validate_available, validate_description, validate_format, validate_guild_id, validate_id, validate_name,
    validate_sort_value, validate_tags, validate_type
)

from ...audit_log_entry_change_conversion.change_deserializers import change_deserializer_deprecation
from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversion import (
    _assert_fields_set as _assert_conversion_fields_set
)
from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversionGroup import (
    _assert_fields_set as _assert_conversion_group_fields_set
)
from ...conversion_helpers.converters import (
    value_deserializer_description, value_deserializer_id, value_deserializer_name, value_serializer_description,
    value_serializer_id, value_serializer_name
)

from ..sticker import (
    ASSET_CONVERSION_IGNORED, AVAILABLE_CONVERSION, DESCRIPTION_CONVERSION, FORMAT_CONVERSION, GUILD_ID_CONVERSION,
    ID_CONVERSION, NAME_CONVERSION, SORT_VALUE_CONVERSION, STICKER_CONVERSIONS, TAGS_CONVERSION, TYPE_CONVERSION
)


def test__STICKER_CONVERSIONS():
    """
    Tests whether `STICKER_CONVERSIONS` contains conversion for every expected key.
    """
    _assert_conversion_group_fields_set(STICKER_CONVERSIONS)
    vampytest.assert_eq(
        {*STICKER_CONVERSIONS.iter_field_keys()},
        {'available', 'description', 'name', 'sort_value', 'tags', 'id', 'format_type', 'guild_id', 'asset', 'type'},
    )

# ---- available ----

def test__AVAILABLE_CONVERSION__generic():
    """
    Tests whether ``AVAILABLE_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(AVAILABLE_CONVERSION)
    vampytest.assert_is(AVAILABLE_CONVERSION.value_serializer, None)
    vampytest.assert_is(AVAILABLE_CONVERSION.value_validator, validate_available)


def _iter_options__available__value_deserializer():
    yield True, True
    yield False, False
    yield None, True


@vampytest._(vampytest.call_from(_iter_options__available__value_deserializer()).returning_last())
def test__AVAILABLE_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `AVAILABLE_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `bool`
    """
    return AVAILABLE_CONVERSION.value_deserializer(input_value)


# ---- description ----

def test__DESCRIPTION_CONVERSION__generic():
    """
    Tests whether ``DESCRIPTION_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(DESCRIPTION_CONVERSION)
    vampytest.assert_is(DESCRIPTION_CONVERSION.value_deserializer, value_deserializer_description)
    vampytest.assert_is(DESCRIPTION_CONVERSION.value_serializer, value_serializer_description)
    vampytest.assert_is(DESCRIPTION_CONVERSION.value_validator, validate_description)


# ---- format ----

def test__FORMAT_CONVERSION__generic():
    """
    Tests whether ``FORMAT_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(FORMAT_CONVERSION)
    vampytest.assert_is(FORMAT_CONVERSION.value_validator, validate_format)


def _iter_options__format__value_deserializer():
    yield None, StickerFormat.none
    yield StickerFormat.png.value, StickerFormat.png


@vampytest._(vampytest.call_from(_iter_options__format__value_deserializer()).returning_last())
def test__FORMAT_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `FORMAT_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``StickerFormat``
    """
    return FORMAT_CONVERSION.value_deserializer(input_value)


def _iter_options__format__value_serializer():
    yield StickerFormat.none, StickerFormat.none.value
    yield StickerFormat.png, StickerFormat.png.value


@vampytest._(vampytest.call_from(_iter_options__format__value_serializer()).returning_last())
def test__FORMAT_CONVERSION__value_serializer(input_value):
    """
    Tests whether `FORMAT_CONVERSION.value_serializer` works as intended.
    
    Parameters
    ----------
    input_value : ``StickerFormat``
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return FORMAT_CONVERSION.value_serializer(input_value)


# ---- guild_id ----

def test__GUILD_ID_CONVERSION__generic():
    """
    Tests whether ``GUILD_ID_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(GUILD_ID_CONVERSION)
    vampytest.assert_is(GUILD_ID_CONVERSION.value_deserializer, value_deserializer_id)
    vampytest.assert_is(GUILD_ID_CONVERSION.value_serializer, value_serializer_id)
    vampytest.assert_is(GUILD_ID_CONVERSION.value_validator, validate_guild_id)


# ---- id ----

def test__ID_CONVERSION__generic():
    """
    Tests whether ``ID_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(ID_CONVERSION)
    vampytest.assert_is(ID_CONVERSION.value_deserializer, value_deserializer_id)
    vampytest.assert_is(ID_CONVERSION.value_serializer, value_serializer_id)
    vampytest.assert_is(ID_CONVERSION.value_validator, validate_id)


# ---- name ----

def test__NAME_CONVERSION__generic():
    """
    Tests whether ``NAME_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(NAME_CONVERSION)
    vampytest.assert_is(NAME_CONVERSION.value_deserializer, value_deserializer_name)
    vampytest.assert_is(NAME_CONVERSION.value_serializer, value_serializer_name)
    vampytest.assert_is(NAME_CONVERSION.value_validator, validate_name)


# ---- sort_value ----

def test__SORT_VALUE_CONVERSION__generic():
    """
    Tests whether ``SORT_VALUE_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(SORT_VALUE_CONVERSION)
    vampytest.assert_is(SORT_VALUE_CONVERSION.value_serializer, None)
    vampytest.assert_is(SORT_VALUE_CONVERSION.value_validator, validate_sort_value)


def _iter_options__sort_value__value_deserializer():
    yield 60, 60
    yield 0, 0
    yield None, SORT_VALUE_MIN


@vampytest._(vampytest.call_from(_iter_options__sort_value__value_deserializer()).returning_last())
def test__SORT_VALUE_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `SORT_VALUE_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `int`
    """
    return SORT_VALUE_CONVERSION.value_deserializer(input_value)

# ---- tags ----

def test__TAGS_CONVERSION__generic():
    """
    Tests whether ``TAGS_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(TAGS_CONVERSION)
    vampytest.assert_is(TAGS_CONVERSION.value_validator, validate_tags)


def _iter_options__tags__value_deserializer():
    yield None, None
    yield '', None
    yield 'koishi, satori', frozenset(('koishi', 'satori'))


@vampytest._(vampytest.call_from(_iter_options__tags__value_deserializer()).returning_last())
def test__TAGS_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `TAGS_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `None | frozenset<str>`
    """
    return TAGS_CONVERSION.value_deserializer(input_value)


def _iter_options__tags__value_serializer():
    yield None, ''
    yield frozenset(('koishi', 'satori')), 'koishi, satori'


@vampytest._(vampytest.call_from(_iter_options__tags__value_serializer()).returning_last())
def test__TAGS_CONVERSION__value_serializer(input_value):
    """
    Tests whether `TAGS_CONVERSION.value_serializer` works as intended.
    
    Parameters
    ----------
    input_value : `None | frozenset<str>`
        Processed value.
    
    Returns
    -------
    output : `str`
    """
    return TAGS_CONVERSION.value_serializer(input_value)


# ---- type ----

def test__TYPE_CONVERSION__generic():
    """
    Tests whether ``TYPE_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(TYPE_CONVERSION)
    vampytest.assert_is(TYPE_CONVERSION.value_validator, validate_type)


def _iter_options__type__value_deserializer():
    yield None, StickerType.none
    yield StickerType.standard.value, StickerType.standard


@vampytest._(vampytest.call_from(_iter_options__type__value_deserializer()).returning_last())
def test__TYPE_CONVERSION__value_deserializer(input_value):
    """
    Tests whether `TYPE_CONVERSION.value_deserializer` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``StickerType``
    """
    return TYPE_CONVERSION.value_deserializer(input_value)


def _iter_options__type__value_serializer():
    yield StickerType.none, StickerType.none.value
    yield StickerType.standard, StickerType.standard.value


@vampytest._(vampytest.call_from(_iter_options__type__value_serializer()).returning_last())
def test__TYPE_CONVERSION__value_serializer(input_value):
    """
    Tests whether `TYPE_CONVERSION.value_serializer` works as intended.
    
    Parameters
    ----------
    input_value : ``StickerType``
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return TYPE_CONVERSION.value_serializer(input_value)


# ---- ignored ----

def _iter_options__ignored():
    yield ASSET_CONVERSION_IGNORED


@vampytest.call_from(_iter_options__ignored())
def test_ignored(conversion):
    """
    Tests whether the ignored conversions are set up as intended.
    
    Parameters
    ----------
    conversion : ``AuditLogEntryChangeConversion``
        The conversion to test.
    """
    _assert_conversion_fields_set(conversion)
    vampytest.assert_is(conversion.change_deserializer, change_deserializer_deprecation)
    vampytest.assert_eq(conversion.field_name, '')
