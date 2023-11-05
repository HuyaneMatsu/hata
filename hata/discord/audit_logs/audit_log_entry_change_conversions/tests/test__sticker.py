import vampytest

from ....sticker import StickerFormat, StickerType
from ....sticker.sticker.constants import SORT_VALUE_MIN
from ....sticker.sticker.fields import (
    validate_available, validate_description, validate_format, validate_guild_id, validate_id, validate_name,
    validate_sort_value, validate_tags, validate_type
)

from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversion import (
    _assert_fields_set as _assert_conversion_fields_set
)
from ...audit_log_entry_change_conversion.tests.test__AuditLogEntryChangeConversionGroup import (
    _assert_fields_set as _assert_conversion_group_fields_set
)
from ...conversion_helpers.converters import (
    get_converter_description, get_converter_id, get_converter_name, put_converter_description, put_converter_id,
    put_converter_name
)

from ..sticker import (
    AVAILABLE_CONVERSION, DESCRIPTION_CONVERSION, FORMAT_CONVERSION, GUILD_ID_CONVERSION, ID_CONVERSION,
    NAME_CONVERSION, SORT_VALUE_CONVERSION, STICKER_CONVERSIONS, TAGS_CONVERSION, TYPE_CONVERSION
)


def test__STICKER_CONVERSIONS():
    """
    Tests whether `STICKER_CONVERSIONS` contains conversion for every expected key.
    """
    _assert_conversion_group_fields_set(STICKER_CONVERSIONS)
    vampytest.assert_eq(
        {*STICKER_CONVERSIONS.get_converters.keys()},
        {'available', 'description', 'name', 'sort_value', 'tags', 'id', 'format_type', 'guild_id', 'asset', 'type'},
    )

# ---- available ----

def test__AVAILABLE_CONVERSION__generic():
    """
    Tests whether ``AVAILABLE_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(AVAILABLE_CONVERSION)
    # vampytest.assert_is(AVAILABLE_CONVERSION.get_converter, )
    # vampytest.assert_is(AVAILABLE_CONVERSION.put_converter, )
    vampytest.assert_is(AVAILABLE_CONVERSION.validator, validate_available)


def _iter_options__available__get_converter():
    yield True, True
    yield False, False
    yield None, True


@vampytest._(vampytest.call_from(_iter_options__available__get_converter()).returning_last())
def test__AVAILABLE_CONVERSION__get_converter(input_value):
    """
    Tests whether `AVAILABLE_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `bool`
    """
    return AVAILABLE_CONVERSION.get_converter(input_value)


def _iter_options__available__put_converter():
    yield True, True
    yield False, False


@vampytest._(vampytest.call_from(_iter_options__available__put_converter()).returning_last())
def test__AVAILABLE_CONVERSION__put_converter(input_value):
    """
    Tests whether `AVAILABLE_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `bool`
        Processed value.
    
    Returns
    -------
    output : `bool`
    """
    return AVAILABLE_CONVERSION.put_converter(input_value)


# ---- description ----

def test__DESCRIPTION_CONVERSION__generic():
    """
    Tests whether ``DESCRIPTION_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(DESCRIPTION_CONVERSION)
    vampytest.assert_is(DESCRIPTION_CONVERSION.get_converter, get_converter_description)
    vampytest.assert_is(DESCRIPTION_CONVERSION.put_converter, put_converter_description)
    vampytest.assert_is(DESCRIPTION_CONVERSION.validator, validate_description)


# ---- format ----

def test__FORMAT_CONVERSION__generic():
    """
    Tests whether ``FORMAT_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(FORMAT_CONVERSION)
    # vampytest.assert_is(FORMAT_CONVERSION.get_converter, )
    # vampytest.assert_is(FORMAT_CONVERSION.put_converter, )
    vampytest.assert_is(FORMAT_CONVERSION.validator, validate_format)


def _iter_options__format__get_converter():
    yield None, StickerFormat.none
    yield StickerFormat.png.value, StickerFormat.png


@vampytest._(vampytest.call_from(_iter_options__format__get_converter()).returning_last())
def test__FORMAT_CONVERSION__get_converter(input_value):
    """
    Tests whether `FORMAT_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``StickerFormat``
    """
    return FORMAT_CONVERSION.get_converter(input_value)


def _iter_options__format__put_converter():
    yield StickerFormat.none, StickerFormat.none.value
    yield StickerFormat.png, StickerFormat.png.value


@vampytest._(vampytest.call_from(_iter_options__format__put_converter()).returning_last())
def test__FORMAT_CONVERSION__put_converter(input_value):
    """
    Tests whether `FORMAT_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : ``StickerFormat``
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return FORMAT_CONVERSION.put_converter(input_value)


# ---- guild_id ----

