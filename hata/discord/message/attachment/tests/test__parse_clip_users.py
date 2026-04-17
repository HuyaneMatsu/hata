import vampytest

from ....user import ClientUserBase, User

from ..fields import parse_clip_users


def _iter_options():
    user_id_0 = 202502020000
    user_id_1 = 202502020001
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'clip_participants': [],
        },
        None,
    )
    
    yield (
        {
            'clip_participants': [
                user_0.to_data(defaults = True, include_internals = True),
                user_1.to_data(defaults = True, include_internals = True),
            ],
        },
        (
            user_0,
            user_1,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_clip_users(input_data):
    """
    Tests whether ``parse_clip_users`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``None | tuple<ClientUserBase>``
    """
    output = parse_clip_users(input_data)
    
    vampytest.assert_instance(output, tuple, nullable = True)
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, ClientUserBase)
    
    return output
