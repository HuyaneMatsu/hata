import vampytest

from ....permission import Permission

from ..fields import parse_deny


def _iter_options():
    yield {'deny': '1111'}, Permission(1111)
    yield {'deny': 1111}, Permission(1111)
    yield {'deny': None}, Permission()
    yield {}, Permission()
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_deny(input_data):
    """
    Tests whether ``parse_deny`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data to parse the permission from.
    
    Returns
    -------
    output : ``Permission``
    """
    output = parse_deny(input_data)
    vampytest.assert_instance(output, Permission)
    return output
