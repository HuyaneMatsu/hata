import vampytest

from .....channel import ForumTag

from ..applied_tags import CONVERSION_APPLIED_TAGS


def _iter_options__set_listing_identifier():
    yield [202403120040], []
    yield [202403120041, 202403120042], []
    yield [ForumTag.precreate(202403120043)], [[202403120043]]
    yield [ForumTag.precreate(202403120044), ForumTag.precreate(202403120045)], [[202403120044, 202403120045]]
    
    yield [202403120046, 'mister'], []
    yield [ForumTag.precreate(202403120047), 'mister'], []


@vampytest._(vampytest.call_from(_iter_options__set_listing_identifier()).returning_last())
def test__CONVERSION_APPLIED_TAGS__set_listing_identifier(input_value):
    """
    Tests whether ``CONVERSION_APPLIED_TAGS.set_listing_identifier`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test.
    
    Returns
    -------
    output : `list<list<int>>`
    """
    return [*CONVERSION_APPLIED_TAGS.set_listing_identifier(input_value)]


def _iter_options__set_validator():
    yield object(), []
    yield None, [None]
    yield [], [None]
    yield (), [None]
    yield [202403120050], [[202403120050]]
    yield [202403120051, 202403120052], [[202403120051, 202403120052]]
    yield [ForumTag.precreate(202403120053)], [[202403120053]]
    yield [ForumTag.precreate(202403120054), ForumTag.precreate(202403120055)], [[202403120054, 202403120055]]
    
    yield 'mister', []
    yield [202403120056, 'mister'], []
    yield [ForumTag.precreate(202403120057), 'mister'], []
    
    yield 202403120058, [[202403120058]]
    yield ForumTag.precreate(202403120059), [[202403120059]]


@vampytest._(vampytest.call_from(_iter_options__set_validator()).returning_last())
def test__CONVERSION_APPLIED_TAGS__set_validator(input_value):
    """
    Tests whether ``CONVERSION_APPLIED_TAGS.set_validator`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test.
    
    Returns
    -------
    output : `list<None | list<int>>`
    """
    return [*CONVERSION_APPLIED_TAGS.set_validator(input_value)]


def _iter_options__get_processor():
    yield None, None
    yield [202403120060], [ForumTag.precreate(202403120060)]
    yield [202403120061, 202403120062], [ForumTag.precreate(202403120061), ForumTag.precreate(202403120062)]


@vampytest._(vampytest.call_from(_iter_options__get_processor()).returning_last())
def test__CONVERSION_APPLIED_TAGS__get_processor(input_value):
    """
    Tests whether ``CONVERSION_APPLIED_TAGS.get_processor`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<int>`
        Value to test.
    
    Returns
    -------
    output : `None | list<ForumTag>`
    """
    return CONVERSION_APPLIED_TAGS.get_processor(input_value)
