import vampytest

from ..fields import parse_scopes
from ..preinstanced import Oauth2Scope


def test__parse_scopes():
    """
    Tests whether ``parse_scopes`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'scope': None}, None),
        ({'scope': ''}, None),
        ({'scope': Oauth2Scope.bot.value}, (Oauth2Scope.bot,)),
        (
            {'scope': ' '.join([Oauth2Scope.bot.value, Oauth2Scope.email.value])},
            (Oauth2Scope.bot, Oauth2Scope.email.value),
        ),
    ):
        output = parse_scopes(input_data)
        vampytest.assert_eq(output, expected_output)
