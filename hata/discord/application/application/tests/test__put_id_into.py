import vampytest

from ..fields import put_id_into


def test__put_id_into():
    """
    Tests whether ``put_id_into`` is working as intended.
    """
    application_id = 202211270012
    
    for input_, defaults, expected_output in (
        (0, False, {'id': None}),
        (0, True, {'id': None}),
        (application_id, False, {'id': str(application_id)}),
    ):
        data = put_id_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
