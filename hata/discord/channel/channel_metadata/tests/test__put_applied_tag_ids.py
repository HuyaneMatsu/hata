import vampytest

from ..fields import put_applied_tag_ids


def test__put_applied_tag_ids():
    """
    Tests whether ``put_applied_tag_ids`` is working as intended.
    """
    applied_tag_id = 202209140023
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'applied_tags': []}),
        ((applied_tag_id, ), False, {'applied_tags': [str(applied_tag_id)]}),
    ):
        data = put_applied_tag_ids(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
