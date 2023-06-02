import vampytest

from ..command import _build_scaffold_description


def test__build_scaffold_description():
    """
    Tests whether ``_build_scaffold_description`` works as intended.
    """
    output = _build_scaffold_description()
    vampytest.assert_instance(output, str)
