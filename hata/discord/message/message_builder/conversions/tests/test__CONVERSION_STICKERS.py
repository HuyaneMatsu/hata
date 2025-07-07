import vampytest

from .....sticker import Sticker

from ..stickers import CONVERSION_STICKERS


def _iter_options__set_listing_identifier():
    yield [202402240040], []
    yield [202402240041, 202402240042], []
    yield [Sticker.precreate(202402240043)], [[202402240043]]
    yield [Sticker.precreate(202402240044), Sticker.precreate(202402240045)], [[202402240044, 202402240045]]
    
    yield [202402240046, 'mister'], []
    yield [Sticker.precreate(202402240047), 'mister'], []


@vampytest._(vampytest.call_from(_iter_options__set_listing_identifier()).returning_last())
def test__CONVERSION_STICKERS__set_listing_identifier(input_value):
    """
    Tests whether ``CONVERSION_STICKERS.set_listing_identifier`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test.
    
    Returns
    -------
    output : `list<list<int>>`
    """
    return [*CONVERSION_STICKERS.set_listing_identifier(input_value)]


def _iter_options__set_validator():
    yield object(), []
    yield None, [None]
    yield [], [None]
    yield (), [None]
    yield [202402240050], [[202402240050]]
    yield [202402240051, 202402240052], [[202402240051, 202402240052]]
    yield [Sticker.precreate(202402240053)], [[202402240053]]
    yield [Sticker.precreate(202402240054), Sticker.precreate(202402240055)], [[202402240054, 202402240055]]
    
    yield 'mister', []
    yield [202402240056, 'mister'], []
    yield [Sticker.precreate(202402240057), 'mister'], []
    
    yield 202402240058, [[202402240058]]
    yield Sticker.precreate(202402240059), [[202402240059]]


@vampytest._(vampytest.call_from(_iter_options__set_validator()).returning_last())
def test__CONVERSION_STICKERS__set_validator(input_value):
    """
    Tests whether ``CONVERSION_STICKERS.set_validator`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test.
    
    Returns
    -------
    output : `list<None | list<int>>`
    """
    return [*CONVERSION_STICKERS.set_validator(input_value)]


def _iter_options__get_processor():
    yield None, None
    yield [202402240060], [Sticker.precreate(202402240060)]
    yield [202402240061, 202402240062], [Sticker.precreate(202402240061), Sticker.precreate(202402240062)]


@vampytest._(vampytest.call_from(_iter_options__get_processor()).returning_last())
def test__CONVERSION_STICKERS__get_processor(input_value):
    """
    Tests whether ``CONVERSION_STICKERS.get_processor`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<int>`
        Value to test.
    
    Returns
    -------
    output :` `None | list<Sticker>``
    """
    return CONVERSION_STICKERS.get_processor(input_value)
