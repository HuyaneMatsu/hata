import vampytest

from .....sticker import Sticker

from ..sticker import CONVERSION_STICKER


def _iter_options__set_type_processor():
    sticker_id = 202403080000
    
    yield Sticker.precreate(sticker_id), [sticker_id]


@vampytest._(vampytest.call_from(_iter_options__set_type_processor()).returning_last())
def test__CONVERSION_STICKER__set_type_processor(input_value):
    """
    Tests whether ``CONVERSION_STICKER.set_type_processor`` works as intended.
    
    Parameters
    ----------
    input_value : ``Sticker``
        Value to test.
    
    Returns
    -------
    output : `list<int>`
    """
    return CONVERSION_STICKER.set_type_processor(input_value)


def _iter_options__set_validator():
    yield object(), []
    yield None, [None]
    yield [], [None]
    yield (), [None]
    yield [202402240016], [[202402240016]]
    yield [202402240017, 202402240019], [[202402240017, 202402240019]]
    yield [Sticker.precreate(202402240018)], [[202402240018]]
    yield [Sticker.precreate(202402240020), Sticker.precreate(202402240022)], [[202402240020, 202402240022]]
    
    yield 'mister', []
    yield [202402240024, 'mister'], []
    yield [Sticker.precreate(202402240021), 'mister'], []
    
    yield 202402240035, [[202402240035]]
    yield Sticker.precreate(202402240036), [[202402240036]]


@vampytest._(vampytest.call_from(_iter_options__set_validator()).returning_last())
def test__CONVERSION_STICKER__set_validator(input_value):
    """
    Tests whether ``CONVERSION_STICKER.set_validator`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test.
    
    Returns
    -------
    output : `list<None | list<int>>`
    """
    return [*CONVERSION_STICKER.set_validator(input_value)]


def _iter_options__get_processor():
    yield None, None
    yield [202402240037], Sticker.precreate(202402240037)
    yield [202402240038, 202402240039], Sticker.precreate(202402240038)


@vampytest._(vampytest.call_from(_iter_options__get_processor()).returning_last())
def test__CONVERSION_STICKER__get_processor(input_value):
    """
    Tests whether ``CONVERSION_STICKER.get_processor`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<int>`
        Value to test.
    
    Returns
    -------
    output : `None | Sticker`
    """
    return CONVERSION_STICKER.get_processor(input_value)
