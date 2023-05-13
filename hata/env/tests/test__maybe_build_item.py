import vampytest

from ..parsing import maybe_build_item


@vampytest.call_with(None, None, None)
@vampytest.call_with('a', None, ('a', None))
@vampytest.call_with(None, 'a', None)
@vampytest.call_with('a', 'b', ('a', 'b'))
def test__maybe_build_item(input_key, input_value, expected_output):
    """
    Tests whether ``maybe_build_item`` works as intended.
    """
    output = maybe_build_item(input_key, input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    vampytest.assert_eq(output, expected_output)
