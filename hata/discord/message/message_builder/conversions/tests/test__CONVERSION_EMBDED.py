import vampytest

from .....embed import Embed

from ..embed import CONVERSION_EMBED


def _iter_options__set_type_processor():
    yield Embed('hey'), [Embed('hey')]


@vampytest._(vampytest.call_from(_iter_options__set_type_processor()).returning_last())
def test__CONVERSION_EMBED__set_type_processor(input_value):
    """
    Tests whether ``CONVERSION_EMBED.set_type_processor`` works as intended.
    
    Parameters
    ----------
    input_value : ``Embed``
        Value to test.
    
    Returns
    -------
    output : `list<Embed>`
    """
    return CONVERSION_EMBED.set_type_processor(input_value)


def _iter_options__set_validator():
    yield object(), []
    yield None, [None]
    yield Embed('hey'), [[Embed('hey')]]
    yield [Embed('hey')], [[Embed('hey')]]
    yield [], [None]
    yield [1], []
    yield [Embed('hey'), 2], []


@vampytest._(vampytest.call_from(_iter_options__set_validator()).returning_last())
def test__CONVERSION_EMBED__set_validator(input_value):
    """
    Tests whether ``CONVERSION_EMBED.set_validator`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test.
    
    Returns
    -------
    output : `list<None | list<Embed>>`
    """
    return [*CONVERSION_EMBED.set_validator(input_value)]


def _iter_options__get_processor():
    yield None, None
    yield [Embed('hey')], Embed('hey')
    yield [Embed('hey'), Embed('mister')], Embed('hey')


@vampytest._(vampytest.call_from(_iter_options__get_processor()).returning_last())
def test__CONVERSION_EMBED__get_processor(input_value):
    """
    Tests whether ``CONVERSION_EMBED.get_processor`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<Embed>`
        Value to test.
    
    Returns
    -------
    output : `None | Embed`
    """
    return CONVERSION_EMBED.get_processor(input_value)
