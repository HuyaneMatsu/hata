import vampytest

from ....message import MessageFlag

from ..flags import CONVERSION_FLAGS


def _iter_options__set_merger():
    yield 1, 1, 1
    yield 1, 2, 3


@vampytest._(vampytest.call_from(_iter_options__set_merger()).returning_last())
def test__CONVERSION_FLAGS__set_merger(input_value_0, input_value_1):
    """
    Tests whether ``CONVERSION_FLAGS.set_merger`` works as intended.
    
    Parameters
    ----------
    input_value_0 : `int`
        Value to test.
    input_value_1 : `int`
        Value to test.
    
    Returns
    -------
    output : `int`
    """
    return CONVERSION_FLAGS.set_merger(input_value_0, input_value_1)


def _iter_options__set_validator():
    yield object(), []
    yield None, [0]
    yield 1, [1]
    yield MessageFlag(1), [MessageFlag(1)]


@vampytest._(vampytest.call_from(_iter_options__set_validator()).returning_last())
def test__CONVERSION_FLAGS__set_validator(input_value):
    """
    Tests whether ``CONVERSION_FLAGS.set_validator`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test.
    
    Returns
    -------
    output : `list<int>`
    """
    return [*CONVERSION_FLAGS.set_validator(input_value)]


def _iter_options__get_processor():
    yield 1, MessageFlag(1)
    yield MessageFlag(1), MessageFlag(1)


@vampytest._(vampytest.call_from(_iter_options__get_processor()).returning_last())
def test__CONVERSION_FLAGS__get_processor(input_value):
    """
    Tests whether ``CONVERSION_FLAGS.get_processor`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Value to test.
    
    Returns
    -------
    output : ``MessageFlag``
    """
    output = CONVERSION_FLAGS.get_processor(input_value)
    vampytest.assert_instance(output, MessageFlag)
    return output


def _iter_options__serializer_optional():
    yield 0, []
    yield 1, [1]


@vampytest._(vampytest.call_from(_iter_options__serializer_optional()).returning_last())
def test__CONVERSION_FLAGS__serializer_optional(input_value):
    """
    Tests whether ``CONVERSION_FLAGS.serializer_optional`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Value to test.
    
    Returns
    -------
    output : `list<int>`
    """
    return [*CONVERSION_FLAGS.serializer_optional(input_value)]


def _iter_options__serializer_required():
    yield 0, 0
    yield 1, 1


@vampytest._(vampytest.call_from(_iter_options__serializer_required()).returning_last())
def test__CONVERSION_FLAGS__serializer_required(input_value):
    """
    Tests whether ``CONVERSION_FLAGS.serializer_required`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Value to test.
    
    Returns
    -------
    output : `int`
    """
    return CONVERSION_FLAGS.serializer_required(input_value)
