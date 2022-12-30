import vampytest

from ..fields import put_type_into
from ..preinstanced import IntegrationType


def test__put_type_into():
    """
    Tests whether ``put_type_into`` works as intended.
    """
    for input_, defaults, expected_output in (
        (IntegrationType.discord, False, {'type': IntegrationType.discord.value}),
    ):
        data = put_type_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