def test__GUILD_ID_CONVERSION__generic():
    """
    Tests whether ``GUILD_ID_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(GUILD_ID_CONVERSION)
    vampytest.assert_is(GUILD_ID_CONVERSION.get_converter, get_converter_id)
    vampytest.assert_is(GUILD_ID_CONVERSION.put_converter, put_converter_id)
    vampytest.assert_is(GUILD_ID_CONVERSION.validator, validate_guild_id)


# ---- id ----

def test__ID_CONVERSION__generic():
    """
    Tests whether ``ID_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(ID_CONVERSION)
    vampytest.assert_is(ID_CONVERSION.get_converter, get_converter_id)
    vampytest.assert_is(ID_CONVERSION.put_converter, put_converter_id)
    vampytest.assert_is(ID_CONVERSION.validator, validate_id)


# ---- name ----

def test__NAME_CONVERSION__generic():
    """
    Tests whether ``NAME_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(NAME_CONVERSION)
    vampytest.assert_is(NAME_CONVERSION.get_converter, get_converter_name)
    vampytest.assert_is(NAME_CONVERSION.put_converter, put_converter_name)
    vampytest.assert_is(NAME_CONVERSION.validator, validate_name)


# ---- sort_value ----

def test__SORT_VALUE_CONVERSION__generic():
    """
    Tests whether ``SORT_VALUE_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(SORT_VALUE_CONVERSION)
    # vampytest.assert_is(SORT_VALUE_CONVERSION.get_converter, )
    # vampytest.assert_is(SORT_VALUE_CONVERSION.put_converter, )
    vampytest.assert_is(SORT_VALUE_CONVERSION.validator, validate_sort_value)


def _iter_options__sort_value__get_converter():
    yield 60, 60
    yield 0, 0
    yield None, SORT_VALUE_MIN


@vampytest._(vampytest.call_from(_iter_options__sort_value__get_converter()).returning_last())
def test__SORT_VALUE_CONVERSION__get_converter(input_value):
    """
    Tests whether `SORT_VALUE_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `int`
    """
    return SORT_VALUE_CONVERSION.get_converter(input_value)


def _iter_options__sort_value__put_converter():
    yield 60, 60
    yield SORT_VALUE_MIN, SORT_VALUE_MIN


@vampytest._(vampytest.call_from(_iter_options__sort_value__put_converter()).returning_last())
def test__SORT_VALUE_CONVERSION__put_converter(input_value):
    """
    Tests whether `SORT_VALUE_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return SORT_VALUE_CONVERSION.put_converter(input_value)


# ---- tags ----

def test__TAGS_CONVERSION__generic():
    """
    Tests whether ``TAGS_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(TAGS_CONVERSION)
    # vampytest.assert_is(TAGS_CONVERSION.get_converter, )
    # vampytest.assert_is(TAGS_CONVERSION.put_converter, )
    vampytest.assert_is(TAGS_CONVERSION.validator, validate_tags)


def _iter_options__tags__get_converter():
    yield None, None
    yield '', None
    yield 'koishi, satori', frozenset(('koishi', 'satori'))


@vampytest._(vampytest.call_from(_iter_options__tags__get_converter()).returning_last())
def test__TAGS_CONVERSION__get_converter(input_value):
    """
    Tests whether `TAGS_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : `None | frozenset<str>`
    """
    return TAGS_CONVERSION.get_converter(input_value)


def _iter_options__tags__put_converter():
    yield None, ''
    yield frozenset(('koishi', 'satori')), 'koishi, satori'


@vampytest._(vampytest.call_from(_iter_options__tags__put_converter()).returning_last())
def test__TAGS_CONVERSION__put_converter(input_value):
    """
    Tests whether `TAGS_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : `None | frozenset<str>`
        Processed value.
    
    Returns
    -------
    output : `str`
    """
    return TAGS_CONVERSION.put_converter(input_value)


# ---- type ----

def test__TYPE_CONVERSION__generic():
    """
    Tests whether ``TYPE_CONVERSION`` works as intended.
    """
    _assert_conversion_fields_set(TYPE_CONVERSION)
    # vampytest.assert_is(TYPE_CONVERSION.get_converter, )
    # vampytest.assert_is(TYPE_CONVERSION.put_converter, )
    vampytest.assert_is(TYPE_CONVERSION.validator, validate_type)


def _iter_options__type__get_converter():
    yield None, StickerType.none
    yield StickerType.standard.value, StickerType.standard


@vampytest._(vampytest.call_from(_iter_options__type__get_converter()).returning_last())
def test__TYPE_CONVERSION__get_converter(input_value):
    """
    Tests whether `TYPE_CONVERSION.get_converter` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Raw value.
    
    Returns
    -------
    output : ``StickerType``
    """
    return TYPE_CONVERSION.get_converter(input_value)


def _iter_options__type__put_converter():
    yield StickerType.none, StickerType.none.value
    yield StickerType.standard, StickerType.standard.value


@vampytest._(vampytest.call_from(_iter_options__type__put_converter()).returning_last())
def test__TYPE_CONVERSION__put_converter(input_value):
    """
    Tests whether `TYPE_CONVERSION.put_converter` works as intended.
    
    Parameters
    ----------
    input_value : ``StickerType``
        Processed value.
    
    Returns
    -------
    output : `int`
    """
    return TYPE_CONVERSION.put_converter(input_value)

