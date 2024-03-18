import vampytest

from .....channel import ForumTag

from ..applied_tag_ids import CONVERSION_APPLIED_TAG_IDS


def _iter_options__set_validator():
    yield object(), []
    yield None, [None]
    yield [], [None]
    yield (), [None]
    yield [202403120000], [[202403120000]]
    yield [202403120001, 202403120002], [[202403120001, 202403120002]]
    yield [ForumTag.precreate(202403120005)], [[202403120005]]
    yield [ForumTag.precreate(202403120003), ForumTag.precreate(202403120004)], [[202403120003, 202403120004]]
    
    yield 'mister', []
    yield [202403120006, 'mister'], []
    yield [ForumTag.precreate(202403120007), 'mister'], []
    
    yield 202403120031, [[202403120031]]
    yield ForumTag.precreate(202403120032), [[202403120032]]


@vampytest._(vampytest.call_from(_iter_options__set_validator()).returning_last())
def test__CONVERSION_APPLIED_TAG_IDS__set_validator(input_value):
    """
    Tests whether ``CONVERSION_APPLIED_TAG_IDS.set_validator`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test.
    
    Returns
    -------
    output : `list<None | list<int>>`
    """
    return [*CONVERSION_APPLIED_TAG_IDS.set_validator(input_value)]


def _iter_options__serializer_optional():
    yield None, []
    yield [202403120008], [[str(202403120008)]]
    yield [202403120009, 202403120010], [[str(202403120009), str(202403120010)]]


@vampytest._(vampytest.call_from(_iter_options__serializer_optional()).returning_last())
def test__CONVERSION_APPLIED_TAG_IDS__serializer_optional(input_value):
    """
    Tests whether ``CONVERSION_APPLIED_TAG_IDS.serializer_optional`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<int>`
        Value to test.
    
    Returns
    -------
    output : `list<None | list<int>`
    """
    return [*CONVERSION_APPLIED_TAG_IDS.serializer_optional(input_value)]


def _iter_options__serializer_required():
    yield None, None
    yield [202403120011], [str(202403120011)]
    yield [202403120012, 202403120013], [str(202403120012), str(202403120013)]


@vampytest._(vampytest.call_from(_iter_options__serializer_required()).returning_last())
def test__CONVERSION_APPLIED_TAG_IDS__serializer_required(input_value):
    """
    Tests whether ``CONVERSION_APPLIED_TAG_IDS.serializer_required`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<int>`
        Value to test.
    
    Returns
    -------
    output : `list<None | list<int>`
    """
    return CONVERSION_APPLIED_TAG_IDS.serializer_required(input_value)
