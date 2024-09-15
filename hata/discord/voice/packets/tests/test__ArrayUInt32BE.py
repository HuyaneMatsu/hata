import vampytest

from ..array import ArrayUInt32BE


def _assert_fields_set(array):
    """
    Asserts whether every fields are set of the given array.
    
    Parameters
    ----------
    array : ``ArrayUInt32BE``
        The array to check.
    """
    vampytest.assert_instance(array, ArrayUInt32BE)
    vampytest.assert_instance(array._data, bytes)
    vampytest.assert_instance(array._start, int)
    vampytest.assert_instance(array._end, int)


def test__ArrayUInt32BE__new():
    """
    Tests whether ``ArrayUInt32BE.__new__`` works as intended.
    """
    data = b'0' * 28
    start = 4
    end = 24
    
    array = ArrayUInt32BE(data, start, end)
    _assert_fields_set(array)
    
    vampytest.assert_eq(array._data, data)
    vampytest.assert_eq(array._start, start)
    vampytest.assert_eq(array._end, end)


def test__ArrayUInt32BE__len():
    """
    Tests whether ``ArrayUInt32BE.__len__`` works as intended.
    """
    data = b'0' * 28
    start = 4
    end = 24
    
    array = ArrayUInt32BE(data, start, end)
    
    output = len(array)
    vampytest.assert_instance(output, int)
    vampytest.assert_eq(output, 5)

    
def test__ArrayUInt32BE__getitem():
    """
    Tests whether ``ArrayUInt32BE.__getitem__`` works as intended.
    """
    data = b''.join(value.to_bytes(4, 'big') for value in range(7))
    start = 4
    end = 24
    
    array = ArrayUInt32BE(data, start, end)
    
    for index, expected_output in zip(range(5), range(1, 6)):
        output = array[index]
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, expected_output)


def test__ArrayUInt32BE__repr():
    """
    Tests whether ``ArrayUInt32BE.__repr__`` works as intended.
    """
    data = b'0' * 28
    start = 4
    end = 24
    
    array = ArrayUInt32BE(data, start, end)
    
    output = repr(array)
    vampytest.assert_instance(output, str)
   
    
def test__ArrayUInt32BE__iter():
    """
    Tests whether ``ArrayUInt32BE.__iter__`` works as intended.
    """
    data = b''.join(value.to_bytes(4, 'big') for value in range(7))
    start = 4
    end = 24
    
    array = ArrayUInt32BE(data, start, end)
    
    vampytest.assert_eq([*array], [*range(1, 6)],)
