import vampytest

from ..parsing import (
    is_character_comment, is_character_equal, is_character_identifier_continuous, is_character_identifier_starter,
    is_character_non_comment_or_line_break, is_character_per_n, is_character_per_r, is_character_white_space
)


@vampytest.call_with(' ', True)
@vampytest.call_with('\t', True)
@vampytest.call_with('\n', False)
@vampytest.call_with('\r', False)
@vampytest.call_with('1', False)
@vampytest.call_with('a', False)
@vampytest.call_with('_', False)
@vampytest.call_with('=', False)
@vampytest.call_with('#', False)
def test__is_character_white_space(input_value, expected_output):
    """
    Tests whether ``is_character_white_space`` works as intended.
    """
    output = is_character_white_space(input_value)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, expected_output)


@vampytest.call_with(' ', False)
@vampytest.call_with('\t', False)
@vampytest.call_with('\n', False)
@vampytest.call_with('\r', True)
@vampytest.call_with('1', False)
@vampytest.call_with('a', False)
@vampytest.call_with('Z', False)
@vampytest.call_with('_', False)
@vampytest.call_with('=', False)
@vampytest.call_with('#', False)
def test__is_character_per_r(input_value, expected_output):
    """
    Tests whether ``is_character_per_r`` works as intended.
    """
    output = is_character_per_r(input_value)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, expected_output)


@vampytest.call_with(' ', False)
@vampytest.call_with('\t', False)
@vampytest.call_with('\n', True)
@vampytest.call_with('\r', False)
@vampytest.call_with('1', False)
@vampytest.call_with('a', False)
@vampytest.call_with('Z', False)
@vampytest.call_with('_', False)
@vampytest.call_with('=', False)
@vampytest.call_with('#', False)
def test__is_character_per_n(input_value, expected_output):
    """
    Tests whether ``is_character_per_n`` works as intended.
    """
    output = is_character_per_n(input_value)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, expected_output)


@vampytest.call_with(' ', True)
@vampytest.call_with('\t', True)
@vampytest.call_with('\n', False)
@vampytest.call_with('\r', False)
@vampytest.call_with('1', True)
@vampytest.call_with('a', True)
@vampytest.call_with('Z', True)
@vampytest.call_with('_', True)
@vampytest.call_with('=', True)
@vampytest.call_with('#', False)
def test__is_character_non_comment(input_value, expected_output):
    """
    Tests whether ``is_character_non_comment`` works as intended.
    """
    output = is_character_non_comment_or_line_break(input_value)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, expected_output)


@vampytest.call_with(' ', False)
@vampytest.call_with('\t', False)
@vampytest.call_with('\n', False)
@vampytest.call_with('\r', False)
@vampytest.call_with('1', False)
@vampytest.call_with('a', False)
@vampytest.call_with('Z', False)
@vampytest.call_with('_', False)
@vampytest.call_with('=', False)
@vampytest.call_with('#', True)
def test__is_character_comment(input_value, expected_output):
    """
    Tests whether ``is_character_comment`` works as intended.
    """
    output = is_character_comment(input_value)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, expected_output)


@vampytest.call_with(' ', False)
@vampytest.call_with('\t', False)
@vampytest.call_with('\n', False)
@vampytest.call_with('\r', False)
@vampytest.call_with('1', False)
@vampytest.call_with('a', False)
@vampytest.call_with('Z', False)
@vampytest.call_with('_', False)
@vampytest.call_with('=', True)
@vampytest.call_with('#', False)
def test__is_character_equal(input_value, expected_output):
    """
    Tests whether ``is_character_equal`` works as intended.
    """
    output = is_character_equal(input_value)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, expected_output)


@vampytest.call_with(' ', False)
@vampytest.call_with('\t', False)
@vampytest.call_with('\n', False)
@vampytest.call_with('\r', False)
@vampytest.call_with('1', False)
@vampytest.call_with('a', True)
@vampytest.call_with('Z', True)
@vampytest.call_with('_', True)
@vampytest.call_with('=', False)
@vampytest.call_with('#', False)
def test__is_character_identifier_starter(input_value, expected_output):
    """
    Tests whether ``is_character_identifier_starter`` works as intended.
    """
    output = is_character_identifier_starter(input_value)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, expected_output)


@vampytest.call_with(' ', False)
@vampytest.call_with('\t', False)
@vampytest.call_with('\n', False)
@vampytest.call_with('\r', False)
@vampytest.call_with('1', True)
@vampytest.call_with('a', True)
@vampytest.call_with('Z', True)
@vampytest.call_with('_', True)
@vampytest.call_with('=', False)
@vampytest.call_with('#', False)
def test__is_character_identifier_continuous(input_value, expected_output):
    """
    Tests whether ``is_character_identifier_continuous`` works as intended.
    """
    output = is_character_identifier_continuous(input_value)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, expected_output)
