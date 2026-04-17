import vampytest

from ..helpers import parse_oauth2_redirect_url


def test__parse_oauth2_redirect_url__0():
    """
    Tests whether ``parse_oauth2_redirect_url`` works as intended.
    
    Case: bad url.
    """
    url = 'https://orindance.party/'
    
    output = parse_oauth2_redirect_url(url)
    
    vampytest.assert_is(output, None)


def test__parse_oauth2_redirect_url__1():
    """
    Tests whether ``parse_oauth2_redirect_url`` works as intended.
    
    Case: Good url.
    """
    url = 'https://orindance.party/'
    code = 'a' * 30
    
    output = parse_oauth2_redirect_url(f'{url}?code={code}')
    
    vampytest.assert_eq(output, (url, code))
