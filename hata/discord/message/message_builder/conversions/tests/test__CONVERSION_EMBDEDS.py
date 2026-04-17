import vampytest

from .....embed import Embed

from ..embeds import CONVERSION_EMBEDS


def _iter_options__set_listing_identifier():
    yield [Embed('hey')], [[Embed('hey')]]
    yield [1], []
    yield [Embed('hey'), 1], []


@vampytest._(vampytest.call_from(_iter_options__set_listing_identifier()).returning_last())
def test__CONVERSION_EMBEDS__set_listing_identifier(input_value):
    """
    Tests whether ``CONVERSION_EMBEDS.set_listing_identifier`` works as intended.
    
    Parameters
    ----------
    input_value : `list<object>`
        Value to test.
    
    Returns
    -------
    output : `list<list<Embed>>`
    """
    return [*CONVERSION_EMBEDS.set_listing_identifier(input_value)]


def _iter_options__set_validator():
    yield object(), []
    yield None, [None]
    yield Embed('hey'), [[Embed('hey')]]
    yield [Embed('hey')], [[Embed('hey')]]
    yield [], [None]
    yield [1], []
    yield [Embed('hey'), 2], []


@vampytest._(vampytest.call_from(_iter_options__set_validator()).returning_last())
def test__CONVERSION_EMBEDS__set_validator(input_value):
    """
    Tests whether ``CONVERSION_EMBEDS.set_validator`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test.
    
    Returns
    -------
    output : `list<None | list<Embed>>`
    """
    return [*CONVERSION_EMBEDS.set_validator(input_value)]


def _iter_options__serializer_optional():
    yield None, []
    yield [Embed('hey')], [[Embed('hey').to_data()]]
    yield [Embed('hey'), Embed('mister')], [[Embed('hey').to_data(), Embed('mister').to_data()]]


@vampytest._(vampytest.call_from(_iter_options__serializer_optional()).returning_last())
def test__CONVERSION_EMBEDS__serializer_optional(input_value):
    """
    Tests whether ``CONVERSION_EMBEDS.serializer_optional`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<Embed>`
        Value to test.
    
    Returns
    -------
    output : `list<None | list<dict<str, object>>>`
    """
    return [*CONVERSION_EMBEDS.serializer_optional(input_value)]


def _iter_options__serializer_required():
    yield None, None
    yield [Embed('hey')], [Embed('hey').to_data()]
    yield [Embed('hey'), Embed('mister')], [Embed('hey').to_data(), Embed('mister').to_data()]


@vampytest._(vampytest.call_from(_iter_options__serializer_required()).returning_last())
def test__CONVERSION_EMBEDS__serializer_required(input_value):
    """
    Tests whether ``CONVERSION_EMBEDS.serializer_required`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<Embed>`
        Value to test.
    
    Returns
    -------
    output : `None | list<dict<str, object>>`
    """
    return CONVERSION_EMBEDS.serializer_required(input_value)
