import vampytest

from ....application_command import ApplicationCommandOptionType

from ..fields import put_type_into


def test__put_type_into():
    """
    Tests whether ``put_type_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (ApplicationCommandOptionType.sub_command, True, {'type': ApplicationCommandOptionType.sub_command.value}),
    ):
        data = put_type_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
