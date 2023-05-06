import vampytest

from ..fields import put_application_id_into


def test__put_application_id_into():
    """
    Tests whether ``put_application_id_into`` works as intended.
    """
    application_id = 202304280051
    webhook_id = 202304280052
    
    for input_value, input_data, defaults, expected_output in (
        (0, {}, True, {'application_id': None}),
        (0, {}, False, {}),
        (0, {'webhook_id': str(webhook_id)}, True, {'webhook_id': str(webhook_id), 'application_id': None}),
        (0, {'webhook_id': str(webhook_id)}, False, {'webhook_id': str(webhook_id)}),
        (application_id, {}, False, {'application_id': str(application_id), 'webhook_id': str(application_id)}),
        (
            application_id,
            {'webhook_id': None},
            False,
            {'application_id': str(application_id), 'webhook_id': str(application_id)},
        ),
        (
            application_id,
            {'webhook_id': str(webhook_id)},
            False,
            {'application_id': str(application_id), 'webhook_id': str(webhook_id)},
        ),
    ):
        output_data = put_application_id_into(input_value, input_data.copy(), defaults)
        vampytest.assert_eq(output_data, expected_output)
