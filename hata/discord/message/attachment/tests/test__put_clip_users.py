import vampytest

from ....user import User

from ..fields import put_clip_users


def _iter_options():
    user_id_0 = 202502020002
    user_id_1 = 202502020003
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)

    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'clip_participants': [],
        },
    )
    
    yield (
        (user_0, user_1),
        False,
        {
            'clip_participants': [
                user_0.to_data(defaults = False, include_internals = True),
                user_1.to_data(defaults = False, include_internals = True),
            ],
        },
    )
    
    yield (
        (user_0, user_1),
        True,
        {
            'clip_participants': [
                user_0.to_data(defaults = True, include_internals = True),
                user_1.to_data(defaults = True, include_internals = True),
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_clip_users(input_value, defaults):
    """
    Tests whether ``put_clip_users`` works as intended.
    
    Parameters
    ----------
    input_value : ``None | tuple<ClientUserBase>``
        Value to serialise.
    
    defaults : `bool`
        Whether default values should be serialised as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_clip_users(input_value, {}, defaults)
