import vampytest

from ..fields import put_webhook_name


def test__put_webhook_name():
    """
    Tests whether ``put_webhook_name`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        ('', False, {'name': ''}),
        ('a', False, {'name': 'a'}),
    ):
        data = put_webhook_name(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
