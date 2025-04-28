import vampytest

from ..fields import parse_activity_application_ids


def _iter_options():
    application_id_0 = 202504210006
    application_id_1 = 202504210007
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'game_application_ids': None,
        },
        None,
    )
    
    yield (
        {
            'game_application_ids': [],
        },
        None,
    )
    
    yield (
        {
            'game_application_ids': [
                str(application_id_0),
                str(application_id_1),
            ],
        },
        (
            application_id_0,
            application_id_1,
        )
    )
    
    yield (
        {
            'game_application_ids': [
                str(application_id_1),
                str(application_id_0),
            ],
        },
        (
            application_id_1,
            application_id_0,
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_activity_application_ids(input_data):
    """
    Tests whether ``parse_activity_application_ids`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | tuple<int>`
    """
    output = parse_activity_application_ids(input_data)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output
