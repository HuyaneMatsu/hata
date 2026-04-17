import vampytest

from ....user import ClientUserBase, User, ZEROUSER

from ..fields import parse_user


def _iter_options():
    user_id = 202404030000
    user = User.precreate(user_id)
    
    yield {}, ZEROUSER
    yield {'user_id': None}, ZEROUSER
    yield {'user_id': str(user_id)}, user


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_user(input_data):
    """
    Tests whether ``parse_user`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to try to parse the user identifier from.
    
    Returns
    -------
    output : ``ClientUserBase``
    """
    output = parse_user(input_data)
    vampytest.assert_instance(output, ClientUserBase)
    return output
