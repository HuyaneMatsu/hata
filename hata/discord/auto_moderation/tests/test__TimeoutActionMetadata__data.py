import vampytest

from .. import TimeoutActionMetadata


def test__TimeoutActionMetadata__to_data():
    """
    Tests whether ``TimeoutActionMetadata``'s `to_data` method works as expected.
    """
    metadata = TimeoutActionMetadata(0)
    
    vampytest.assert_eq(
        metadata.to_data(),
        {
            'duration_seconds': 0,
        },
    )

    
def test__TimeoutActionMetadata__from_data():
    """
    Tests whether ``TimeoutActionMetadata``'s `from_data` method works as expected.
    """
    metadata = TimeoutActionMetadata.from_data({
        'duration_seconds': 0,
    })
    
    vampytest.assert_eq(
        metadata,
        TimeoutActionMetadata(0),
    )
