import vampytest

from ..fields import parse_url_host_names


def _iter_options():
    yield (
        {},
        None,
    )
    
    yield (
        {
            'link_hostname': None,
        },
        None,
    )
    
    yield (
        {
            'link_hostname': [],
        },
        None,
    )
    
    yield (
        {
            'link_hostname': [
                'fry',
                'shrimp',
            ],
        },
        (
            'fry',
            'shrimp',
        ),
    )
    
    yield (
        {
            'link_hostname': [
                'shrimp',
                'fry',
            ],
        },
        (
            'fry',
            'shrimp',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_url_host_names(input_data):
    """
    Tests whether ``parse_url_host_names`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | tuple<str>`
    """
    output = parse_url_host_names(input_data)
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, str)
    
    return output
