import vampytest

from ..fields import put_rpc_origins_into


def test__put_rpc_origins_into():
    """
    Tests whether ``put_rpc_origins_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'rpc_origins': []}),
        (('https://orindance.party/', ), False, {'rpc_origins': ['https://orindance.party/']}),
    ):
        data = put_rpc_origins_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
