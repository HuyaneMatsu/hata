import vampytest

from ..helpers import Oauth2Scope, join_oath2_scopes


def test__join_oath2_scopes():
    """
    Tests whether `join_oath2_scopes` works as expected.
    """
    for input_, expected_output in (
        (None, ''),
        ((Oauth2Scope.bot,), 'bot'),
        ((Oauth2Scope.bot, Oauth2Scope.email), 'bot email'),
    ):
        output = join_oath2_scopes(input_)
        vampytest.assert_eq(output, expected_output)
