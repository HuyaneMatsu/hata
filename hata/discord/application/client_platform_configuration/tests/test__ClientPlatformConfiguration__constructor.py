from datetime import datetime as DateTime

import vampytest

from ..client_platform_configuration import ClientPlatformConfiguration
from ..preinstanced import LabelType, ReleasePhase


def _assert_fields_set(configuration):
    """
    Asserts whether all fields are set of the given client platform configuration.
    
    Parameters
    ----------
    configuration : ``ClientPlatformConfiguration``
    """
    vampytest.assert_instance(configuration, ClientPlatformConfiguration)
    vampytest.assert_instance(configuration.label_type, LabelType)
    vampytest.assert_instance(configuration.labelled_until, DateTime, nullable = True)
    vampytest.assert_instance(configuration.release_phase, ReleasePhase)


def test__ClientPlatformConfiguration__new__no_fields():
    """
    Tests whether ``ClientPlatformConfiguration.__new__`` works as intended.
    
    Case: No fields given.
    """
    configuration = ClientPlatformConfiguration()
    _assert_fields_set(configuration)


def test__ClientPlatformConfiguration__new__all_fields():
    """
    Tests whether ``ClientPlatformConfiguration.__new__`` works as intended.
    
    Case: All fields given.
    """
    label_type = LabelType.new
    labelled_until = DateTime(2016, 5, 14)
    release_phase = ReleasePhase.global_launch
    
    configuration = ClientPlatformConfiguration(
        label_type = label_type,
        labelled_until = labelled_until,
        release_phase = release_phase,
    )
    _assert_fields_set(configuration)
    
    vampytest.assert_is(configuration.label_type, label_type)
    vampytest.assert_eq(configuration.labelled_until, labelled_until)
    vampytest.assert_is(configuration.release_phase, release_phase)
