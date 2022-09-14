import vampytest


from ..topic import put_topic_into


def test__put_topic_into():
    """
    Tests whether ``put_topic_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (None, False, {'topic': ''}),
        ('a', False, {'topic': 'a'}),
    ):
        data = put_topic_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
