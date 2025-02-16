import vampytest

from ..fields import put_expire_behavior
from ..preinstanced import IntegrationExpireBehavior


def test__put_expire_behavior():
    """
    Tests whether ``put_expire_behavior`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (IntegrationExpireBehavior.kick, False, {'expire_behavior': IntegrationExpireBehavior.kick.value}),
        (IntegrationExpireBehavior.remove_role, True, {'expire_behavior': IntegrationExpireBehavior.remove_role.value}),
    ):
        data = put_expire_behavior(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
