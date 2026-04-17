import vampytest

from ...forum_tag import ForumTag

from ..fields import parse_available_tags


def test__parse_available_tags():
    """
    Tests whether ``parse_available_tags`` works as intended.
    """
    forum_tag = ForumTag.precreate(202209110002, name = 'ExistRuth')
    
    for input_data, expected_output in (
        ({}, None),
        ({'available_tags': None}, None),
        ({'available_tags': []}, None),
        ({'available_tags': [forum_tag.to_data(include_internals = True)]}, (forum_tag, ))
    ):
        output = parse_available_tags(input_data)
        
        vampytest.assert_eq(output, expected_output)
