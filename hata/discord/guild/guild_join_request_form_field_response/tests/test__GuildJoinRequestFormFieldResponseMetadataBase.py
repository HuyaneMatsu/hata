import vampytest

from ..metadata import GuildJoinRequestFormFieldResponseMetadataBase


def test__GuildJoinRequestFormFieldResponseMetadataBase__place_holders():
    metadata = object.__new__(GuildJoinRequestFormFieldResponseMetadataBase)
    vampytest.assert_instance(metadata.accepted, bool)
    vampytest.assert_instance(metadata.terms, tuple, nullable = True)
    vampytest.assert_instance(metadata.placeholder, str, nullable = True)
    vampytest.assert_instance(metadata.value, str, nullable = True)
    vampytest.assert_instance(metadata.choice_index, int)
    vampytest.assert_instance(metadata.choices, tuple, nullable = True)
