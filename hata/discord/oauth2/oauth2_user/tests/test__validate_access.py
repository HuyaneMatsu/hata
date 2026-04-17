import vampytest

from ...oauth2_access import Oauth2Access

from ..fields import validate_access


def test__validate_access__0():
    """
    Tests whether ``validate_access` works as intended.
    
    Case: Passing.
    """
    access = Oauth2Access()
    output = validate_access(access)
    vampytest.assert_eq(access, output)


def test__validate_access__1():
    """
    Tests whether ``validate_access` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
        None,
    ):
        with vampytest.assert_raises(TypeError):
            validate_access(input_value)
