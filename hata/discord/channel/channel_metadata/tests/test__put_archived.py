import vampytest

from ..fields import put_archived


def test__put_archived():
    """
    Tests whether ``put_archived`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'thread_metadata': {'archived': False}}),
        (True, False, {'thread_metadata': {'archived': True}}),
    ):
        data = put_archived(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
