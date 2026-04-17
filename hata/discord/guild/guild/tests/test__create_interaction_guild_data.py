import vampytest

from ....localization import Locale

from ..guild import Guild
from ..preinstanced import GuildFeature
from ..utils import create_interaction_guild_data


def test__create_interaction_guild_data():
    """
    Tests whether ``create_interaction_guild_data`` works as intended.
    """
    guild_id = 202310100000
    
    locale = Locale.dutch
    features = [GuildFeature.icon_animated]
    
    expected_output = {
        'id': str(guild_id),
        'locale': locale.value,
        'preferred_locale': locale.value,
        'features': [feature.value for feature in features],
    }
    

    guild = Guild.precreate(
        guild_id,
        locale = locale,
        features = features,
    )
    
    vampytest.assert_eq(
        create_interaction_guild_data(guild),
        expected_output,
    )
