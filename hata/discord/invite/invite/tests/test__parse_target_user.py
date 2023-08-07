import vampytest

from ....user import User

from ..fields import parse_target_user


def _iter_options():
    user = User.precreate(202308030003, name = 'Yuuka')
    
    yield {}, None
    yield {'target_user': None}, None
    yield {'target_user': user.to_data(include_internals = True)}, user


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_target_user(input_data):
    """
    Tests whether ``parse_target_user`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    target_user : `None`, ``ClientUserBase``
    """
    return parse_target_user(input_data)
