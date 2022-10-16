import vampytest

from ..archived import put_archived_into


def test__put_archived_into():
    """
    Tests whether ``put_archived_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (False, False, {}),
        (False, True, {'thread_metadata': {'archived': False}}),
        (True, False, {'thread_metadata': {'archived': True}}),
    ):
        data = put_archived_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
