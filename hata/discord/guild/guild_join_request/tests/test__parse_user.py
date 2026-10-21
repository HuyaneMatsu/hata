import vampytest

from ....user import ClientUserBase, User

from ..fields import parse_user


def _iter_options():
    user = User.precreate(202307310004, name = 'Yuuka')
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'user': None,
        },
        None,
    )
    
    yield (
        {
            'user': user.to_data(include_internals = True),
        },
        user,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_user(input_data):
    output = parse_user(input_data)
    vampytest.assert_instance(output, ClientUserBase, nullable = True)
    return output
