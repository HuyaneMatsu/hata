import vampytest

from ..applied_tag_ids import parse_applied_tag_ids


def test__parse_applied_tag_ids():
    """
    Tests whether ``parse_applied_tag_ids`` works as intended.
    """
    forum_tag_id_1 = 202209140020
    forum_tag_id_2 = 202209140021
    
    for input_data, expected_output in (
        ({}, None),
        ({'applied_tags': None}, None),
        ({'applied_tags': []}, None),
        ({'applied_tags': [str(forum_tag_id_1), str(forum_tag_id_2)]}, (forum_tag_id_1, forum_tag_id_2)),
        ({'applied_tags': [str(forum_tag_id_2), str(forum_tag_id_1)]}, (forum_tag_id_1, forum_tag_id_2)),
    ):
        output = parse_applied_tag_ids(input_data)
        vampytest.assert_eq(output, expected_output)
