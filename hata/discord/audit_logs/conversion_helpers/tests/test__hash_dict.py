import vampytest

from ..helpers import _hash_dict


def test__hash_dict():
    """
    Tests whether ``_hash_dict`` works as intended.
    """
    output = _hash_dict({'hey': 'mister', 'scared': 'noises'})
    vampytest.assert_instance(output, int)
