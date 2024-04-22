import vampytest


def _assert_list_of_str(value):
    """
    Asserts whether the given value is a list of strings.
    
    Parameters
    ----------
    value : `object`
    """
    vampytest.assert_instance(value, list)
    for element in value:
        vampytest.assert_instance(element, str)
