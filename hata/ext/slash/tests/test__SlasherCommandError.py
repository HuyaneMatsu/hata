import vampytest

from ..exceptions import SlasherCommandError


def _assert_fields_set(exception):
    """
    Asserts whether ``SlasherCommandError`` has every of its attributes set.
    
    Parameters
    ----------
    exception : ``SlasherCommandError``
        The exception to test.
    """
    vampytest.assert_instance(exception, SlasherCommandError)


def test__SlasherCommandError__new():
    """
    Tests whether ``SlasherCommandError.__new__`` works as intended.
    """
    exception = SlasherCommandError()
    _assert_fields_set(exception)


def _iter_options__pretty_repr():
    yield (), ''


@vampytest._(vampytest.call_from(_iter_options__pretty_repr()).returning_last())
def test__SlasherCommandError__pretty_repr(parameters):
    """
    Tests whether ``SlasherCommandError.pretty_repr`` works as intended.
    
    Parameters
    ----------
    parameters : `tuple<object>`
        Parameters to create the exception from.
    
    Returns
    -------
    output : `str`
    """
    exception = SlasherCommandError(*parameters)
    
    output = exception.pretty_repr
    vampytest.assert_instance(output, str)
    return output


def test__SlasherCommandError__repr():
    """
    Tests whether ``SlasherCommandError.__repr__`` works as intended.
    """
    exception = SlasherCommandError()
    
    output = repr(exception)
    
    vampytest.assert_instance(output, str)
    vampytest.assert_in(type(exception).__name__, output)


def _iter_options__eq__same_type():
    yield (), (), True


@vampytest._(vampytest.call_from(_iter_options__eq__same_type()).returning_last())
def test__SlasherCommandError__eq__same_type(parameters_0, parameters_1):
    """
    Tests whether ``SlasherCommandError.__eq__`` works as intended.
    
    Case: same type.
    
    Parameters
    ----------
    parameters_0 : `tuple<object>`
        Parameters to create exception from.
    parameters_0 : `tuple<object>`
        Parameters to create exception from.
    
    Returns
    -------
    output : `bool`
    """
    exception_0 = SlasherCommandError(*parameters_0)
    exception_1 = SlasherCommandError(*parameters_1)
    
    output = exception_0 == exception_1
    vampytest.assert_instance(output, bool)
    return output



def _iter_options__eq__different_type():
    yield None, False
    yield object(), False


@vampytest._(vampytest.call_from(_iter_options__eq__different_type()).returning_last())
def test__SlasherCommandError__eq__different_type(other):
    """
    Tests whether ``SlasherCommandError.__eq__`` works as intended.
    
    Case: different type.
    
    Parameters
    ----------
    other : `object`
        Other object to compare the exception to.
    
    Returns
    -------
    output : `bool`
    """
    exception = SlasherCommandError()
    
    output = exception == other
    vampytest.assert_instance(output, bool)
    return output


def test__SlasherCommandError__hash():
    """
    Tests whether ``SlasherCommandError.__hash__`` works as intended.
    """
    exception = SlasherCommandError()
    
    output = hash(exception)
    vampytest.assert_instance(output, int)
