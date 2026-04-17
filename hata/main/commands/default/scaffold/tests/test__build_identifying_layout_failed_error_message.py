import vampytest

from ..helpers import _build_identifying_layout_failed_error_message


def test__build_identifying_layout_failed_error_message():
    """
    Tests whether ``_build_identifying_layout_failed_error_message`` works as intended.
    """
    output = _build_identifying_layout_failed_error_message('nue')
    vampytest.assert_instance(output, str)
