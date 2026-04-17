import vampytest

from .....sticker import Sticker

from ..sticker_ids import CONVERSION_STICKER_IDS


def _iter_options__set_validator():
    yield object(), []
    yield None, [None]
    yield [], [None]
    yield (), [None]
    yield [202402240000], [[202402240000]]
    yield [202402240001, 202402240002], [[202402240001, 202402240002]]
    yield [Sticker.precreate(202402240005)], [[202402240005]]
    yield [Sticker.precreate(202402240003), Sticker.precreate(202402240004)], [[202402240003, 202402240004]]
    
    yield 'mister', []
    yield [202402240006, 'mister'], []
    yield [Sticker.precreate(202402240007), 'mister'], []
    
    yield 202402240031, [[202402240031]]
    yield Sticker.precreate(202402240032), [[202402240032]]


@vampytest._(vampytest.call_from(_iter_options__set_validator()).returning_last())
def test__CONVERSION_STICKER_IDS__set_validator(input_value):
    """
    Tests whether ``CONVERSION_STICKER_IDS.set_validator`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test.
    
    Returns
    -------
    output : `list<None | list<int>>`
    """
    return [*CONVERSION_STICKER_IDS.set_validator(input_value)]


def _iter_options__serializer_optional():
    yield None, []
    yield [202402240008], [[str(202402240008)]]
    yield [202402240009, 202402240010], [[str(202402240009), str(202402240010)]]


@vampytest._(vampytest.call_from(_iter_options__serializer_optional()).returning_last())
def test__CONVERSION_STICKER_IDS__serializer_optional(input_value):
    """
    Tests whether ``CONVERSION_STICKER_IDS.serializer_optional`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<int>`
        Value to test.
    
    Returns
    -------
    output : `list<None | list<int>`
    """
    return [*CONVERSION_STICKER_IDS.serializer_optional(input_value)]


def _iter_options__serializer_required():
    yield None, None
    yield [202402240011], [str(202402240011)]
    yield [202402240012, 202402240013], [str(202402240012), str(202402240013)]


@vampytest._(vampytest.call_from(_iter_options__serializer_required()).returning_last())
def test__CONVERSION_STICKER_IDS__serializer_required(input_value):
    """
    Tests whether ``CONVERSION_STICKER_IDS.serializer_required`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<int>`
        Value to test.
    
    Returns
    -------
    output : `list<None | list<int>`
    """
    return CONVERSION_STICKER_IDS.serializer_required(input_value)
