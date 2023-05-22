import vampytest

from ..parsing import render_string_hidden_representation_into


@vampytest.call_with('', 2, '\'\'')
@vampytest.call_with('aabb', 2, '\'aabb\'')
@vampytest.call_with('aabb', 1, '\'a ... (+2 hidden) ... b\'')
@vampytest.call_with('aa\\b', 2, '\'aa\\\\b\'')
def test__render_string_hidden_representation_into(input_string, input_cut_at, expected_output_string):
    """
    Tests whether ``render_string_hidden_representation_into`.
    
    Parameters
    ----------
    input_string : `str`
        Input to pass tas a parameter.
    input_cut : `int`
        Input where to cut the string.
    expected_output_string : `str`
        The expected output as a joined string.
    """
    output = render_string_hidden_representation_into([], input_string, input_cut_at)
    
    vampytest.assert_instance(output, list)
    output_string = ''.join(output)
    vampytest.assert_eq(output_string, expected_output_string)
