import vampytest

from ....sticker.sticker.constants import SORT_VALUE_MIN
from ....sticker.sticker.fields import (
    validate_available, validate_description, validate_name, validate_sort_value, validate_tags
)

from ...conversion_helpers.converters import (
    get_converter_description, get_converter_name, put_converter_description, put_converter_name
)

from ..sticker import (
    AVAILABLE_CONVERSION, DESCRIPTION_CONVERSION, NAME_CONVERSION, SORT_VALUE_CONVERSION, STICKER_CONVERSIONS,
    TAGS_CONVERSION
)


def test__STICKER_CONVERSIONS():
    """
    Tests whether `STICKER_CONVERSIONS` contains conversion for every expected key.
    """
    vampytest.assert_eq(
        {*STICKER_CONVERSIONS.get_converters.keys()},
        {'available', 'description', 'name', 'sort_value', 'tags'},
    )

# ---- available ----

def test__AVAILABLE_CONVERSION__generic():
    """
    Tests whether ``AVAILABLE_CONVERSION`` works as intended.
    """
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
    vampytest.assert_is(DESCRIPTION_CONVERSION.get_converter, get_converter_description)
    vampytest.assert_is(DESCRIPTION_CONVERSION.put_converter, put_converter_description)
    vampytest.assert_is(DESCRIPTION_CONVERSION.validator, validate_description)


# ---- name ----

def test__NAME_CONVERSION__generic():
    """
    Tests whether ``NAME_CONVERSION`` works as intended.
    """
    vampytest.assert_is(NAME_CONVERSION.get_converter, get_converter_name)
    vampytest.assert_is(NAME_CONVERSION.put_converter, put_converter_name)
    vampytest.assert_is(NAME_CONVERSION.validator, validate_name)


# ---- sort_value ----

def test__SORT_VALUE_CONVERSION__generic():
    """
    Tests whether ``SORT_VALUE_CONVERSION`` works as intended.
    """
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
