import vampytest

from ..parsing import embed_error_code, uproot_error_code, PARSED_STATE_FAILURE


@vampytest.call_with(PARSED_STATE_FAILURE, 0)
@vampytest.call_with(PARSED_STATE_FAILURE, 12)
def test__embed_and_uproot_error_code(parsed_state, error_code):
    """
    Tests whether ``embed_error_code`` and ``uproot_error_code`` works as intended.
    
    Parameters
    ----------
    parsed_state : `int`
        Input parsed state to embed the error code into.
    error_code : `int`
        The error code to embed.
    """
    embed_output = embed_error_code(parsed_state, error_code)
    vampytest.assert_instance(embed_output, int)
    vampytest.assert_true(embed_output & parsed_state)
    
    uproot_output = uproot_error_code(embed_output)
    vampytest.assert_instance(uproot_output, int)
    vampytest.assert_eq(uproot_output, error_code)
