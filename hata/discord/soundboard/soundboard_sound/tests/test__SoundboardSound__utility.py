import vampytest

from ....client import Client
from ....core import BUILTIN_EMOJIS
from ....guild import Guild
from ....user import ClientUserBase
from ....utils import is_url

from ..soundboard_sound import SoundboardSound

from .test__SoundboardSound__constructor import _assert_fields_set


def test__SoundboardSound__guild():
    """
    Tests whether ``SoundboardSound.guild`` works as intended.
    """
    guild_id_0 = 202305240042
    guild_id_1 = 202305240043
    
    guild = Guild.precreate(guild_id_0)
    
    for sound_id, input_guild_id, expected_output in (
        (202305240044, guild_id_0, guild),
        (202305240045, guild_id_1, None),
        (202305240046, 0, None),
    ):
        sound = SoundboardSound.precreate(sound_id, guild_id = input_guild_id)
        vampytest.assert_is(sound.guild, expected_output)


def test__SoundboardSound__user():
    """
    Tests whether ``SoundboardSound.user`` works as intended.
    """
    user_id = 202305240047
    
    sound = SoundboardSound(user_id = user_id)
    user = sound.user
    vampytest.assert_instance(user, ClientUserBase)
    vampytest.assert_eq(user.id, user_id)
    
    test_user = sound.user
    vampytest.assert_is(test_user, user)



def test__SoundboardSound__partial__0():
    """
    Tests whether ``SoundboardSound.partial`` works as intended.
    
    Case: Fully partial.
    """
    sound = SoundboardSound()
    output = sound.partial
    
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)


def test__SoundboardSound__partial__1():
    """
    Tests whether ``SoundboardSound.partial`` works as intended.
    
    Case: Not linked to its guild.
    """
    sound_id = 202305270038
    guild_id = 202305270039
    
    guild = Guild.precreate(guild_id)
    
    sound = SoundboardSound.precreate(
        sound_id,
        guild_id = guild_id,
    )
    
    output = sound.partial
    
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)


def test__SoundboardSound__partial__2():
    """
    Tests whether ``SoundboardSound.partial`` works as intended.
    
    Case: Linked to its guild & guild not partial.
    """

    client = Client(
        token = 'token_202305270000',
    )
    try:
        sound_id = 202305270040
        guild_id = 202305270041
        
        guild = Guild.precreate(guild_id)
        guild.clients = [client]
        
        sound = SoundboardSound.precreate(
            sound_id,
            guild_id = guild_id,
        )
        
        guild.soundboard_sounds = {sound_id: sound}
        
        output = sound.partial
        
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, False)
        
    # Cleanup
    finally:
        client._delete()
        client = None


def test__SoundboardSound__copy():
    """
    Tests whether ``SoundboardSound.copy`` works as intended.
    """
    available = False
    emoji = BUILTIN_EMOJIS['heart']
    name = 'rember'
    user_id = 202305240049
    volume = 0.69
    
    sound = SoundboardSound(
        available = available,
        emoji = emoji,
        name = name,
        user_id = user_id,
        volume = volume,
    )
    
    copy = sound.copy()
    _assert_fields_set(copy)
    vampytest.assert_is_not(sound, copy)
    
    vampytest.assert_eq(sound, copy)


def test__SoundboardSound__copy_with__0():
    """
    Tests whether ``SoundboardSound.copy_with`` works as intended.
    
    Case: No fields overwritten.
    """
    available = False
    emoji = BUILTIN_EMOJIS['heart']
    name = 'rember'
    user_id = 202305240050
    volume = 0.69
    
    sound = SoundboardSound(
        available = available,
        emoji = emoji,
        name = name,
        user_id = user_id,
        volume = volume,
    )
    
    copy = sound.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_is_not(sound, copy)
    
    vampytest.assert_eq(sound, copy)


