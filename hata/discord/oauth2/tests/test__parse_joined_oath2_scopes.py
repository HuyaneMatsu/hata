import vampytest

from ..helpers import parse_joined_oath2_scopes


def test__parse_joined_oath2_scopes_0():
    """
    Tests whether ``parse_joined_oath2_scopes`` works as intended.
    Case : empty string
    """
    vampytest.assert_is(parse_joined_oath2_scopes(''), None)


def test__parse_joined_oath2_scopes_1():
    """
    Tests whether ``parse_joined_oath2_scopes`` works as intended.
    Case : non-empty string
    """
    vampytest.assert_eq(parse_joined_oath2_scopes('bot'), ('bot',))


def test__parse_joined_oath2_scopes_2():
    """
    Tests whether ``parse_joined_oath2_scopes`` works as intended.
    Case : scopes with different order
    """
    vampytest.assert_eq(parse_joined_oath2_scopes('bot email'), parse_joined_oath2_scopes('email bot'))
