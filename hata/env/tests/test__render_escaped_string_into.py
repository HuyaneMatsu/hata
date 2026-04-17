import vampytest

from ..parsing import render_escaped_string_into


@vampytest.call_with('aa', 'aa')
@vampytest.call_with('\\a\t', '\\\\a\\t')
def test__render_escaped_string_into(input_string, expected_output_string):
    """
    Tests whether ``render_escaped_string_into`` works as intended.
    
    Parameters
    ----------
    input_string : `str`
        Input to pass tas a parameter.
    expected_output_string : `str`
        The expected output as a joined string.
    """
    output = render_escaped_string_into([], input_string)
    
    vampytest.assert_instance(output, list)
    output_string = ''.join(output)
    vampytest.assert_eq(output_string, expected_output_string)
