import vampytest

from ..fields import put_activity_application_ids


def _iter_options():
    application_id = 202504210008
    
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'game_application_ids': [],
        },
    )
    
    yield (
        (application_id,),
        False,
        {
            'game_application_ids': [
                str(application_id),
            ]
        },
    )
    
    yield (
        (application_id,),
        True,
        {
            'game_application_ids': [
                str(application_id),
            ]
        },
    )
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_activity_application_ids(input_value, defaults):
    """
    Tests whether ``put_activity_application_ids`` is working as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<int>`
        Role identifiers to serialize.
    
    defaults : `bool`
        Whether fields with their default values should be included.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_activity_application_ids(input_value, {}, defaults)
