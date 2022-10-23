import vampytest

from ..shared_helpers import create_identifier_custom_id_from_name


def test__create_identifier_custom_id_from_name():
    """
    Tests whether ``create_identifier_custom_id_from_name`` works as intended.
    """
    input = 'hello name'
    expected_output = 'hello_name'
    
    output = create_identifier_custom_id_from_name(input)
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, expected_output)
