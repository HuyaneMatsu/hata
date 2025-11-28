import vampytest

from ..utils import sanitise_links


def _iter_options():
    yield (
        None,
        None,
    )
    
    yield (
        '',
        '',
    )
    
    yield (
        '[orin](https://orincarding.nyan)',
        'orin',
    )
    
    yield (
        '[orin](http://orincarding.nyan)',
        'orin',
    )
    
    yield (
        '[a](https://a)[b](https://a)',
        'ab',
    )
    
    yield (
        'a[b](https://a)c',
        'abc',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__sanitise_links(content):
    """
    Tests whether ``sanitise_links`` works as intended.
    
    Parameters
    ----------
    content : `None | str`
        Content to sanitize.
    
    Returns
    -------
    output : `None | str`
    """
    output = sanitise_links(content)
    vampytest.assert_instance(output, str, nullable = True)
    return output
