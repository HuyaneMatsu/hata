import vampytest

from ....interaction import InteractionType

from ..fields import put_type_into


def test__put_type_into():
    """
    Tests whether ``put_type_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (InteractionType.application_command, False, {'type': InteractionType.application_command.value}),
    ):
        data = put_type_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
