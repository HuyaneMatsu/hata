import vampytest

from ....user import ClientUserBase, User

from ..fields import validate_user


def _iter_options__passing():
    user = User.precreate(202308010000, name = 'Yukari')
    yield user, user
    yield None, None


def _iter_options__type_error():
    yield 'a'


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_user(input_value):
    output = validate_user(input_value)
    vampytest.assert_instance(output, ClientUserBase, nullable = True)
    return output
