import vampytest

from ..shared_helpers import create_auto_custom_id


def test__create_auto_custom_id():
    """
    Tests whether `create_auto_custom_id` works as intended.
    """
    custom_id = create_auto_custom_id()
    
    vampytest.assert_instance(custom_id, str)
    vampytest.assert_true(custom_id)
