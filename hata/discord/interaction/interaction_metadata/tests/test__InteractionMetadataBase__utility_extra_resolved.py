import vampytest

from ..base import InteractionMetadataBase


def test__InteractionMetadataBase__resolve_attachment():
    """
    Tests whether ``InteractionMetadataBase.resolve_attachment`` works as intended.
    """
    vampytest.assert_is(InteractionMetadataBase().resolve_attachment(0), None)


def test__InteractionMetadataBase__resolve_channel():
    """
    Tests whether ``InteractionMetadataBase.resolve_channel`` works as intended.
    """
    vampytest.assert_is(InteractionMetadataBase().resolve_attachment(0), None)


def test__InteractionMetadataBase__resolve_role():
    """
    Tests whether ``InteractionMetadataBase.resolve_role`` works as intended.
    """
    vampytest.assert_is(InteractionMetadataBase().resolve_attachment(0), None)


def test__InteractionMetadataBase__resolve_message():
    """
    Tests whether ``InteractionMetadataBase.resolve_message`` works as intended.
    """
    vampytest.assert_is(InteractionMetadataBase().resolve_attachment(0), None)


def test__InteractionMetadataBase__resolve_user():
    """
    Tests whether ``InteractionMetadataBase.resolve_user`` works as intended.
    """
    vampytest.assert_is(InteractionMetadataBase().resolve_attachment(0), None)


def test__InteractionMetadataBase__resolve_mentionable():
    """
    Tests whether ``InteractionMetadataBase.resolve_mentionable`` works as intended.
    """
    vampytest.assert_is(InteractionMetadataBase().resolve_attachment(0), None)


def test__InteractionMetadataBase__resolve_entity():
    """
    Tests whether ``InteractionMetadataBase.resolve_entity`` works as intended.
    """
    vampytest.assert_is(InteractionMetadataBase().resolve_attachment(0), None)
