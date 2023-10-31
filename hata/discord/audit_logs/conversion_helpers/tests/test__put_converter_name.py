import vampytest

from ..converters import put_converter_name


def _iter_options():
    name = 'koishi'
    yield '', ''
    yield name, name


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_converter_name(input_value):
    """
    Tests whether ``put_converter_name`` works as intended.
    
    Parameters
    ----------
    input_value : `str`
        Processed value.
    
    Returns
    -------
    output : `str`
    """
    return put_converter_name(input_value)
