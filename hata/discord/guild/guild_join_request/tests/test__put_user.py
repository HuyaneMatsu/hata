import vampytest

from ....user import User

from ..fields import put_user


def _iter_options():
    user = User.precreate(202307310008, name = 'Ken')
    
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'user': None,
        },
    )
    
    yield (
        user,
        False,
        {
            'user': user.to_data(defaults = False, include_internals = True),
        },
    )
    yield (
        user,
        True,
        {
            'user': user.to_data(defaults = True, include_internals = True),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_user(input_value, defaults):
    return put_user(input_value, {}, defaults)
