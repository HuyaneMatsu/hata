import vampytest

from ....permission import Permission

from ..fields import parse_allow


def _iter_options():
    yield {'allow': '1111'}, Permission(1111)
    yield {'allow': 1111}, Permission(1111)
    yield {'allow': None}, Permission()
    yield {}, Permission()
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_allow(input_data):
    """
    Tests whether ``parse_allow`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data to parse the permission from.
    
    Returns
    -------
    output : ``Permission``
    """
    output = parse_allow(input_data)
    vampytest.assert_instance(output, Permission)
    return output
