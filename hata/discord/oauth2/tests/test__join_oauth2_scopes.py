import vampytest

from ..helpers import Oauth2Scope, join_oauth2_scopes


def test__join_oauth2_scopes():
    """
    Tests whether `join_oauth2_scopes` works as expected.
    """
    for input_value, expected_output in (
        (None, ''),
        ((Oauth2Scope.bot,), 'bot'),
        ((Oauth2Scope.bot, Oauth2Scope.email), 'bot email'),
    ):
        output = join_oauth2_scopes(input_value)
        vampytest.assert_eq(output, expected_output)
