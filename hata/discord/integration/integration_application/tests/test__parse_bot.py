import vampytest

from ....user import User, ZEROUSER

from ..fields import parse_bot


def test__parse_bot():
    """
    Tests whether ``parse_bot`` works as intended.
    """
    user = User.precreate(202210080009, name = 'Ken', bot = True)
    
    for input_data, expected_output in (
        ({}, ZEROUSER),
        ({'bot': None}, ZEROUSER),
        ({'bot': user.to_data()}, user),
    ):
        output = parse_bot(input_data)
        vampytest.assert_is(output, expected_output)
