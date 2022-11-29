import vampytest

from ..fields import put_eula_id_into


def test__put_eula_id_into():
    """
    Tests whether ``put_eula_id_into`` is working as intended.
    """
    eula_id = 202211270007
    
    for input_, defaults, expected_output in (
        (0, False, {}),
        (0, True, {'eula_id': None}),
        (eula_id, False, {'eula_id': str(eula_id)}),
    ):
        data = put_eula_id_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
