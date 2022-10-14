import vampytest

from ..fields import put_type_into
from ..integration_type import IntegrationType


def test__put_type_into():
    """
    Tests whether ``put_type_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (IntegrationType.discord, False, {'type': IntegrationType.discord.value}),
    ):
        data = put_type_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
