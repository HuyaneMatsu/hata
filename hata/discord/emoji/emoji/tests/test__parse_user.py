import vampytest

from ....user import User, ZEROUSER

from ..fields import parse_user


def _iter_options():
    user = User.precreate(202307310001, name = 'Yuuka')
    
    yield {}, ZEROUSER
    yield {'user': None}, ZEROUSER
    yield {'user': user.to_data(include_internals = True)}, user



@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_user(input_data):
    """
    Tests whether ``parse_user`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    user : ``ClientUserBase``
    """
    return parse_user(input_data)
