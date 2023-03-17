import vampytest

from ....user import User, ZEROUSER

from ..fields import parse_creator


def test__parse_creator():
    """
    Tests whether ``parse_creator`` works as intended.
    """
    creator = User.precreate(202303140003, name = 'Orin')
    
    for input_data, expected_output in (
        ({}, ZEROUSER),
        ({'creator': None}, ZEROUSER),
        ({'creator': creator.to_data(defaults = True, include_internals = True)}, creator),
    ):
        output = parse_creator(input_data)
        vampytest.assert_is(output, expected_output)
