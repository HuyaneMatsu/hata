import vampytest

from ....oauth2 import Oauth2Scope

from ..fields import parse_scopes


def test__parse_scopes():
    """
    Tests whether ``parse_scopes`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'scopes': None}, None),
        ({'scopes': []}, None),
        ({'scopes': [Oauth2Scope.bot.value]}, (Oauth2Scope.bot.value,)),
    ):
        output = parse_scopes(input_data)
        vampytest.assert_eq(output, expected_output)
