import vampytest

from ..preinstanced import GuildJoinRequestFormFieldType


@vampytest.call_from(GuildJoinRequestFormFieldType.INSTANCES.values())
def test__GuildJoinRequestFormFieldType__instances(instance):
    vampytest.assert_instance(instance, GuildJoinRequestFormFieldType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, GuildJoinRequestFormFieldType.VALUE_TYPE)
