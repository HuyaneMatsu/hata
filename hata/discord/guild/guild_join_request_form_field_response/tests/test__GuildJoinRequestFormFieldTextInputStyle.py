import vampytest

from ..preinstanced import GuildJoinRequestFormFieldTextInputStyle


@vampytest.call_from(GuildJoinRequestFormFieldTextInputStyle.INSTANCES.values())
def test__GuildJoinRequestFormFieldTextInputStyle__instances(instance):
    vampytest.assert_instance(instance, GuildJoinRequestFormFieldTextInputStyle)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, GuildJoinRequestFormFieldTextInputStyle.VALUE_TYPE)