def test__SoundboardSound__copy_with__1():
    """
    Tests whether ``SoundboardSound.copy_with`` works as intended.
    
    Case: All fields overwritten.
    """
    old_available = False
    old_emoji = BUILTIN_EMOJIS['heart']
    old_name = 'rember'
    old_user_id = 202305240051
    old_volume = 0.69
    
    new_available = True
    new_emoji = BUILTIN_EMOJIS['x']
    new_name = 'happy day'
    new_user_id = 202305240052
    new_volume = 0.70
    
    sound = SoundboardSound(
        available = old_available,
        emoji = old_emoji,
        name = old_name,
        user_id = old_user_id,
        volume = old_volume,
    )
    
    copy = sound.copy_with(
        available = new_available,
        emoji = new_emoji,
        name = new_name,
        user_id = new_user_id,
        volume = new_volume,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_is_not(sound, copy)
    
    vampytest.assert_eq(copy.available, new_available)
    vampytest.assert_is(copy.emoji, new_emoji)
    vampytest.assert_eq(copy.name, new_name)
    vampytest.assert_eq(copy.user_id, new_user_id)
    vampytest.assert_eq(copy.volume, new_volume)


def test__SoundboardSound__url():
    """
    tests whether ``SoundboardSound.url`` works as intended.
    """
    sound_id = 202305240054
    
    sound = SoundboardSound.precreate(sound_id)
    output = sound.url
    
    vampytest.assert_instance(output, str)
    vampytest.assert_true(is_url(output))
    vampytest.assert_in(str(sound_id), output)


def test__SoundboardSound__delete():
    """
    Tests whether ``SoundboardSound._delete`` works as intended.
    """
    sound_id = 202305270042
    guild_id = 202305270043
    
    guild = Guild.precreate(guild_id)
    
    sound = SoundboardSound.precreate(
        sound_id,
        guild_id = guild_id,
    )
    
    guild.soundboard_sounds = {sound_id: sound}
    
    sound._delete()
    
    vampytest.assert_eq(guild.soundboard_sounds, None)


def test__SoundboardSound__is_custom_sound__0():
    """
    Tests whether ``SoundboardSound.is_custom_sound`` works as intended.
    
    Case: Template.
    """
    sound = SoundboardSound()
    
    output = sound.is_custom_sound()
    vampytest.assert_instance(output, bool)
    vampytest.assert_true(output)


def test__SoundboardSound__is_custom_sound__1():
    """
    Tests whether ``SoundboardSound.is_custom_sound`` works as intended.
    
    Case: Default.
    """
    sound = SoundboardSound()
    sound.id = 6
    
    output = sound.is_custom_sound()
    vampytest.assert_instance(output, bool)
    vampytest.assert_false(output)


def test__SoundboardSound__is_custom_sound__2():
    """
    Tests whether ``SoundboardSound.is_custom_sound`` works as intended.
    
    Case: Custom.
    """
    sound = SoundboardSound.precreate(202305290000)
    
    output = sound.is_custom_sound()
    vampytest.assert_instance(output, bool)
    vampytest.assert_true(output)


def test__SoundboardSound__is_default_sound__template():
    """
    Tests whether ``SoundboardSound.is_default_sound`` works as intended.
    
    Case: Template.
    """
    sound = SoundboardSound()
    
    output = sound.is_default_sound()
    vampytest.assert_instance(output, bool)
    vampytest.assert_false(output)


def test__SoundboardSound__is_default_sound__default():
    """
    Tests whether ``SoundboardSound.is_default_sound`` works as intended.
    
    Case: Default.
    """
    sound = SoundboardSound()
    sound.id = 6
    
    output = sound.is_default_sound()
    vampytest.assert_instance(output, bool)
    vampytest.assert_true(output)


def test__SoundboardSound__is_default_sound__custom():
    """
    Tests whether ``SoundboardSound.is_default_sound`` works as intended.
    
    Case: Custom.
    """
    sound_id = 202305290001
    
    sound = SoundboardSound.precreate(202305290001)
    
    output = sound.is_default_sound()
    vampytest.assert_instance(output, bool)
    vampytest.assert_false(output)


def test__SoundboardSound__mention():
    """
    Tests whether ``SoundboardSound.mention`` works as intended.
    """
    sound_id = 202501300040
    guild_id = 202501300041
    
    sound = SoundboardSound.precreate(sound_id, guild_id = guild_id)
    
    output = sound.mention
    vampytest.assert_instance(output, str)
