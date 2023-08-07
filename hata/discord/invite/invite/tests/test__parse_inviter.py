import vampytest

from ....user import User, ZEROUSER

from ..fields import parse_inviter


def _iter_options():
    user = User.precreate(202307310007, name = 'Yuuka')
    
    yield {}, ZEROUSER
    yield {'inviter': None}, ZEROUSER
    yield {'inviter': user.to_data(include_internals = True)}, user



@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_inviter(input_data):
    """
    Tests whether ``parse_inviter`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    inviter : ``ClientUserBase``
    """
    return parse_inviter(input_data)
