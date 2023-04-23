import vampytest

from ....interaction import InteractionType

from ..fields import parse_type


def test__parse_type():
    """
    Tests whether ``parse_type`` works as intended.
    """
    for input_data, expected_output in (
        ({'type': InteractionType.application_command.value}, InteractionType.application_command),
    ):
        output = parse_type(input_data)
        vampytest.assert_is(output, expected_output)
