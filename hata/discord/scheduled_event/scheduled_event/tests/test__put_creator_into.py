import vampytest

from ....user import User

from ..fields import put_creator_into


def test__put_creator_into():
    """
    Tests whether ``put_creator_into`` is working as intended.
    """
    creator = User.precreate(202303140004, name = 'Orin')
    
    for input_value, defaults, expected_output in (
        (creator, True, {'creator': creator.to_data(defaults = True, include_internals = True)}),
    ):
        data = put_creator_into(input_value, {}, defaults, include_internals = True)
        vampytest.assert_eq(data, expected_output)
