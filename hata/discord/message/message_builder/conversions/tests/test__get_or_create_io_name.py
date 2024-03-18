from os.path import join as join_paths

import vampytest

from ..attachments import _get_or_create_io_name


class TestType(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as exception:
            raise AttributeError from exception


def _iter_options():
    yield TestType(), 12, '12'
    yield TestType(name = 'hey'), 12, 'hey'
    yield TestType(name = join_paths('hey', 'mister')), 12, 'mister'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_or_create_io_name(input_value, mock_random_id_output):
    """
    Tests whether ``_get_or_create_io_name`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test on.
    mock_random_id_output : `int`
        Outcome of the mocked ``random_id`` function.
    
    Returns
    -------
    output : `str`
    """
    def random_id():
        nonlocal mock_random_id_output
        return mock_random_id_output
    
    mocked = vampytest.mock_globals(_get_or_create_io_name, random_id = random_id)
    output = mocked(input_value)
    return output
