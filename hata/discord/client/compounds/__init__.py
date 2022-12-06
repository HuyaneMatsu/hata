from .achievement import *
from .application_command import *
from .application_role_connection import *
from .auto_moderation import *
from .channel import *
from .client import *
from .client_gayteway import *
from .discovery import *
from .emoji import *
from .guild import *
from .guild_ban import *
from .interaction import *
from .integration import *
from .invite import *
from .locked import *
from .message import *
from .oauth2 import *
from .miscellaneous import *
from .reaction import *
from .role import *
from .scheduled_event import *
from .stage import *
from .sticker import *
from .thread import *
from .user import *
from .webhook import *


__all__ = (
    *achievement.__all__,
    *application_command.__all__,
    *application_role_connection.__all__,
    *auto_moderation.__all__,
    *channel.__all__,
    *client.__all__,
    *client_gayteway.__all__,
    *discovery.__all__,
    *emoji.__all__,
    *guild.__all__,
    *guild_ban.__all__,
    *interaction.__all__,
    *integration.__all__,
    *invite.__all__,
    *locked.__all__,
    *message.__all__,
    *miscellaneous.__all__,
    *oauth2.__all__,
    *reaction.__all__,
    *role.__all__,
    *scheduled_event.__all__,
    *stage.__all__,
    *sticker.__all__,
    *thread.__all__,
    *user.__all__,
    *webhook.__all__,
)


from .achievement import ClientCompoundAchievementEndpoints
from .application_command import ClientCompoundApplicationCommandEndpoints
from .application_role_connection import ClientCompoundApplicationRoleConnectionEndpoints
from .auto_moderation import ClientCompoundAutoModerationEndpoints
from .channel import ClientCompoundChannelEndpoints
from .client import ClientCompoundClientEndpoints
from .client_gayteway import ClientCompoundClientGateway
from .discovery import ClientCompoundDiscoveryEndpoints
from .emoji import ClientCompoundEmojiEndpoints
from .guild import ClientCompoundGuildEndpoints
from .guild_ban import ClientCompoundGuildBanEndpoints
from .interaction import ClientCompoundInteractionEndpoints
from .integration import ClientCompoundIntegrationEndpoints
from .invite import ClientCompoundInviteEndpoints
from .locked import ClientCompoundLockedEndpoints
from .message import ClientCompoundMessageEndpoints
from .miscellaneous import ClientCompoundMiscellaneousEndpoints
from .oauth2 import ClientCompoundOauth2Endpoints
from .reaction import ClientCompoundReactionEndpoints
from .role import ClientCompoundRoleEndpoints
from .scheduled_event import ClientCompoundScheduledEventEndpoints
from .stage import ClientCompoundStageEndpoints
from .sticker import ClientCompoundStickerEndpoints
from .thread import ClientCompoundThreadEndpoints
from .user import ClientCompoundUserEndpoints
from .webhook import ClientCompoundWebhookEndpoints


CLIENT_COMPOUNDS = (
    ClientCompoundAchievementEndpoints,
    ClientCompoundApplicationCommandEndpoints,
    ClientCompoundApplicationRoleConnectionEndpoints,
    ClientCompoundAutoModerationEndpoints,
    ClientCompoundChannelEndpoints,
    ClientCompoundClientEndpoints,
    ClientCompoundClientGateway,
    ClientCompoundDiscoveryEndpoints,
    ClientCompoundEmojiEndpoints,
    ClientCompoundGuildEndpoints,
    ClientCompoundGuildBanEndpoints,
    ClientCompoundInteractionEndpoints,
    ClientCompoundIntegrationEndpoints,
    ClientCompoundInviteEndpoints,
    ClientCompoundLockedEndpoints,
    ClientCompoundMessageEndpoints,
    ClientCompoundMiscellaneousEndpoints,
    ClientCompoundOauth2Endpoints,
    ClientCompoundReactionEndpoints,
    ClientCompoundRoleEndpoints,
    ClientCompoundScheduledEventEndpoints,
    ClientCompoundStageEndpoints,
    ClientCompoundStickerEndpoints,
    ClientCompoundThreadEndpoints,
    ClientCompoundUserEndpoints,
    ClientCompoundWebhookEndpoints,
)
