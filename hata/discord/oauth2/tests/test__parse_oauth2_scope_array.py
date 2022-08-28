import vampytest

from ..helpers import Oauth2Scope, parse_oauth2_scope_array


def test__parse_oauth2_scope_array():
    """
    Tests whether ``parse_oauth2_scope_array`` works as intended.
    """
    for input_, expected_output in (
        (None, None),
        ([], None),
        ([Oauth2Scope.bot.value], (Oauth2Scope.bot,)),
        ([Oauth2Scope.email.value, Oauth2Scope.bot.value], (Oauth2Scope.bot, Oauth2Scope.email,)),
    ):
        output = parse_oauth2_scope_array(input_)
        vampytest.assert_eq(output, expected_output)
