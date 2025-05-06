import vampytest

from ..fields import put_topic


def test__put_topic():
    """
    Tests whether ``put_topic`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {'topic': ''}),
        ('a', False, {'topic': 'a'}),
    ):
        data = put_topic(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
