import vampytest

from ..base import InteractionMetadataBase


def test__InteractionMetadataBase__iter_options():
    """
    Tests whether ``InteractionMetadataBase.iter_options`` works as intended.
    """
    interaction_metadata = InteractionMetadataBase()
    
    vampytest.assert_eq([*interaction_metadata.iter_options()], [])


def test__InteractionMetadataBase__focused_option__no_focused_option():
    """
    Tests whether ``InteractionMetadataBase.focused_option`` works as intended.
    
    Case: nope.
    """
    interaction_metadata = InteractionMetadataBase()
    
    vampytest.assert_is(interaction_metadata.focused_option, None)


def test__InteractionMetadataBase__get_non_focused_values():
    """
    Tests whether ``InteractionMetadataBase.get_non_focused_values`` works as intended.
    """
    interaction_metadata = InteractionMetadataBase()
    
    vampytest.assert_eq(interaction_metadata.get_non_focused_values(), {})


def test__InteractionMetadataBase__get_value_of():
    """
    Tests whether ``InteractionMetadataBase.get_value_of`` works as intended.
    """
    interaction_metadata = InteractionMetadataBase()
    
    vampytest.assert_eq(interaction_metadata.get_value_of(), None)


def test__InteractionMetadataBase__value__no_value():
    """
    Tests whether ``InteractionMetadataBase.value`` works as intended.
    
    Case: nope.
    """
    interaction_metadata = InteractionMetadataBase()
    
    vampytest.assert_is(interaction_metadata.value, None)
