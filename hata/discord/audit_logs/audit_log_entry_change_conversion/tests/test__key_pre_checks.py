import vampytest

from ..key_pre_checks import key_pre_check_id


def _iter_options__key_pre_check_id():
    yield '', False
    yield '202311160007', True
    yield 'koishi', False


@vampytest._(vampytest.call_from(_iter_options__key_pre_check_id()).returning_last())
def test__key_pre_check_id(key):
    """
    Tests whether ``key_pre_check_id`` works as intended.
    
    Parameters
    ----------
    keys : `str`
        Key to check.
    
    Returns
    -------
    output : `bool`
    """
    return key_pre_check_id(key)
